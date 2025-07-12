import os
import asyncio

async def delete_file(path: str, delay: int = 10):
    """Delete file after specified delay in seconds"""
    await asyncio.sleep(delay)
    if os.path.exists(path):
        os.remove(path)
        print(f"Deleted file: {path}")