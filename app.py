import secrets, sys
import validators
from fastapi import Depends ,FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from url_shortener_app.components import schemas, models
from url_shortener_app.components.database import SessionLocal, engine
from url_shortener_app.logger import logging
from url_shortener_app.exception import URLShortnerException

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        raise URLShortnerException(e,sys)
    finally:
        db.close()

def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)

def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)

@app.get("/")
def read_root():
    try:
        logging.info("Root url hitted")
        return "Welcome to the URL shortener API :)"
    except Exception as e:
        raise URLShortnerException(e,sys)

@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    """
                Method Name: create_url
                Description: Requires a URLBase schema as an argument and depends on the database session. By passing get_db into Depends(), 
                you establish a database session for the request and close the session when the request is finished.
                Output: The URL for the create_url endpoint is /url.
                On Failure: Raise Exception
        """
    try:
        if not validators.url(url.target_url):
            raise_bad_request(message="Your provided URL is not valid")

        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        key = "".join(secrets.choice(chars) for _ in range(5))
        secret_key = "".join(secrets.choice(chars) for _ in range(8))
        db_url = models.URL(
            target_url=url.target_url, key=key, secret_key=secret_key
        )
        db.add(db_url)
        db.commit()
        db.refresh(db_url)
        db_url.url = key
        db_url.admin_url = secret_key
        logging.info("url created successfully with key =",db_url.url)
        return db_url
    except Exception as e:
        raise URLShortnerException(e,sys)

@app.get("/{url_key}")
def forward_to_target_url(
        url_key: str,
        request: Request,
        db: Session = Depends(get_db)
    ):
    """
                Method Name: forward_to_target_url
                Description:  With the "/{url_key}" argument, the forward_to_target_url() function will be called any time a client requests a URL that matches the host and key pattern.
                Output:We look for an active URL entry with the provided url_key in our database. If a database entry is found, then we return the RedirectResponse with target_url
                On Failure: Raise Exception
        """
    try:
        db_url = (
            db.query(models.URL)
            .filter(models.URL.key == url_key, models.URL.is_active)
            .first()
        )
        if db_url:
            logging.info("url redirected successfully with key ")
            return RedirectResponse(db_url.target_url)
        else:
            logging.info("url doesnt exists ")
            raise_not_found(request)
    except Exception as e:
        raise URLShortnerException(e,sys)