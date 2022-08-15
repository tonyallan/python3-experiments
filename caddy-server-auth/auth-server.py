from aiohttp import web
import base64
import hashlib
import json
import os
import secrets
import sys
import urllib.parse


# Datastore is a minimal implementation for the purposes of the example

class Datastore:
    def __init__(self):
        self.users = {}
        self.tokens = {}


    def add_user(self, user_id, **user_info):
            self.users[user_id] = user_info


    def get_user(self, user_id, remove_password=True):
        if user_id not in self.users:
            return None

        user = self.users.get(user_id).copy()

        user['user_id'] = user_id

        if remove_password and 'password' in user:
            del user['password']

        return user


    def get_user_by_email(self, email, remove_password=True):
        for user_id, user in self.users.items():
            if user.get('email') == email:
                return self.get_user(user_id, remove_password=remove_password)

        return None


    def get_user_from_token(self, token, remove_password=True):
        user_id = self.get_token(token)

        return self.get_user(user_id, remove_password=remove_password)


    def add_token(self, value, type='token', bits=128, test=None):
        t = base64.b32encode(secrets.token_bytes(int(bits / 8))).decode('utf-8').lower().replace('=', '')
        token = type + '-' + t

        if test:
            token = test

        self.tokens[token] = value

        return token


    def get_token(self, token):
        return self.tokens.get(token)


    def delete_token(self, token):
        if token in self.tokens:
            del self.tokens[token]


routes = web.RouteTableDef()


def check_password(password, hashed_and_salted_password):
    if password is None:
        return False

    password_to_check = base64.b64decode(hashed_and_salted_password.encode('utf-8'))
    salt = password_to_check[:8] # 64 bit
    hashed_password = password_to_check[8:]

    h = hashlib.blake2b(salt=salt)
    h.update(password.encode('utf-8'))

    return hashed_password == h.digest()


def response_ok(text, headers={}):
    print('HTTPOk', text)

    raise web.HTTPOk(text=text, headers=headers)


def response_unauthorized(text, headers={}, redirect=None):
    print('HTTPUnauthorized', text)

    query = {}

    if text is not None:
        query['reason'] = text

    if redirect is not None:
        query['redirect'] = redirect

    query_text = urllib.parse.urlencode(query)

    raise web.HTTPFound(text=text, location='/auth/sign-in?' + query_text, headers=headers)


def get_user_from_header(request):
    user = request.headers.get('X-User')

    if user is None:
        response_unauthorized('X-User header not found')

    try:
        return json.loads(user)

    except json.decoder.JSONDecodeError as e:
        print('get_user_from_header()', e)
    
    response_unauthorized('invalid X-User header')


def delete_auth_cookie(request):
    ds = request.app.get('ds')
    domain = request.headers.get('Host')

    session_token = request.cookies.get('Auth')
    
    ds.delete_token(session_token)

    return {'Set-Cookie': f'Auth=deleted; Domain={domain}; ' + \
                      'Path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT'}


@routes.get('/auth/check')
async def auth_check(request):
    ds = request.app.get('ds')

    forwarded_uri = request.headers.get('X-Forwarded-Uri')
    forwarded_path = urllib.parse.urlparse(forwarded_uri).path
    print(f'---------- /auth/check ---------> {forwarded_path}')

    authorization = request.headers.get('Authorization')

    if authorization:
        # Bearer token authentication (assume JSON based)

        b, api_token = authorization.split(' ', 1)

        user = ds.get_user_from_token(api_token)

        print(f'{api_token=} {user=}')

        if user is None:
            raise web.HTTPUnauthorized()

    else:
        # Password authentication

        if forwarded_path in ['/auth/sign-in', '/auth/password-authenticate']:
            response_ok(f'no auth check for {forwarded_path}')

        session_token = request.cookies.get('Auth')
        print(f'found {session_token=}')

        if forwarded_uri == '/auth/sign-out':
            forwarded_uri = None

        if session_token is None:
            response_unauthorized('(auth cookie not found)', redirect=forwarded_uri)

        user = ds.get_user_from_token(session_token)

        if user is None:
            headers = delete_auth_cookie(request)
            response_unauthorized(f'(user not found)', headers=headers, redirect=forwarded_uri)

    headers = {'X-User': json.dumps(user)}
    response_ok('continue to authorised page', headers=headers)


# all remaining routes are auth server functions

