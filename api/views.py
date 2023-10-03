from typing import List
from http import HTTPStatus
from fastapi import APIRouter, Path, HTTPException

from api.models import PostDB, PostSchema
from api.utils import get_all_posts, create_post, get_single_post, update_post, delete_post

router = APIRouter()


@router.post("/", response_model=PostDB, status_code=HTTPStatus.CREATED)
async def create_post_view(payload: PostSchema):
    post_id = await create_post(payload)

    response_object = {
        "id": post_id,
        "title": payload.title,
        "description": payload.description,
        "created_by": payload.created_by,
    }
    return response_object


@router.get('/', response_model=List[PostDB])
async def read_all_posts_view():
    return await get_all_posts()


@router.get('/{id}/', response_model=PostDB)
async def read_single_post_view(id: int = Path(..., gt=0)):
    post = await get_single_post(id)
    if not post:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='Post not found')
    return post


@router.put('/{id}/', response_model=PostDB)
async def update_single_post(payload: PostSchema, id: int = Path(..., gt=0)):
    post = await get_single_post(id)
    if not post:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='Post not found')
    post_id = await update_post(id=id, payload=payload)
    response_object = {
        "id": post_id,
        "title": payload.title,
        "description": payload.description,
        "created_by": payload.created_by,
    }
    return response_object


@router.delete('/{id}/', response_model=PostDB)
async def delete_single_post_view(id: int = Path(..., gt=0)):
    post = await get_single_post(id)
    if not post:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='Post not found')
    await delete_post(id)
    return post
