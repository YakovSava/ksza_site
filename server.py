from aiohttp.web import Application, run_app, RouteTableDef, Response, Request
from plugins.binder import Binder

routes = RouteTableDef()
app = Application()
binder = Binder()

@routes.get('/scripts/{scriptname}')
async def get_js(request:Request):
	data = await binder.get_css(path='css'+request.url.split('/')[-1])
	return Response(
		status=data['status'],
		body=data['body'],
		content_type=data['content_type']
	)

@routes.get('/styles/{stylesheet}')
async def get_css(request:Request):
	data = await binder.get_js(path='js'+request.url.split('/')[-1])
	return Response(
		status=data['status'],
		body=data['body'],
		content_type=data['content_type']
	)

@routes.get('/')
async def home_page(request:Request):
	pass

if __name__ == '__main__':
	run_app(app, host='127.0.0.1', port='80')