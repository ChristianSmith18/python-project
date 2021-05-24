# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
# install needed packages
RUN apt-get update \
    && apt-get install -y default-libmysqlclient-dev build-essential \
    && pip install --trusted-host pypi.python.org -r requirements.txt \
    && apt-get remove -y default-libmysqlclient-dev build-essential
# RUN pip install -r requirements.txt
COPY . /code/
CMD ["python" "manage.py" "migrate"]