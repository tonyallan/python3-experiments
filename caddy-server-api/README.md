# Caddy Server API
The [Caddy server](https://caddyserver.com/) has a [REST API](https://caddyserver.com/docs/quick-starts/api)

The following examples show how to use the API using Python 3.

## Setup

View your full configuration
http://localhost:2019/config/

# setup
These examples used Caddy v2.5.1.

Start Caddy with no initial configuration

`./caddy run`

```
cd ~/Development/webproject-apps/test1
#python3 main.py --port 9004 --env test
python3 -m http.server 9004 --bind=localhost

cd ~/Development/webproject-experiments
python3 caddy-api.py

Admin endpoint tcp/localhost:2019
http://localhost:2019/config/apps/http/servers/srv0/routes/0

Metrics endpoint
http://localhost:2019/metrics


curl -X POST "http://localhost:2019/stop"

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
1 [Caddy server website](https://caddyserver.com/)
1 [Caddy REST API](https://caddyserver.com/docs/quick-starts/api)