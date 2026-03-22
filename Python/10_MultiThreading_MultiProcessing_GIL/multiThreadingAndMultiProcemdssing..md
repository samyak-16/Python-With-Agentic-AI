Multi Threading:
┌─────────────────────────────────┐
│     ONE Python Interpreter      │
│     ONE GIL                     │
│                                 │
│  Thread 1 ┐                     │
│  Thread 2 ┤  fight for ONE GIL  │
│  Thread 3 ┘                     │
└─────────────────────────────────┘
only 1 runs at a time

Multi Processing:
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Interpreter 1│  │ Interpreter 2│  │ Interpreter 3│
│ OWN GIL      │  │ OWN GIL      │  │ OWN GIL      │
│ Process 1    │  │ Process 2    │  │ Process 3    │
└──────────────┘  └──────────────┘  └──────────────┘
     Core 1            Core 2            Core 3
   running ✅        running ✅        running ✅



Cores           →  physical hardware, actual execution
Threads         →  software, sequence of tasks
Context Switch  →  OS illusion of parallelism
GIL             →  one thread runs Python at a time
                   but switches mid-operation
Race Condition  →  corruption from mid-operation switching
Lock / Mutex    →  protect your own data, atomic operations
Multiprocessing →  escape GIL, own interpreter per process
Child Process   →  isolated Python copy, own memory, own GIL
I/O Bound       →  waiting for external things, GIL releases
CPU Bound       →  pure computation, GIL hurts, use multiprocess