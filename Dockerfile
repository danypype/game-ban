# syntax=docker/dockerfile:1
# install python
FROM python:3.9-bullseye

# copy app files
COPY . .
RUN cp .env.aws .env

# install dependencies
RUN pip install -U pip setuptools wheel
RUN pip install -r requirements.txt
RUN pip install gunicorn

# expose port 8080
EXPOSE 8080
