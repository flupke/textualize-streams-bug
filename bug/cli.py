import asyncio


async def run_process(*args):
    proc = await asyncio.create_subprocess_exec(*args, stdout=asyncio.subprocess.PIPE)
    if proc.stdout is not None:
        async for line in proc.stdout:
            print(line.decode().strip())


def counter():
    asyncio.run(run_process("python", "counter.py"))
