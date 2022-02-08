FROM python:latest
RUN apt update -y
RUN apt upgrade -y
WORKDIR /usr/app/src
ADD ./twiliosms/requirements.txt ./
RUN pip install -r requirements.txt
WORKDIR /usr/app/src
COPY ./twiliosms/smsservice.py ./
CMD [ "python", "./smsservice.py"]