from fastapi import APIRouter
from pyexpat.errors import messages

from starlette.responses import JSONResponse

from enum import Enum

from typing import Literal

from pydantic import BaseModel, Field

from src.services.gitlab_service import GitlabUtil

router = APIRouter(prefix='/gitlab', tags=['gitlab'])

# class Languages(Enum):
#     python='python'
#     go='go'
#     java='java'


class GitlabCreateSchema(BaseModel):
    token: str = Field(max_length=32)
    name: str = Field(min_length=3, max_length=9)
    language: Literal['python', 'go', 'java']


class GitLabDeleteSchema(BaseModel):
    token: str = Field(max_length=32)
    name: str = Field(min_length=3, max_length=9)


@router.post('/create')
async def create_repo(pyload: GitlabCreateSchema):
    token = pyload.token
    name = pyload.name
    language = pyload.language
    try:
        util = GitlabUtil(
            token=token,
            name=name,
            language=language
        )
        util.auth()
        util.create_project()
        with util.managed_project():
            util.protected_branches_project()
            util.add_base_files_for_project()
            util.add_branches_project()
            util.get_project_info()
            return JSONResponse({"message": "Repo is created"}, status_code=201)
    except Exception:
        return JSONResponse({"message": "Something went wrong"}, status_code=400)


@router.post('/delete')
async def delete_repo(pyload: GitLabDeleteSchema):
    token = pyload.token
    name = pyload.name

    try:
        util = GitlabUtil(
            name=name,
            token=token
        )
        util.auth()
        with util.managed_project():
            util.delete_project()
            return JSONResponse({"message": "Repo is deleted successfully"}, status_code=200)
    except Exception:
        return JSONResponse({"message": "Something went wrong"}, status_code=400)
