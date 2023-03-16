from aiohttp.web import Response, Application, Request, RouteTableDef
from plugins.binder import Binder

app = Application()
routes = RouteTableDef()
binder = Binder()

@routes.get('/')
async def main_static_handler(request:Request):
	return Response(status=418)

@routes.get('/scripts/{scriptname}')
async def get_js(request: Request):
	data = await binder.get_js(path='scripts/' + str(request.url).split('/')[-1])
	return Response(
		status=data['status'],
		body=data['body'],
		content_type=data['content_type']
	)


@routes.get('/styles/{stylesheet}')
async def get_css(request: Request):
	data = await binder.get_css(path='styles/' + str(request.url).split('/')[-1])
	return Response(
		status=data['status'],
		body=data['body'],
		content_type=data['content_type']
	)


@routes.get('/header/{stylesheet}')
async def get_css2(request: Request):
	data = await binder.get_css(path='styles/' + str(request.url).split('/')[-1])
	return Response(
		status=data['status'],
		body=data['body'],
		content_type=data['content_type']
	)


@routes.get('/png/{filename}')
async def get_png(request: Request):
	data = await binder.get_png(path='png/' + str(request.url).split('/')[-1])
	return Response(
		status=data['status'],
		body=data['body'],
		content_type=data['content_type']
	)

app.add_routes(routes)

if __name__ == '__main__':
	from aiohttp.web import run_app

	run_app(app, host='127.0.0.1', port=80)