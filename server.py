from json import loads
from aiohttp.web import Application, run_app, RouteTableDef, Response, Request, json_response
from plugins.binder import Binder
from static import app as subapp

routes = RouteTableDef()
app = Application()
binder = Binder()

app.add_subapp('/', subapp)


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


if __name__ == '__main__':
	run_app(app, host='192.168.100.2', port='80')
