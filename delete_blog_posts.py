import os
import json
import logging
import requests

import azure.functions as func

### Please provide needed URL and KEY below ###

GHOST_API_URL = os.environ['GHOST_API_URL']
GHOST_API_KEY = os.environ['GHOST_API_KEY']

def delete_all_posts():
    headers = {
        'Authorization': f'Ghost {GHOST_API_KEY}'
    }

    posts_url = f'{GHOST_API_URL}/admin/posts/'
    response = requests.get(posts_url, headers=headers)
    response.raise_for_status()

    posts = response.json().get('posts', [])

    for post in posts:
        post_id = post['id']
        delete_url = f'{GHOST_API_URL}/admin/posts/{post_id}/'
        delete_response = requests.delete(delete_url, headers=headers)
        delete_response.raise_for_status()
        logging.info(f'Deleted post with ID {post_id}')

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        delete_all_posts()
        return func.HttpResponse("All posts have been deleted", status_code=200)
    except Exception as e:
        logging.error(f'Error while deleting posts: {e}')
        return func.HttpResponse("Failed to delete all posts", status_code=500)
