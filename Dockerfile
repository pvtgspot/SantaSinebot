FROM python:3.8

WORKDIR /opt/sinebot
ADD . .

RUN python3 -m pip install -r requirements.txt

CMD [ "python3", "./src/main.py" ]
