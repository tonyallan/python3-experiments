# python3-experiments
Exploring Python3 and various APIs using Python 3 code snippets.

When I try something new I create a simple proof of concept script 
to figure out how to use a feature or new module or API.
Because I might need an example in a future project it seems like a 
good idea to document these experiements.


## Running the samples
It is assumed that:
* the current working directory is `~/GitHub/python3-experiments`
* and that `caddy` has been copied to this directory


## Caddy Server API
A Python 3 example on how to control the [Caddy server](https://caddyserver.com/) 
using the [REST API](https://caddyserver.com/docs/quick-starts/api).

[Details](caddy-server-api/)


## Caddy Server Python FastCGI
A Python 3 example using the Caddy reverse proxy `fastCGI` transport.

[Details](caddy-server-fastcgi/)


## Caddy Server Authentication
This is a example of how to use the Caddy forward_auth directive to create a separate authentication server.

[Details](caddy-server-auth/)


## Python readline adds add history and editting to input()
[Details](python-readline/)
