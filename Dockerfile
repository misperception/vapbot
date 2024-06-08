FROM python:3.11

WORKDIR /vapbot

COPY .

RUN apt-get update && apt-get install -y libffi-dev python3.11-dev
RUN pip install -r requirements.txt

CMD ["python", "main.py"]

