# Caddy Server FastCGI
The [Caddy server](https://caddyserver.com/) supports the reverse_proxy
[fastcgi](https://caddyserver.com/docs/caddyfile/directives/reverse_proxy#the-fastcgi-transport) transport.

This is a simple test of the functionality using python.

See [test.py](test.py).


## Setup
This example assumes Caddy v2.5.1 or later.

Install the [fastcgi](https://pypi.org/project/fastcgi/) dependancy:
```
pip install fastcgi
```

Use following `Caddyfile`:

```
fastcgi.localhost {
    reverse_proxy unix/caddy-server-fastcgi/fcgi.sock {
        transport fastcgi
    }
}
```

Start Caddy:
```shell
cd ~/GitHub/python3-experiments
./caddy run --config caddy-server-fastcgi/Caddyfile
```

The test is very simple:
```python3
import json
from fastcgi import *
import os

print('starting', file=sys.stderr)

@fastcgi()
def hello():
    query   = os.environ["QUERY_STRING"]
    path    = os.environ["PATH_INFO"]
    environ = '\n' + json.dumps(os.environ, indent=2)
    content = sys.stdin.read()

    print(f'request {path}', file=sys.stderr)

    sys.stdout.write(f"Content-type: text/html\r\n\r\n")
    sys.stdout.write(f"""
        <h1>FastCGI Test</h1>
        <pre>
        \nos.environ =
        {environ}
        </pre>\r\n
    """)
```

Start the app in a separate terminal:
```
cd ~/GitHub/python3-experiments/caddy-server-fastcgi
python3 test.py
```

This creates a unix socket file `fcgi.sock` with a filename that matches the `Caddyfile`. 

GUI file managers hide UNIX socket files so use `ls` in the terminal.

Use your browser to view:
* <https://fastcgi.localhost/aaa?a=b>
