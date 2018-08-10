FROM python:3
COPY . /matrix_bot
WORKDIR /matrix_bot
RUN pip install -r requirements.txt
