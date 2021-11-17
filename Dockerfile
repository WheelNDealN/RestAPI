FROM python:3.8

COPY main.py .
COPY info.json .
COPY requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "./main.py" ]