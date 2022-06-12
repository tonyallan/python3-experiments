# Caddy Server API
The [Caddy server](https://caddyserver.com/) has a [REST API](https://caddyserver.com/docs/quick-starts/api)

The following examples show how to use the API using Python 3.

## Setup
These examples used Caddy v2.5.1.

View your full configuration
http://localhost:2019/config/


Start Caddy with no initial configuration
```
./caddy run
```

While it is running you can access the
* Configuration endpoint <http://localhost:2019/config>
* Metrics endpoint <http://localhost:2019/metrics>


Start a local webserver (anything will do) for the examples
```
python3 -m http.server 9004 --bind=localhost
```

Download and then run the example
```
python3 caddy-api.py
```

Have a look at various URL's
* <http://localhost:2019/config/apps/http/servers/server0>
* The ping website <https://ping.localhost/>
* The test website <https://test.localhost/>
* Redirecting `www` <https://www.test.localhost/>
* The various website definitions
  - <http://localhost:2019/id/ping>
  - <http://localhost:2019/id/test>
  - <http://localhost:2019/id/www.test>

You can perform specific functions (e.g. stopping Caddy)
```
curl -X POST "http://localhost:2019/stop"
```

basic json config structure (https://caddyserver.com/docs/json/)
{
    "admin": {},
    "logging": {},
    "storage": {•••},
    "apps": {•••}
}

basic routes structure
[{
    "group": "",
    "match": [{•••}],
    "handle": [{•••}],
    "terminal": false
}]
```



## References
1. [Caddy server website](https://caddyserver.com/)
1. [REST API](https://caddyserver.com/docs/quick-starts/api)
1. [API Tutorial](https://caddyserver.com/docs/api-tutorial)