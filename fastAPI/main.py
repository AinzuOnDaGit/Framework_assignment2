from fastapi import FastAPI, Request
from pydantic import BaseModel


app = FastAPI()

# simulated database, storing posts
posts = []


# define what each post will contain, image_url instead of image within a database
class Post(BaseModel):
    title: str
    description: str
    image_url: str | None = None

# when retrieving posts (/posts) return the most recent three
@app.get("/blog_posts")
def retrieve_posts():
    return posts[-3:]

# when sending data to posts, check it matches the Post model class, if so append
@app.post("/blog_posts")
def create_blog_post(post: Post):
    posts.append(post)
    # successful creation message
    return {"message": "Post Created", "post": post}

#simulate searching for posts with a query, convert querys to lower to avoid missing capital configurations
@app.get("/blog_posts/search")
def search_blog_posts(query: str):
    return [i for i in posts if query.lower() in i.title.lower() or query.lower() in i.description.lower()]

