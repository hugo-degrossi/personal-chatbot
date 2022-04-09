# Personal Chatbot

Here's my personal chatbot made using SpaCy, FastAPI and deployed on Heroku :)

## To run locally

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Then, run via uvicorn:

    uvicorn slack:app --reload

## To deploy to heroku

    heroku login  
    heroku create
    git push heroku main
    heroku open