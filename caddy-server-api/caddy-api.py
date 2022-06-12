import json
import sys
import urllib.parse
import urllib.request


def simple_website(website_id, host=None, upstream=None):
    config = dict(
        match=[
            dict(
                host=[host])
            ],
        terminal=True,
        handle=[
            #dict(
            #    handler='vars',
            #    website_id=website_id),
            dict(
                handler='reverse_proxy',
                upstreams=[dict(dial=upstream)])
        ])

    config['@id'] = website_id

    return api(path='apps/http/servers/server0/routes', method='POST', data=config)


def static_website(website_id, host=None, status_code=200, headers={}, body=None):
    config = dict(
        match=[
            dict(
                host=[host])
            ],
        terminal=True,
        handle=[
            #dict(
            #    handler='vars',
            #    website_id=website_id),
            dict(
                handler='static_response',
                status_code=status_code,
                headers=headers,
                body=body)
            ])

    config['@id'] = website_id

    return api(path='apps/http/servers/server0/routes', method='POST', data=config)


def initial_config():
    # https://ping.localhost/

    response = api(path='', method='DELETE') # current configuration

    config = dict(
        apps=dict(
            http=dict(
                servers=dict(
                    server0=dict(
                        listen=[':443'],
                        routes=[])
                    )
                )
            )
        )

    response = api(path='', method='PUT', data=config)

    response = static_website('ping', host='ping.localhost', 
        headers={'Content-Type':['application/json']},
        body='{"result":"ok", "website":"{http.vars.id}", "unix_ms":"{time.now.unix_ms}"}')


def api(path='', method='GET', string=None, data=None):
    base_url = 'http://localhost:2019/config/'

    if string:
        data = string.encode('utf-8')

    elif data:
        data = json.dumps(data, indent=2).encode('utf-8')

    if data:
        req = urllib.request.Request(base_url + path, data=data, method=method)

    else:
        req = urllib.request.Request(base_url + path, method=method)

    req.add_header('Content-Type', f'application/json')

    try:
        with urllib.request.urlopen(req) as response:
            r = response.read().decode('utf-8')

            if response.status != 200:
                print(f'{path} ({response.status=})')
                return dict(message=f'Error HTTP Status {response.status}', path=path)

            if len(r) == 0:
                return dict(message=response.msg, path=path)

            return json.loads(r)

    except urllib.error.HTTPError as e:
        # status=500 returned for PUT value and other configuration errors
        return dict(message=str(e), path=path)

    except json.decoder.JSONDecodeError as e:
        return dict(message=str(e), path=path)

    return dict(message='unknown error', path=path)


def list_websites():
    # Update to use @id instead of vars

    routes = api('apps/http/servers/server0/routes/')

    for route in routes:
        website_id = route.get('@id', 'unknown')
        reverse_proxy = ''

        for handle in route['handle']:
            handler = handle['handler']

            # if handler == 'vars':
            #     website_id = handle['website_id']

            if handler == 'reverse_proxy':
                reverse_proxy = str(handle['upstreams'][0]['dial'])

        print((f'{website_id:10} {handler:20} {reverse_proxy}'))


def main():
    # base config and ping.local website
    initial_config()

    # Example: fetch the entire configuration
    # response = api()

    # Example: get the first route
    # response = api('apps/http/servers/srv0/routes/0')

    # Example: add an additional listener on the first route
    # response = api(path='apps/http/servers/srv0/listen/0', method='PUT', string='":2231"')

    # Example: replace the first listener on the first route
    # response = api(path='apps/http/servers/srv0/listen/0', method='PATCH', string='":2223"')

    # for the next examples, a simple server should be listening in localhost:9004

    # Example (https://test.localhost/): add reverse_proxy from test.localhost to localhost:9004
    simple_website('test', host='test.localhost', upstream='localhost:9004')

    # Example (https://www.test.localhost/): redirect from www.test.localhost to test.localhost
    static_website('www.test', host='www.test.localhost', status_code=302, 
        headers={'Location':['https://test.localhost{http.request.uri}']})

    list_websites()


if __name__ == '__main__':
    main()
