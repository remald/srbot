import asyncio
import logging

from bot.bot import run_bot
from util.mq import run_mq

# Configure logging
logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_mq(loop))
    run_bot(loop)
