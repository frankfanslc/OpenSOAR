FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY app/requirements.txt .
RUN pip install -r requirements.txt

COPY ./app /app