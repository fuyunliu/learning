"""
模型：
1，单线程同步模型，可阻塞
2，多线程模型，但是由于python解释器的GIL(全局解释器锁)，任何Python线程执行前，
必须先获得GIL锁才能执行，执行完成后，解释器就自动释放GIL锁，让别的线程有机会执行。
这个GIL全局锁实际上把所有线程的执行代码都给上了锁，所以，多线程在Python中只能交替执行
3，单线程异步模型，与同步模型相比，异步模型的优势在如下情况下会得到发挥：
    (1)有大量的任务，以至于可以认为在一个时刻至少有一个任务要运行，
    (2)任务执行大量的I/O操作，这样同步模型就会在因为任务阻塞而浪费大量的时间，
    (3)任务之间相互独立，以至于任务内部的交互很少。




"""
