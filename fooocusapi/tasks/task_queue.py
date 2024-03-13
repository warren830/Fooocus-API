"""Define task queue object"""
import asyncio
import time

from fooocusapi.utils.logger import default_logger
from fooocusapi.tasks.task import TaskObj


class TaskQueue:
    """任务队列"""
    def __init__(self, queue_size: int):
        self.queue_size = queue_size
        self.queue = asyncio.Queue(queue_size)
        self.current = None
        self.history = []
        self.lock = asyncio.Lock()
        self.semaphore = asyncio.Semaphore(1)

    async def add_task(self, task: TaskObj):
        """添加任务到队列"""
        if self.queue.full():
            default_logger.std_error("[TaskQueue] Task queue is full")
            return
        await task.pre_task()
        await self.queue.put(task)
        default_logger.std_info(f"[TaskQueue] Task {task.task_id} added to queue")
        return task.to_dict()

    async def process_tasks(self):
        """处理队列中的任务"""
        last_print_time = int(time.time())
        while True:
            if self.queue.empty():
                await asyncio.sleep(1)
                if int(time.time()) - last_print_time >= 300:
                    default_logger.std_info("[TaskQueue] Idle, waiting for the task...")
                    last_print_time = int(time.time())
                continue
            if self.current is not None:
                if self.current.task_status is not None:
                    self.current = None
                    continue
                await asyncio.sleep(1)
                default_logger.std_info(f"[TaskQueue] {self.current.task_id} running...")
                continue
            async with self.semaphore:
                self.current = await self.queue.get()
                default_logger.std_info(f"[TaskQueue] Start processing task {self.current.task_id}")
                self.current.update('status', 'running')
                await asyncio.create_task(self.current.run())
                self.history.append(self.current)
                await self.current.post_task()


task_queue = TaskQueue(100)
