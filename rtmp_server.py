import os
import asyncio
import tempfile

from pyrtmp import StreamClosedException, RTMPProtocol
from pyrtmp.messages import SessionManager
from pyrtmp.messages.audio import AudioMessage
from pyrtmp.messages.command import NCConnect, NCCreateStream, NSPublish, NSCloseStream, NSDeleteStream
from pyrtmp.messages.data import MetaDataMessage
from pyrtmp.messages.protocolcontrol import WindowAcknowledgementSize, SetChunkSize, SetPeerBandwidth
from pyrtmp.messages.usercontrol import StreamBegin
from pyrtmp.messages.video import VideoMessage
from pyrtmp.misc.flvdump import FLVFile, FLVMediaType


async def simple_controller(reader, writer):
	session = SessionManager(reader=reader, writer=writer)
	flv = None
	try:
		# do handshake
		await session.handshake()

		# read chunks
		async for chunk in session.read_chunks_from_stream():
			message = chunk.as_message()
			if isinstance(message, NCConnect):
				session.write_chunk_to_stream(
					WindowAcknowledgementSize(ack_window_size=5000000))
				session.write_chunk_to_stream(SetPeerBandwidth(
					ack_window_size=5000000, limit_type=2))
				session.write_chunk_to_stream(StreamBegin(stream_id=0))
				session.write_chunk_to_stream(SetChunkSize(chunk_size=8192))
				session.writer_chunk_size = 8192
				session.write_chunk_to_stream(message.create_response())
				await session.drain()
			elif isinstance(message, WindowAcknowledgementSize):
				pass
			elif isinstance(message, NCCreateStream):
				session.write_chunk_to_stream(message.create_response())
				await session.drain()
			elif isinstance(message, NSPublish):
				# create flv file at temp
				flv = FLVFile(os.path.join(
					tempfile.gettempdir(), message.publishing_name))
				session.write_chunk_to_stream(StreamBegin(stream_id=1))
				session.write_chunk_to_stream(message.create_response())
				await session.drain()
			elif isinstance(message, MetaDataMessage):
				# Write meta data to file
				flv.write(0, message.to_raw_meta(), FLVMediaType.OBJECT)
			elif isinstance(message, SetChunkSize):
				session.reader_chunk_size = message.chunk_size
			elif isinstance(message, VideoMessage):
				# Write video data to file
				flv.write(message.timestamp, message.payload,
						FLVMediaType.VIDEO)
			elif isinstance(message, AudioMessage):
				# Write data data to file
				flv.write(message.timestamp, message.payload,
						FLVMediaType.AUDIO)
			elif isinstance(message, NSCloseStream):
				pass
			elif isinstance(message, NSDeleteStream):
				pass
	except StreamClosedException:
		pass
	finally:
		if flv:
			flv.close()


async def serve_rtmp(use_protocol:bool=True, host:str='localhost', port:int=1935):
	loop = asyncio.get_running_loop()
	if use_protocol:
		server = await loop.create_server(lambda: RTMPProtocol(controller=simple_controller, loop=loop), host, port)
	else:
		server = await asyncio.start_server(simple_controller, host, port)
	addr = server.sockets[0].getsockname()
	print(f' Listening RTMP server on {addr} '.center(9, fillchar='-'))
	async with server:
		await server.serve_forever()