FROM python:3.6.10

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ./run.sh