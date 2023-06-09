
import asyncio
import io

from PIL import Image
from aio_pika import connect, IncomingMessage, Message

from torchvision import transforms
import model.util as util
from bot.image_handlers import get_bytearray
from util.config import __CONFIG__

model_original, model_self_trained, model_antiblur = util.load_models()
model_original.eval()
model_self_trained.eval()
model_antiblur.eval()

channel = None


async def on_message(message: IncomingMessage):
    netG = None
    if message.headers['model'] == 'original':
        netG = model_original
    elif message.headers['model'] == 'antiblur':
        netG = model_antiblur
    else:
        netG = model_self_trained

    image = Image.open(io.BytesIO(message.body))
    lr = transforms.ToTensor()(image).unsqueeze(0)
    fake = netG(lr).clamp_(0., 1)
    image = transforms.ToPILImage(mode='RGB')(fake[0])
    await channel.default_exchange.publish(
        Message(get_bytearray(image), headers={'user_id': message.headers['user_id'],
                                               'model': message.headers['model']}),
        routing_key='result'
    )


async def main(loop):
    global channel
    # Perform connection
    connection = await connect(
        f"amqp://{__CONFIG__['mq_addr']}/", loop=loop
    )

    # Creating a channel
    channel = await connection.channel()

    # Declaring queue
    queue = await channel.declare_queue("process")

    await queue.consume(on_message, no_ack=True)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main(loop))

    # we enter a never-ending loop that waits for data and
    # runs callbacks whenever necessary.
    print(" [*] Waiting for messages. To exit press CTRL+C")
    loop.run_forever()
