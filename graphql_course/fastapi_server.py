from fastapi import FastAPI
import uvicorn

from graphql_schema import schema
from starlette_graphene3 import make_playground_handler, GraphQLApp

app = FastAPI()


app.mount(
    "/graphql",
    GraphQLApp(
        schema,
        on_get=make_playground_handler(
            playground_options={
                "endpoint": "/graphql",
                "title": "GraphQL Playground",
                "subscriptionEndpoint": "/graphql",
            }
        ),
    ),
)

# @app.post("/graphql")
# async def graphql_endpoint(request: Request):
#     payload = await request.json()
#     result = schema.execute(
#         payload.get("query"),
#         variables=payload.get("variables"),
#         operation_name=payload.get("operationName"),
#     )
#     response = {}
#     if result.errors:
#         response["errors"] = [str(e) for e in result.errors]
#     if result.data is not None:
#         response["data"] = result.data
#     return JSONResponse(response)


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run("fastapi_server:app", reload=True)
