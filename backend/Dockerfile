# pull the official docker image
FROM python:latest

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# run command
CMD ["python", "main.py"]