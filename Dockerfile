FROM python:3

ADD flask_server.py .
ADD requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 3018

CMD [ "python", "./flask_server.py"]
