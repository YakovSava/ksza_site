from os import getcwd
from os.path import join
from aiofiles import open as aiopen
# from plugins.downoloader import Downoloader

class Binder:

	def __init__(self, path:str='html/'):
		self._path = path
		# self._downoload = downoloader

	async def _get_string(self, filename:str='') -> str:
		async with aiopen(join(self._path, filename), 'r', encoding='utf-8') as file:
			return await file.read()

	async def _get_bytes(self, filename:str='') -> bytes:
		async with aiopen(join(self._path, filename), 'rb') as file:
			return await file.read()
	
	async def _set_string(self, filename:str='', lines:str='') -> None:
		# self._downoload.write(join(getcwd(), self._path, filename), lines)
		async with aiopen(join(self._path, filename), 'w', encoding='utf-8') as file:
			await file.write(liens)

	async def _set_bytes(self, filename:str='', byte:bytes=b'') -> None:
		async with aiopen(join(self._path, filename), 'wb') as file:
			await file.write(byte)
	
	async def _get_object(self, object_filename:str='') -> tuple[bool, dict]:
		try:
			obj = await self._get_string(filename=object_filename)
			return (True, {
				'status': 200,
				'body': obj,
				'content_type': 'text/plain'
			})
		except:
			return (False, {
				'status': 404,
				'body': 'error',
				'content_type': 'text/plain'
			})

	async def _get_bytes_object(self, object_filename:str='') -> tuple[bool, dict]:
		try:
			obj = await self._get_bytes(filename=object_filename)
			return (True, {
				'status': 200,
				'body': obj,
				'content_type': 'text/plain'
			})
		except:
			return (False, {
				'status': 404,
				'body': 'error',
				'content_type': 'text/plain'
			})

	async def get_js(self, path:str='') -> dict:
		status, obj = await self._get_object(object_filename=path)
		if status:
			obj['content_type'] = 'text/javascript'
			return obj
		else:
			obj['status'] = 404
			return obj

	async def get_css(self, path:str='') -> dict:
		status, obj = await self._get_object(object_filename=path)
		if status:
			if path.endswith('.css'):
				obj['content_type'] = 'text/css'
			else:
				obj['content_type'] = 'text/plain'
			return obj
		else:
			obj['status'] = 404
			return obj

	async def get_svg(self, path:str='') -> dict:
		status, obj = await self._get_object(object_filename=path)
		if status:
			obj['content_type'] = 'image/svg+xml'
			return obj
		else:
			obj['status'] = 404
			return obj

	async def get_png(self, path:str='') -> dict:
		status, obj = await self._get_bytes_object(object_filename=path)
		if status:
			obj['content_type'] = 'image/png'
			return obj
		else:
			obj['status'] = 404
			return obj

	async def get_html(self, filename:str='') -> dict:
		status, obj = await self._get_object(object_filename=filename)
		if status:
			obj['content_type'] = 'text/html'
			return obj
		else:
			obj['status'] = 404
			return obj

	async def get_columns(self):
		async with aiopen('columns.pylist', 'r', encoding='utf-8') as file:
			lines = await file.read()
		return eval(lines)

	async def change_pylist(self, data:dict={'columns': [[1, 'Title', 'Description']]}):
		pass