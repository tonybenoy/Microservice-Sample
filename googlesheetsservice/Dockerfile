FROM python:latest
RUN apt update -y
RUN apt upgrade -y
WORKDIR /usr/app/src
ADD ./googlesheetsservice/requirements.txt ./
RUN pip install -r requirements.txt
WORKDIR /usr/app/src
COPY ./googlesheetsservice/sheetservice.py ./
CMD [ "python", "./sheetservice.py"]