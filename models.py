from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Users(models.Model):
    id = fields.IntField(pk=True, unique=True)
    user_id = fields.IntField(unique=True)
    name = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=80)
    gender = fields.CharField(max_length=15)
    status = fields.CharField(max_length=10)


class Posts(models.Model):
    id = fields.IntField(pk=True)
    post_id = fields.IntField(unique=True)
    user_id = fields.IntField()
    title = fields.CharField(max_length=250)
    body = fields.TextField()


User_Pydantic = pydantic_model_creator(Users, name="User")
UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)

Posts_Pydantic = pydantic_model_creator(Posts, name="Posts")
PostsIn_Pydantic = pydantic_model_creator(Posts, name="PostsIn", exclude_readonly=True)