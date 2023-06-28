from typing import Callable, Any
import asyncio

from textual.app import App
from textual.widgets import TextLog


async def run_process(*args, print_function: Callable[[str], Any]):
    proc = await asyncio.create_subprocess_exec(*args, stdout=asyncio.subprocess.PIPE)
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


def gui_counter():
    app = CounterApp()
    app.run()
