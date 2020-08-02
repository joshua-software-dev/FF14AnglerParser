#! /usr/bin/env python3

import asyncio


class DelayOnReleaseLock:

    def __init__(self, pause_duration: int):
        self._pause_duration: int = pause_duration
        self._lock: asyncio.Lock = asyncio.Lock()

    async def __aenter__(self):
        await self._lock.acquire()

    async def __aexit__(self, exc_type, exc, tb):
        await asyncio.sleep(self._pause_duration)
        self._lock.release()
