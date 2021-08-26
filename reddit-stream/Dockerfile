FROM python:3.8

# Install CMake for gqlalchemy
RUN apt-get update && \
  apt-get --yes install cmake && \
  rm -rf /var/lib/apt/lists/*

# Install packages
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY app.py /app/app.py

COPY dummy.py /app/dummy.py
COPY worldnews_data.jsonl /app/worldnews_data.jsonl

WORKDIR /app
