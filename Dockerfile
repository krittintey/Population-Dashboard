FROM python:3.7

WORKDIR /app

EXPOSE 8050

ENV UPDATE_DATA False

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app /app

CMD ["python", "./app.py"]