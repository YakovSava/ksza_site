import asyncio

from json import loads
from argparse import ArgumentParser
from aiohttp.web import Application, run_app, RouteTableDef, Response, Request, json_response
from plugins.binder import Binder
from static import app as subapp
from rtmp_server import serve_rtmp

routes = RouteTableDef()
app = Application()
binder = Binder()
parser = ArgumentParser()

app.add_subapp('/static', subapp)

parser.add_argument('--host', description='Host for listening', default='127.0.0.1')
parser.add_argument('--port', description='Port for listening', default=80)
parser.add_argument('--rtmp', description='Port for rtmp-server listening', default=1935)

@routes.get('/service/get?method={method}&data={data}')
async def service_path(request: Request):
	method, data = list(
		map(
			lambda x: x.split('=')[1],
			(str(request.url)
			.split('?')[1]
			.split('&')
			)
		)
	)
	data = loads(data)
	if method == 'getColumns':
		columns = await binder.get_columns(data)
		return json_response(
			data={'columns': columns}
		)
	elif method == 'devTest':
		return json_response(
			data={'test': 2}
		)
	else:
		return json_response(
			data={'error': f'Method {method} not exist!'}
		)

@routes.get('/')
async def home_page(request: Request):
	data = await binder.get_html(filename='index.html')
	return Response(
		status=data['status'],
		body=data['body'],
		content_type=data['content_type']
	)


@routes.get('/servicelist')
async def getz_service_list(request: Request):
	data = await binder.get_html('service.html')
	return Response(
		status=data['status'],
		body=data['body'],
		content_type=data['content_type']
	)

app.add_routes(routes)

args = parser.parse_args()

async def listening_server(loop):
	run_app(app, host=args.host, port=args.port, loop=loop)

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(
		asyncio.wait([
			loop.create_task(listening_server(loop)),
			loop.create_task(serve_rtmp(host=args.host, port=args.rtmp))
		])
	)
