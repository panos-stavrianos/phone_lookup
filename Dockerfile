FROM tiangolo/meinheld-gunicorn:python3.7

WORKDIR /usr/data
RUN mkdir -p /usr/app-data
COPY app-data /usr/app-data

WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt

