FROM memgraph/memgraph-mage

USER root 

# Install packages
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

USER memgraph
