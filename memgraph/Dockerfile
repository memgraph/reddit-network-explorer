FROM memgraph/memgraph-mage

USER root

# Install the NLP libraries
RUN python3 -m pip install -U pip setuptools wheel && \
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
