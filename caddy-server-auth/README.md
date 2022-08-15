# Caddy Server Authentication

This is a example of how to use the Caddy [forward_auth](https://caddyserver.com/docs/caddyfile/directives/forward_auth) directive to create a separate authentication server.

See [auth-server.py](auth-server.py) and [app-server.py](app-server.py).

> Important note: The security of this example has not been independantly reviewed. Use at your own risk.


## Setup
This example assumes Caddy v2.5.1 or later.


Use following `Caddyfile`:

```
localhost {
    forward_auth localhost:8001 {
        uri /auth/check
        copy_headers X-User X-Forwarded-Uri
    }

    reverse_proxy /auth/* localhost:8001
    reverse_proxy localhost:8002
}
```

Start Caddy:
```shell
cd ~/GitHub/python3-experiments
./caddy run --config caddy-server-auth/Caddyfile
```

Start the app server in a separate terminal:
```shell
cd ~/GitHub/python3-experiments/caddy-server-auth
python3 app-server.py

starting app server
======== Running on http://0.0.0.0:8002 ========
(Press CTRL+C to quit)
```

Start the auth server in another separate terminal (a hardcoded token is specified for this example only:
```shell
cd ~/GitHub/python3-experiments/caddy-server-auth
python3 auth-server.py api-bfyujsagbtnfvfwjvwfut3hiwy

starting auth server
Authorization: Bearer api-bfyujsagbtnfvfwjvwfut3hiwy
======== Running on http://0.0.0.0:8001 ========
(Press CTRL+C to quit)
```

Use your browser to view the website — <https://localhost/test>.


## Caddyfile

The `Caddyfile` has three parts.

The first part uses the route `/auth/check` to filter requests to the proxies that follow.

1`forward_auth` forwards all requests to `/auth/check` using the `GET` method so as not to consume the body (if present).
1. The `X-User` header contains some information about the authenticated user.
1. The `X-Forwarded-Uri` header passes the original path to the proxy servers.

```
    forward_auth localhost:8001 {
        uri /auth/check
        copy_headers X-User X-Forwarded-Uri
    }
```

The second part is a proxy to handle all requests for the `/auth` route. 
```
    reverse_proxy /auth/* localhost:8001
```

In this example the auth server has the following routes:
* `/auth/check` — filter requests (described above)
* `/auth/password-authenticate` — processes the sign-in form and creates the session token and cookie
* `/auth/sign-in` — display the sign-in web page
* `/auth/sign-out` — removes the session-token and cookie


The last part of the `Caddyfile` passes all remaining requests to the application server.
```
    reverse_proxy localhost:8002
```

In this example the app server has the following routes:
* `/`
* `/admin` — authorises users with a role of `admin` to view the page
* `/test`
* `/api-test` — returns JSON data for api access




## API example (use the api token returned when the server starts)

As well as password users, an API can access the website using the `Authorization` header.

When the auth server starts, it prints the 

```shell
curl --header "Authorization: Bearer api-bfyujsagbtnfvfwjvwfut3hiwy" https://localhost/api-test
{"result": "ok", "title": "API Test Page"}

curl --header "Authorization: Bearer api-zzz" https://localhost/api-test
401: Unauthorized

curl --header "Authorization: Bearer api-bfyujsagbtnfvfwjvwfut3hiwy" https://localhost/zzz     
404: Not Found

````
