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
