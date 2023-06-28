from typing import Callable, Any
import asyncio

import aiohttp
import aiohttp.client_exceptions
from textual.app import App
from textual.widgets import TextLog


PrintFunction = Callable[[str], Any]


async def run_process(*args, print_function: PrintFunction, cwd=None):
    proc = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, cwd=cwd
    )
    if proc.stdout is not None:
        async for line in proc.stdout:
            print_function(line.decode().strip())


def counter():
    asyncio.run(run_process("python", "counter.py", print_function=print))


class CounterApp(App):
    def compose(self):
        yield TextLog()

    def on_ready(self):
        view = self.query_one(TextLog)
        self.run_worker(run_process("python", "counter.py", print_function=view.write))


def counter_gui():
    app = CounterApp()
    app.run()


async def run_phoenix(print_function: PrintFunction):
    await run_process(
        "mix", "deps.get", print_function=print_function, cwd="phoenix_app"
    )
    await run_process(
        "mix", "assets.setup", print_function=print_function, cwd="phoenix_app"
    )
    await run_process(
        "mix", "phx.server", print_function=print_function, cwd="phoenix_app"
    )


async def run_poller(print_function: PrintFunction):
    timeout = aiohttp.ClientTimeout(total=1)
    while True:
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                while True:
                    async with session.get("http://localhost:4000") as response:
                        status = response.status
                        print_function(f"--- Got reply: {status}")
                        await asyncio.sleep(1)
        except aiohttp.client_exceptions.ClientConnectorError:
            print_function("Server not ready, retrying...")
            await asyncio.sleep(1)
        except asyncio.TimeoutError:
            print_function("Timeout, retrying...")


async def do_phoenix():
    await asyncio.gather(*(run_phoenix(print), run_poller(print)))


def phoenix():
    asyncio.run(do_phoenix())


class PhoenixApp(App):
    def compose(self):
        yield TextLog()

    def on_ready(self):
        view = self.query_one(TextLog)
        self.run_worker(run_phoenix(view.write))
        self.run_worker(run_poller(view.write))


def phoenix_gui():
    app = PhoenixApp()
    app.run()
