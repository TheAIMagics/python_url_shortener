import validators
from fastapi import FastAPI, HTTPException

from . import schemas



def raise_bad_request(message):
    '''
    This function takes message as an argument and raises an HTTPException with a status code 400.
    '''
    raise HTTPException(status_code=400, detail=message)




@app.post("/url")
def create_url(url: schemas.URLBase):
    '''
    pydantic makes sure the URL is a string, it doesn’t check if the string is a valid URL. That’s the job of the validators package
    '''
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")
    return f"TODO: Create database entry for: {url.target_url}"
