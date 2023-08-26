import httpx
import tortoise.exceptions
from fastapi import FastAPI
from models import User_Pydantic, Users, Posts_Pydantic, Posts

from tortoise.contrib.fastapi import register_tortoise

app = FastAPI(title="DataBase users and posts")


@app.get("/upload-db")
async def update_users():
    async with httpx.AsyncClient() as client:
        for page_number in range(1, 5):
            response_users = await client.get(f"https://gorest.co.in/public/v2/users?page={page_number}&per_page=100")
            response_users = response_users.json()
            for user in response_users:
                new_user = Users(user_id=user["id"],
                                 name=user["name"],
                                 email=user["email"],
                                 gender=user["gender"],
                                 status=user["status"],
                                 )
                try:
                    await new_user.save()
                except tortoise.exceptions.IntegrityError:
                    continue

        for page_number in range(1, 10):
            response_posts = await client.get(f"https://gorest.co.in/public/v2/posts?page={page_number}&per_page=100")
            response_posts = response_posts.json()
            for post in response_posts:
                new_post = Posts(post_id=post["id"],
                                 title=post["title"],
                                 body=post["body"],
                                 user_id=post["user_id"],
                                 )
                try:
                    await new_post.save()
                except tortoise.exceptions.IntegrityError:
                    continue

    return {"message": "successfully updated"}


@app.get("/users")
async def get_users():
    users_list = await User_Pydantic.from_queryset(Users.all())
    if users_list:
        return users_list
    else:
        return {"message": "DataBase is empty, please, update it with http://127.0.0.1:8000/upload-db"}


@app.get("/user/{user_id}", response_model=User_Pydantic)
async def get_user(user_id: int):
    return await User_Pydantic.from_queryset_single(Users.get(user_id=user_id))


@app.get("/user/{user_id}/posts")
async def get_posts(user_id: int):
    posts = await Posts_Pydantic.from_queryset(Posts.filter(user_id=user_id))
    if posts:
        return posts
    else:
        return {"message": "This user didn't create any posts"}

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
