# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.7-alpine

#ARG secrets_env=./bats/secrets.py

#ENV env_secrets = $secrets_env
# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
#ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /xpence

# Set the working directory
WORKDIR /xpence

# Copy the current directory contents into the container 
ADD . /xpence/

# Install any needed packages specified in requirements.txt
RUN apk update && apk add bash && apk add --no-cache postgresql-libs && apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev &&pip install -r requirements.txt && apk --purge del .build-deps&& apk add --no-cache git

#COPY ./reversion/models.py /usr/local/lib/python3.6/site-packages/reversion/models.py

#COPY $secrets_env /iebats/bats/secrets.py

COPY start.sh /start.sh

EXPOSE 8000

CMD ["/start.sh"]