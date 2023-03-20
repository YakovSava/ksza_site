import asyncio

from json import loads
from urllib.parse import unquote
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

parser.add_argument('--host', help='Host for listening', default='127.0.0.1')
parser.add_argument('--port', help='Port for listening', default=80)
parser.add_argument('--rtmp', help='Port for rtmp-server listening', default=1935)

@routes.get('/service/get')
async def service_path(request: Request):
	try: method, data = list(
		map(
			lambda x: x.split('=')[1],
			(str(request.url)
			.split('?')[1]
			.split('&')
			)
		)
	)
	except: return Response(status=418)
	data = loads(unquote(data))
	if method == 'getColumns':
		columns = await binder.get_columns()
		return json_response(
			data={'columns': columns}
		)
	elif method == 'devTest':
		return json_response(
			data={'test': 2}
		)
	elif method == 'changePylist':
		await bindere.change_pylist(data)
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
async def get_service_list(request: Request):
	data = await binder.get_html('service.html')
	return Response(
		status=data['status'],
		body=data['body'],
		content_type=data['content_type']
	)

@routes.get('/stream')
async def get_stream_page(request:Request):
	data = await binder.get_html('stream.html')
	return Response(
		status=data['status'],
		body=data['body'],
		content_type=data['content_type']
	)

@routes.get('/change')
async def change_handler(request:Request):
	data = await binder.get_html('change.html')
	return Response(
		status=data['status'],
		body=data['body'],
		content_type=data['content_type']
	)

app.add_routes(routes)

args = parser.parse_args()

if __name__ == '__main__':
	from threading import Timer

	loop = asyncio.get_event_loop()

	pr = Timer(10, run_app, args=(app,), kwargs=dict(host=args.host, port=args.port, loop=asyncio.new_event_loop()))
	pr.start()

	loop.run_until_complete(
		asyncio.wait([
			loop.create_task(serve_rtmp(host=args.host, port=args.rtmp))
		])
	)
