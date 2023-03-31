FROM python

EXPOSE 5000

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . .

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]
