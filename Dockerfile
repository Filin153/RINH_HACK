FROM python:3.9

RUN mkdir /API

WORKDIR /API

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9898

CMD gunicorn --workers 1 --worker-class uvicorn.workers.UvicornWorker main:app --bin=${IP}:9898