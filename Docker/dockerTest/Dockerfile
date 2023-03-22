FROM python:3.11

WORKDIR /python/app

COPY . .

RUN pip install -r reqs.txt

EXPOSE 5000

CMD ["python", "./app.py"]
