"""Generate API v1"""
from typing import Optional
from modules.util import HWC3
from fastapi import (
    UploadFile,
    APIRouter,
    Depends,
    Header,
    Query,
    File
)
from fooocusapi.models.v1.requests import (
    ImgInpaintOrOutpaintRequest,
    ImgUpscaleOrVaryRequest,
    ImgPromptRequest,
    Text2ImgRequest
)
from fooocusapi.models.common.requests import DescribeImageType
from fooocusapi.models.common.response import (
    DescribeImageResponse,
    TaskResponse
)

from fooocusapi.utils.api_utils import (
    img_generate_responses,
    api_key_auth
)
from fooocusapi.utils.img_utils import (
    read_input_image,
    upload_base64
)
from fooocusapi.routes.call_work import call_worker

secure_router = APIRouter(dependencies=[Depends(api_key_auth)])


@secure_router.post(
    path="/v1/generation/text-to-image",
    response_model=TaskResponse,
    responses=img_generate_responses,
    tags=['Generation endpoint V1'])
async def text2img_generation(
        req: Text2ImgRequest,
        accept: str = Header(None),
        accept_query: str | None = Query(
            default=None,
            alias="accept",
            description="Parameter to override 'Accept' header, 'image/png' for output bytes",
        )):
    if accept_query is not None and len(accept_query) > 0:
        accept = accept_query

    return await call_worker(req, accept)


@secure_router.post(
    path="/v1/generation/image-upscale-vary",
    response_model=TaskResponse,
    responses=img_generate_responses,
    tags=['Generation endpoint V1'])
async def img_upscale_or_vary(
        input_image: UploadFile,
        req: ImgUpscaleOrVaryRequest = Depends(ImgUpscaleOrVaryRequest.as_form),
        accept: str = Header(None),
        accept_query: str | None = Query(
            default=None,
            alias="accept",
            description="Parameter to override 'Accept' header, 'image/png' for output bytes",
        )):
    if accept_query is not None and len(accept_query) > 0:
        accept = accept_query

    # Due to the asynchronous nature of UploadFile, it is necessary to convert
    # the UploadFile object to a base64 encoded string in advance
    req.input_image = upload_base64(input_image)

    return await call_worker(req, accept)


@secure_router.post(
    path="/v1/generation/image-inpaint-outpaint",
    response_model=TaskResponse,
    responses=img_generate_responses,
    tags=['Generation endpoint V1'])
async def img_inpaint_or_outpaint(
        input_image: UploadFile,
        input_mask: UploadFile = None,
        req: ImgInpaintOrOutpaintRequest = Depends(ImgInpaintOrOutpaintRequest.as_form),
        accept: str = Header(None),
        accept_query: str | None = Query(
            default=None,
            alias="accept",
            description="Parameter to override 'Accept' header, 'image/png' for output bytes",
        )):
    if accept_query is not None and len(accept_query) > 0:
        accept = accept_query

    req.input_image = upload_base64(input_image)
    req.input_mask = upload_base64(input_mask)

    return await call_worker(req, accept)


@secure_router.post(
    path="/v1/generation/image-prompt",
    response_model=TaskResponse,
    responses=img_generate_responses,
    tags=['Generation endpoint V1'])
async def img_prompt(
        cn_img1: Optional[UploadFile] = File(None),
        req: ImgPromptRequest = Depends(ImgPromptRequest.as_form),
        accept: str = Header(None),
        accept_query: str | None = Query(
            default=None,
            alias="accept",
            description="Parameter to override 'Accept' header, 'image/png' for output bytes",
        )):
    if accept_query is not None and len(accept_query) > 0:
        accept = accept_query

    req.input_image = upload_base64(req.input_image)
    req.input_mask = upload_base64(req.input_mask)

    for i_prompt in req.image_prompts:
        i_prompt.cn_img = upload_base64(i_prompt.cn_img)

    return await call_worker(req, accept)


@secure_router.post(
    path="/v1/tools/describe-image",
    response_model=DescribeImageResponse,
    tags=['Generation endpoint V1'])
def describe_image(
        image: UploadFile,
        task_type: DescribeImageType = Query(
            DescribeImageType.photo, description="Image type, 'Photo' or 'Anime'"
        )):
    """
    Describe image, return text description of image.
    Args:
        image: Image file to be described.
        task_type: Image type, 'Photo' or 'Anime'
    """
    if task_type == DescribeImageType.photo:
        from extras.interrogate import default_interrogator as default_interrogator_photo

        interrogator = default_interrogator_photo
    else:
        from extras.wd14tagger import default_interrogator as default_interrogator_anime

        interrogator = default_interrogator_anime

    img = HWC3(read_input_image(image))
    result = interrogator(img)
    return DescribeImageResponse(describe=result)
