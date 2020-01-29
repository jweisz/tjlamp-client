#!/usr/bin/env python3

import os
import sys
import asyncio

class Foo():
    def __init__(self):
        self.task = None
    
    def runTask(self, func):
        # cancel any existing task
        self.cancelTask()
    
        # fire up the new task
        self.task = asyncio.create_task(func)
    
    async def cancelTask(self):
        if not self.task is None:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
    
    def greet(self):
        async def _greet():
            n = 0
            try:
                while True:
                    print(f"hello world {n}")
                    n = n + 1
                    await asyncio.sleep(1)
            except asyncio.CancelledError:
                print(f"goodbye world {n}")
            finally:
                print(f"i'm outta here")
        self.runTask(_greet())

async def greet_every_two_seconds():
    n = 0
    try:
        while True:
            print(f'Hello World {n}')
            n = n + 1
            await asyncio.sleep(2)
    except asyncio.CancelledError:
        print(f"Goodbye world! {n}")
    finally:
        print(f"It's been a good time.")

async def main():
    print("creating asyncio task")
    task = asyncio.create_task(greet_every_two_seconds())
    print("sleeping for 10 seconds")
    await asyncio.sleep(10)
    print("killing task")
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("main(): task has been cancelled")

async def main2():
    print("creating Foo")
    foo = Foo()
    print("calling Foo greet()")
    foo.greet()
    print("sleeping for 5 sec")
    await asyncio.sleep(5)
    print("running another greet()")
    foo.greet()
    print("sleeping another 5 sec")
    await asyncio.sleep(5)
    print("all done")
    await foo.cancelTask()
    print("dead")

# Main program logic follows:
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main2())
