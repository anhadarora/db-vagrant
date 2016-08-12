#
# Database access functions for the web forum.
#

import time
import psycopg2

import bleach

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''

    ## Database connection
    DB = psycopg2.connect("dbname=forum")
    c = DB.cursor()
    query = 'select * from posts order by time desc;'
    c.execute(query)
    posts = c.fetchall()
    # formatting
    posts = [{'content': str(post[0]),'time': str(post[1])} for post in posts]
    DB.close()
    print ' ****** forumdb posts ****** '
    print posts

    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    ## Database connection
    DB = psycopg2.connect("dbname=forum")
    c = DB.cursor()
    sanit_content = str(bleach.clean(content))
    c.execute("INSERT INTO posts (content) VALUES (%s)", (sanit_content,))
    DB.commit()
    DB.close()
