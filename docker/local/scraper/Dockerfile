# pull official base image
FROM python:3.8-alpine3.10

# set work directory
RUN mkdir /app
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add gcc python3-dev
# RUN apk add libressl-dev
# # install psycopg2 dependencies
# RUN apk update \
#     && apk add postgresql-dev gcc python3-dev musl-dev build-base libffi-dev \
#     # Install dev-tools
#     && apk add bash
# # Pillow dependencies
# RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
# # python-libmagic dependencies
# RUN apk add libmagic
# # WeasyPrint dependencies
# RUN apk add cairo-dev pango-dev gdk-pixbuf-dev

# Requirements are installed here to ensure they will be cached.
RUN pip install --upgrade pip
COPY ./requirements /app/requirements.txt

# COPY ./docker/local/scraper/entrypoint /entrypoint
# RUN sed -i 's/\r//' /entrypoint
# RUN chmod +x /entrypoint

# COPY ./docker/local/scraper/start /start
# RUN sed -i 's/\r//' /start
# RUN chmod +x /start

# EXPOSE 8000
# ENTRYPOINT ["/entrypoint"]
