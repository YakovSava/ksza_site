import asyncio

from json import loads
from urllib.parse import unquote
from argparse import ArgumentParser
from aiohttp.web import Application, RouteTableDef, Response, Request, json_response, AppRunner, TCPSite
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
		await binder.change_pylist(data)
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

async def run_app():
    runner = AppRunner(app)
    await runner.setup()
    site = TCPSite(runner, args.host, args.port)
    await site.start()
    print(f"App is running")
    while True: ...

if __name__ == '__main__':
	loop = asyncio.get_event_loop()

	# asyncio.to_thread(run_app, app, host=args.host, port=args.port, loop=asyncio.new_event_loop())

	loop.run_until_complete(
		asyncio.wait([
			loop.create_task(serve_rtmp(host=args.host, port=args.rtmp)),
			loop.create_task(run_app())
		])
	)
