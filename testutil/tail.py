import asyncio
import re

from typing import AsyncGenerator, Optional

SCAN_INTERVAL = 1.0


async def tailfind(file: str, pattern=".*", from_start=False) -> AsyncGenerator[re.Match, None]:
    with open(file, 'r') as f:
        if not from_start:
            f.seek(0, 2)
        while True:
            lines = f.readlines()
            for line in lines:
                m = re.match(pattern, line)
                if m:
                    yield m
            await asyncio.sleep(SCAN_INTERVAL)
