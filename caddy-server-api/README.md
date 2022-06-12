# Caddy Server API
The [Caddy server](https://caddyserver.com/) has a [REST API](https://caddyserver.com/docs/quick-starts/api)

The following examples show how to use the API using Python 3.

See [caddy-api.py](https://github.com/tonyallan/python3-experiments/blob/main/caddy-server-api/caddy-api.py).


## Setup
These examples used Caddy v2.5.1.

View your full configuration
http://localhost:2019/config/

Start Caddy with no initial configuration:
```
./caddy run
```

While it is running you can access the:
* Configuration endpoint <http://localhost:2019/config>
* Metrics endpoint <http://localhost:2019/metrics>


Start a local webserver (anything will do) for the examples:
```
python3 -m http.server 9004 --bind=localhost
```


## Example script `caddy-api.py`
Download and then run the example:
```
python3 caddy-api.py
```

Sample output:
```
ping       static_response      
test       reverse_proxy        localhost:9004
www.test   static_response
```

Have a look at various Caddy [Configuration URLs](https://caddyserver.com/docs/api#get-configpath):
* <http://localhost:2019/config/>
* <http://localhost:2019/config/apps/http/servers/server0>
* The various website definitions (using [@id](https://caddyserver.com/docs/api#using-id-in-json) definitions)
  - <http://localhost:2019/id/ping>
  - <http://localhost:2019/id/ping/handle/0/body>
  - <http://localhost:2019/id/test>
  - <http://localhost:2019/id/www.test>

And the three websites:
* The ping website <https://ping.localhost/>
* The test website <https://test.localhost/>
* Redirecting `www` <https://www.test.localhost/>

Notes:
* Most configuration errors return an unhelpful status 500. The Caddy log might give a hint about the error.

### Sample configuration extract

<http://localhost:2019/id/ping/> response:
```json
{
  "@id": "ping",
  "handle": [
    {
      "body": "{\"result\":\"ok\", \"unix_ms\":\"{time.now.unix_ms}\"}",
      "handler": "static_response",
      "headers": {
        "Content-Type": [
          "application/json"
        ]
      },
      "status_code": 200
    }
  ],
  "match": [
    {
      "host": [
        "ping.localhost"
      ]
    }
  ],
  "terminal": true
}
```


## Other API functions
You can also perform specific functions (e.g. [stopping](https://caddyserver.com/docs/api#post-stop) Caddy)
```
curl -X POST "http://localhost:2019/stop"
```

The base [JSON Config Structure](https://caddyserver.com/docs/json/) is:
```
{
    "admin": {•••},
    "logging": {•••},
    "storage": {•••},
    "apps": {•••}
}
```

Each [route](https://caddyserver.com/docs/json/apps/http/servers/routes/) has the structure (within the whole JSON config):
```
{'apps': 
    {'http': 
        {'servers': 
            {'server0': 
                {'listen': [':443'], 
                    'routes': [
                        {
                            "group": "",
                            "match": [{•••}],
                            "handle": [{•••}],
                            "terminal": false
                        },
                        {•••},
                        {•••},
                    ]
                }
            }
        }
    }
}
```

Because you can POST to a point within the overall structure, code can be simpler, for example:
```python3
def simple_website(website_id, host=None, upstream=None):
    config = dict(
        match=[
            dict(
                host=[host])
            ],
        terminal=True,
        handle=[
            dict(
                handler='reverse_proxy',
                upstreams=[dict(dial=upstream)])
        ])

    config['@id'] = website_id

    return api(path='apps/http/servers/server0/routes', method='POST', data=config)
```

With a call such as:
```python3
simple_website('test', host='test.localhost', upstream='localhost:9004')
```


## Vars
There is also a function to define variables to use in configuration strings:
```
handle=[
    dict(
        handler='vars',
        foo=bar),
    dict(
        handler='static_response',
        •••)
    ])
```

The variables are accessed using a string such as:
```
"{http.vars.foo}"
```


## References
1. [Caddy server website](https://caddyserver.com/)
1. [REST API](https://caddyserver.com/docs/quick-starts/api)
1. [API Tutorial](https://caddyserver.com/docs/api-tutorial)