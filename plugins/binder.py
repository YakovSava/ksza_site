import asyncio

from os.path import exists
from aiofiles import open as aiopen

class Binder:

	def __init__(self, path:str='html/'):
		self._path = path

	async def _get_string(self, filename:str='') -> str:
		async with aiopen(filename, 'r', encoding='utf-8') as file:
			return await file.read()

	async def _get_bytes(self, filename:str='') -> bytes:
		async with aiopen(filename, 'rb') as file:
			return await file.read()
	
	async def _set_string(self, filename:str='', lines:str='') -> None:
		async with aiopen(filename, 'r', encoding='utf-8') as file:
			await file.write(lines)

	async def _set_bytes(self, filename:str='', byte:bytes=b'') -> None:
		async with aiopen(filename, 'wb') as file:
			await file.write(byte)
	
	async def _get_object(self, object_filename:str='') -> tuple[bool, dict]:
		try:
			obj = await self._get_object(filename=object_filename)
			return (True, {
				'status': 200,
				'body': obj
			})
		except:
			return (False, {
				'status': 404
			})

	async def _get_bytes_object(self, object_filename:str='') -> tuple[bool, dict]:
		try:
			obj = await self._get_bytes(filename=object_filename)
			return (True, {
				'status': 200,
				'body': obj
			})
		except:
			return (False, {
				'status': 404
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
			obj['content_type'] = 'text/css'
			return obj
		else:
			obj['status'] = 404
			return obj

	async def get_svg(self, path:str='') -> dict:
		status, obj = await self._get_bytes_object(object_filename=path)
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