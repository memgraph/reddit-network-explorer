FROM python:3.9

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install CMake for gqlalchemy
RUN apt-get update && \
  apt-get --yes install cmake && \
  rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install -U pip \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="${PATH}:/root/.poetry/bin"

WORKDIR /app
COPY . .
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

ENV FLASK_ENV=development
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

#ENTRYPOINT ["poetry", "run", "python", "server/app.py"]
ENTRYPOINT ["gunicorn", "--worker-class", "eventlet", "-w", "2", "-b", "0.0.0.0:5000", "--preload", "server.app:app"]