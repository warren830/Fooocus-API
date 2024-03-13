"""Generate API V2"""
from typing import List
from fastapi import APIRouter, Depends, Header, Query
from fooocusapi.models.common.response import TaskResponse

from fooocusapi.models.v2.request import (
    ImgInpaintOrOutpaintRequestJson,
    ImgPromptRequestJson,
    ImgUpscaleOrVaryRequestJson,
    Text2ImgRequestWithPrompt,
    ImagePromptJson
)
from fooocusapi.routes.call_work import call_worker
from fooocusapi.utils.api_utils import (
    img_generate_responses,
    api_key_auth,
)

secure_router = APIRouter(dependencies=[Depends(api_key_auth)])


@secure_router.post(
    path="/v2/generation/text-to-image-with-ip",
    response_model=TaskResponse,
    responses=img_generate_responses,
    tags=['Generation endpoint V2']
)
async def text_to_img_with_ip(
        req: Text2ImgRequestWithPrompt,
        accept: str = Header(None),
        accept_query: str | None = Query(
            default=None,
            alias="accept",
            description="Parameter to override 'Accept' header, 'image/png' for output bytes",
        )):
    """Generate image from text prompt"""
    if accept_query is not None and len(accept_query) > 0:
        accept = accept_query

    default_image_prompt = ImagePromptJson(cn_img=None)
    image_prompts_files: List[ImagePromptJson] = []
    for img_prompt in req.image_prompts:
        image = ImagePromptJson(
            cn_img=img_prompt.cn_img,
            cn_stop=img_prompt.cn_stop,
            cn_weight=img_prompt.cn_weight,
            cn_type=img_prompt.cn_type,
        )
        image_prompts_files.append(image)

    while len(image_prompts_files) < 4:
        image_prompts_files.append(default_image_prompt)

    req.image_prompts = image_prompts_files

    return call_worker(req, accept)


@secure_router.post(
    path="/v2/generation/image-upscale-vary",
    response_model=TaskResponse,
    responses=img_generate_responses,
    tags=['Generation endpoint V2']
)
def img_upscale_or_vary_v2(
        req: ImgUpscaleOrVaryRequestJson,
        accept: str = Header(None),
        accept_query: str | None = Query(
            default=None,
            alias="accept",
            description="Parameter to override 'Accept' header, 'image/png' for output bytes",
        )):
    """Generate image from text prompt"""
    if accept_query is not None and len(accept_query) > 0:
        accept = accept_query

    default_image_prompt = ImagePromptJson(cn_img=None)
    image_prompts_files: List[ImagePromptJson] = []
    for img_prompt in req.image_prompts:
        image = ImagePromptJson(
            cn_img=img_prompt.cn_img,
            cn_stop=img_prompt.cn_stop,
            cn_weight=img_prompt.cn_weight,
            cn_type=img_prompt.cn_type,
        )
        image_prompts_files.append(image)
    while len(image_prompts_files) < 4:
        image_prompts_files.append(default_image_prompt)
    req.image_prompts = image_prompts_files

    return call_worker(req, accept)


@secure_router.post(
    path="/v2/generation/image-inpaint-outpaint",
    response_model=TaskResponse,
    responses=img_generate_responses,
    tags=['Generation endpoint V2']
)
def img_inpaint_or_outpaint_v2(
        req: ImgInpaintOrOutpaintRequestJson,
        accept: str = Header(None),
        accept_query: str | None = Query(
            default=None,
            alias="accept",
            description="Parameter to override 'Accept' header, 'image/png' for output bytes",
        )):
    """Inpaint or outpaint image"""
    if accept_query is not None and len(accept_query) > 0:
        accept = accept_query

    default_image_prompt = ImagePromptJson(cn_img=None)
    image_prompts_files: List[ImagePromptJson] = []
    for img_prompt in req.image_prompts:
        image = ImagePromptJson(
            cn_img=img_prompt.cn_img,
            cn_stop=img_prompt.cn_stop,
            cn_weight=img_prompt.cn_weight,
            cn_type=img_prompt.cn_type,
        )
        image_prompts_files.append(image)
    while len(image_prompts_files) < 4:
        image_prompts_files.append(default_image_prompt)
    req.image_prompts = image_prompts_files

    return call_worker(req, accept)


@secure_router.post(
    path="/v2/generation/image-prompt",
    response_model=TaskResponse,
    responses=img_generate_responses,
    tags=['Generation endpoint V2']
)
async def img_prompt_v2(
        req: ImgPromptRequestJson,
        accept: str = Header(None),
        accept_query: str | None = Query(
            default=None,
            alias="accept",
            description="Parameter to override 'Accept' header, 'image/png' for output bytes",
        )):
    """Image prompt"""
    if accept_query is not None and len(accept_query) > 0:
        accept = accept_query

    default_image_prompt = ImagePromptJson(cn_img=None)
    image_prompts_files: List[ImagePromptJson] = []
    for img_prompt in req.image_prompts:
        image = ImagePromptJson(
            cn_img=img_prompt.cn_img,
            cn_stop=img_prompt.cn_stop,
            cn_weight=img_prompt.cn_weight,
            cn_type=img_prompt.cn_type,
        )
        image_prompts_files.append(image)

    while len(image_prompts_files) < 4:
        image_prompts_files.append(default_image_prompt)

    req.image_prompts = image_prompts_files

    return await call_worker(req, accept)
