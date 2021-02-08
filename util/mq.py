import io

from aio_pika import IncomingMessage, connect, Message

from bot import image_handlers
from util.config import __CONFIG__
from util.liveOptions import __LIVE_OPTIONS__

mq_chan = None


async def get_result(message: IncomingMessage):
    bio = io.BytesIO(message.body)
    bio.seek(0)
    bio.name = 'uncompressed.png'
    await image_handlers.send_bytes(message.headers['user_id'], bio)


async def publish_bytes(data, user_id, model):
    await mq_chan.default_exchange.publish(
        Message(data, headers={'user_id': user_id,
                               'model': model}),
        routing_key='process')


async def run_mq(loop):
    global mq_chan

    mq_conn = await connect(
        f"amqp://{__CONFIG__['mq_addr']}/", loop=loop
    )
    # Creating a channel
    mq_chan = await mq_conn.channel()

    # Declaring queue
    queue = await mq_chan.declare_queue("result")

    await queue.consume(get_result, no_ack=True)
