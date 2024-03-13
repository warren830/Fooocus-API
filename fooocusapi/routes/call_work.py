import asyncio
import os

from fastapi import Response

from fooocusapi.models.common.base import CommonRequest as Text2ImgRequest
from fooocusapi.models.common.response import TaskResponse
from fooocusapi.tasks.task import TaskObj
from fooocusapi.tasks.task_queue import task_queue
from fooocusapi.utils.file_utils import output_dir


async def call_worker(req: Text2ImgRequest,
                      accept: str) -> Response | TaskResponse:
    """
    Call worker to generate image
    Args:
        req: Text2ImgRequest, or other object inherit CommonRequest
        accept: accept header
    returns: Response or TaskResponse
    """
    if accept == "image/png":
        streaming_output = True
        # image_number auto set to 1 in streaming mode
        req.image_number = 1
    else:
        streaming_output = False

    task = TaskObj(req_params=req)
    await task_queue.add_task(task=task)

    # if Accept is image/png, return image by bytes
    if streaming_output:
        while True:
            await asyncio.sleep(1)
            if task.task_status == 'success':
                try:
                    filename = task.task_result[0].url.split('/')[-1]
                    filedir = task.task_result[0].url.split('/')[-2]
                    file_path = os.path.join(
                        output_dir,
                        filedir,
                        filename
                    )
                    image_bytes = open(file_path, 'rb').read()
                    return Response(
                        image_bytes,
                        media_type="image/png",
                    )
                except IndexError:
                    return Response(status_code=500, content="Internal Server Error")
            if task.task_status in ['failed', 'canceled']:
                return task.to_dict()

    # waiting for task finish, if async_process is false
    if not req.async_process:
        while True:
            print("waiting for sync task")
            await asyncio.sleep(1)
            print(task.task_status)
            if task.task_status is not None:
                return task.to_dict()
    return task.to_dict()