@routes.post('/auth/password-authenticate')
async def auth_password_authenticate(request):
    ds = request.app.get('ds')

    print('POST /auth/password-authenticate')

    domain = request.headers.get('Host')

    if request.can_read_body:
        body     = await request.text()
        data     = urllib.parse.parse_qs(body)

        email    = data.get('email', [None])[0]
        password = data.get('password', [None])[0]
        redirect = data.get('redirect', [None])[0]

        if email is None:
            response_unauthorized('Please enter an email address')

        if password is None:
            response_unauthorized('Please enter a password')

        user = ds.get_user_by_email(email, remove_password=False)

        if user is None:
            response_unauthorized('Email address not found')

        user_id = user.get('user_id')

        stored_password = user.get('password')

        if not check_password(password, stored_password):
            response_unauthorized('Invalid password')

        session_token = ds.add_token(user_id, type='session')

        headers = {'Set-Cookie': f'Auth={session_token}; Max-Age=5184000; Domain={domain}; ' + \
                          'Path=/; Secure; HttpOnly; SameSite=Lax;'}

        print(f'setting cookie and adding session token {session_token}')

        if not redirect:
            redirect = '/'

        print(f'{ds.tokens=} {redirect=}')

        raise web.HTTPFound(location=redirect, headers=headers)


@routes.get('/auth/sign-in')
async def sign_in(request):
    print('/sign-in page (then post to /auth/password-authenticate)')

    return web.Response(content_type='text/html', text=f"""
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Sign-in</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css" rel="stylesheet" 
                integrity="sha384-+0n0xVW2eSR5OomGNYDnhzAbDsOXxcvSN1TPprVMTNDbiYZCxYbOOl7+AMvyTG2x" 
                crossorigin="anonymous">
          </head>

          <body>
              <div class="container mt-5 text-center">
              </div>
              <div class="container mt-2 mb-5" style="width: 330px;">

                <h4 class="text-center text-secondary mt-3">
                 Please Sign-in
                </h4>
                <p id="message" class="text-center small text-warning"></p>

                <form action="/auth/password-authenticate" method="post">
                  <input type="hidden" id='redirect' name="redirect" vaue="">
                  <div class="form-group mt-2">
                    <input type="email" class="form-control" name="email" placeholder="Email address">
                  </div>
                  <div class="form-group mt-2">
                    <input type="password" class="form-control" name="password" placeholder="Password">
                  </div>
                  <button type="submit" name="sub-type" value="password" class="btn btn-primary w-100 mt-2">
                    Sign-in with password</button>
                  <!--  button type="submit" name="sub-type" value="email" class="btn btn-secondary w-100 mt-2">
                    Sign-in with email</button -->
                </form>
                <!-- p class="text-center small text-secondary">No password is needed when signing-in via email. 
                    Check your email for link.</p -->
              </div>

            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/js/bootstrap.bundle.min.js" 
                integrity="sha384-gtEjrD/SeCtmISkJkNUaaKMoLD0//ElJ19smozuHV6z3Iehds+3Ulb9Bn9Plx0x4" 
                crossorigin="anonymous"></script>
            <script>
                const params = new Proxy(new URLSearchParams(window.location.search), {{
                  get: (searchParams, prop) => searchParams.get(prop),
                }});

                document.getElementById("message").textContent = params.reason;
                document.getElementById("redirect").value = params.redirect;
            </script>
          </body>
        </html>
        """)


@routes.get('/auth/sign-out')
async def auth_sign_out(request):
    headers = delete_auth_cookie(request)

    user = get_user_from_header(request)
    user_name = user.get('name')

    response_ok(f'{user_name} signed-out', headers=headers)


if __name__ == '__main__':
    print('starting auth server')

    app = web.Application()
    app.add_routes(routes)

    ds = Datastore()

    ds.add_user('30000', name='John Smith', email='john@example.com', roles=['admin'],
        password='XhgQ0LD5a9V/FSeGn2s+LiF5eb4w2OspcPo/AjqNW1NkItexaB/z7Eltp+ymcIHrqSzIK+T2f3TRi09dKGmtSw1NHu4nynSV')
    ds.add_user('30001', name='Service Account', roles=['service-account'])
    ds.add_user('30002', name='Mary Jones', email='mary@example.com', roles=['user'],
        password='bDYJ4jMqxfDmiwAICkwYsfacfFFZKtcrRlu4YiuwC768k1PVy0wWJROH4TDmkQK1jxO8GQ4sjTqfkDFv3tHguBMIzjtCq00I')

    if len(sys.argv) == 2:
        # if a token is specified, make sure it is long and random (e.g. api-bfyujsagbtnfvfwjvwfut3hiwy)
        api_token = ds.add_token('30001', test=sys.argv[1])

    else:
        api_token = ds.add_token('30001', type='api')
    

    print(f'Authorization: Bearer {api_token}')
 
    app['ds'] = ds

    web.run_app(app, port=8001)
