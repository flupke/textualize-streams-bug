# Reproduction for stuck subprocess bug

## Installation

1. Install [poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
2. Install [asdf](https://asdf-vm.com/guide/getting-started.html)
3. Run `make install`

## To reproduce the bug

The bug can be reproduced by running `make`, which:

1. Builds a [Phoenix](https://www.phoenixframework.org/) application (`mix` is
   one of the processes sensible to this bug, but I have seen it happen with
   `nodemon` too)
2. Starts the Phoenix server
3. Retrieves the server /index.html page every second

To trigger the bug, hover the mouse over the Textualize app, you should
immediately see timeouts in the output. If you look at the process with htop,
you also see its state go from S (sleeping) to T (traced/stopped)

The bug is introduced by this change (everything works fine witouth piping +
os.setpgrp):

```diff
diff --git a/bug/cli.py b/bug/cli.py
index bd6619a..41bb82b 100644
--- a/bug/cli.py
+++ b/bug/cli.py
@@ -1,3 +1,4 @@
+import os
 from typing import Callable, Any
 import asyncio
 
@@ -12,7 +13,11 @@
 
 async def run_process(*args, print_function: PrintFunction, cwd=None):
     proc = await asyncio.create_subprocess_exec(
-        *args, stdout=asyncio.subprocess.PIPE, cwd=cwd
+        *args,
+        stdout=asyncio.subprocess.PIPE,
+        stderr=asyncio.subprocess.STDOUT,
+        cwd=cwd,
+        preexec_fn=os.setpgrp,
     )
     if proc.stdout is not None:
         async for line in proc.stdout:
```

You can also run the non-gui version to check the issue only happens when
running under Textualize.
