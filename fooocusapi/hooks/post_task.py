"""
Function will be running after generate finished
request params is a task object
return is useless, task queue do not receive it
"""


async def post_task(request):
    print(request)
    return request
