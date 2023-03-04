from aiohttp.web import Application, run_app, RouteTableDef, Response, Request
from plugins.binder import Binder

routes = RouteTableDef()
app = Application()
binder = Binder()

@routes.get('/scripts/{scriptname}')
async def get_js(request:Request):
	data = await binder.get_js(path='scripts/'+str(request.url).split('/')[-1])
	return Response(
		status=data['status'],
		body=data['body'],
		content_type=data['content_type']
	)

@routes.get('/styles/{stylesheet}')
async def get_css(request:Request):
	data = await binder.get_css(path='styles/'+str(request.url).split('/')[-1])
	return Response(
		status=data['status'],
		body=data['body'],
		content_type=data['content_type']
	)

@routes.get('/header/{stylesheet}')
async def get_css2(request:Request):
	data = await binder.get_css(path='styles/'+str(request.url).split('/')[-1])
	return Response(
		status=data['status'],
		body=data['body'],
		content_type=data['content_type']
	)

@routes.get('/png/{filename}')
async def get_png(request:Request):
	data = await binder.get_png(path='png/'+str(request.url).split('/')[-1])
	return Response(
		status=data['status'],
		body=data['body'],
		content_type=data['content_type']
	)

@routes.get('/')
async def home_page(request:Request):
	data = await binder.get_html(filename='index.html')
	return Response(
		status=data['status'],
		body=data['body'],
		content_type=data['content_type']
	)

if __name__ == '__main__':
	app.add_routes(routes)
	run_app(app, host='127.0.0.1', port='80')