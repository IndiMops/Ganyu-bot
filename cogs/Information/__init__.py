from ganyu_utils import setup_logging

logger = setup_logging()

logger.info("Information commands are loaded.")


async def setup(bot):
    return