FROM crossbario/autobahn-python:cpy3-minimal-aio-17.6.1

WORKDIR /app/

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD main.py .

CMD ["python", "main.py"]
