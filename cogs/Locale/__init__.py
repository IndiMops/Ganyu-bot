from ganyu_utils import setup_logging
from discord import app_commands

logger = setup_logging()

logger.info("Locale commands are loaded.")

async def setup(bot):
    return