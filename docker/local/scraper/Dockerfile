# pull official base image
FROM python:3.8-slim-buster

# set work directory
RUN mkdir /app
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update -y \
    && apt-get install -y postgresql-dev gcc python3-dev musl-dev build-base libffi-dev \
    # Install dev-tools
    bash libressl-dev \
    # LXML dependencies
    libxml2 libxslt libxslt-dev

# Requirements are installed here to ensure they will be cached.
RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY ./docker/local/scraper/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY ./docker/local/scraper/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

ENTRYPOINT ["/entrypoint"]
