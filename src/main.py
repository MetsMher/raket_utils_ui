from fastapi import FastAPI, APIRouter

import src.api.routes.gitlab_route as gl_route


app = FastAPI(debug=True)

v1 = APIRouter(prefix='/v1', tags=['v1'])
v1.include_router(gl_route.router)

app.include_router(v1)

