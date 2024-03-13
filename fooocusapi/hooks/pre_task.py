"""
Function will be running before task start
request params is a req.params object, and you must return a req.params object
"""


async def pre_task(request):
    print(request)
    return request
