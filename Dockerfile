FROM python:3.8-alpine

# Install deps necessary for uvloop and postgres
RUN apk add --no-cache build-base postgresql-dev

# Install pipenv
RUN pip3 install pipenv

# Create app directory
RUN mkdir -p /app
WORKDIR /app

# Install app dependencies
COPY Pipfile Pipfile.lock /app/

RUN pipenv install --system --deploy

ENV LOG_FORMAT json

COPY . /app

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]

