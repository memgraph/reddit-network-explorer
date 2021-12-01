FROM memgraph/memgraph-mage:1.01

USER root

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-setuptools \
    python3-dev \
    && pip3 install -U pip

# Install the NLP libraries
RUN python3 -m pip install -U wheel && \
    python3 -m pip install -U spacy

# Download the NLP model for English language
RUN python3 -m spacy download en_core_web_sm

# Install pip packages
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# Copy the local query modules
COPY procedures/ /procedures
COPY transformations/ /transformations

USER memgraph
