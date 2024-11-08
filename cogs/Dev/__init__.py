from ganyu_utils import setup_logging

logger = setup_logging()

logger.info("Dev commands are loaded.")


async def setup(bot):
    return