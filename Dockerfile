FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:dd8f-main

RUN apt-get update -y && \
    apt-get -y install git
    
# Install requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Download genome for pyensembl
RUN pyensembl install --release 77 --species human

# STOP HERE:
# The following lines are needed to ensure your build environement works
# correctly with latch.
RUN python3 -m pip install --upgrade latch
COPY wf /root/wf
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
WORKDIR /root
