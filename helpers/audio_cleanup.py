import os
import asyncio
from .logger import logger

async def delete_file(path: str, delay: int = 10):
    """Delete file after specified delay in seconds"""
    await asyncio.sleep(delay)
    if os.path.exists(path):
        os.remove(path)
        logger.info(f"Deleted file: {path}")