from aiohttp import web
import json
import os

routes = web.RouteTableDef()


def get_user(request):
    user = request.headers.get('X-User')

    if not user:
        raise web.HTTPForbidden()

    return json.loads(user)


@routes.get('/')
async def index(request):
    user = get_user(request)

    print(f'page for {user=}')
    return web.Response(text=f'App Server\n{user=}')


@routes.get('/admin')
async def index(request):
    user = get_user(request)

    if 'admin' not in user.get('roles', []):
        return web.Response(text='You must be an admin user to view this page')

    return web.Response(text='Admin page')


@routes.get('/test')
async def index(request):
    return web.Response(text='Test page')


@routes.get('/api-test')
async def index(request):
    return web.json_response(dict(result='ok', title='API Test Page'))


if __name__ == '__main__':
    print('starting app server')

    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, port=8002)
