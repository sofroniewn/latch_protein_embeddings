# latch base image + dependencies for latch SDK --- removing these will break the workflow
from 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:9c8f-main
run pip install latch==2.13.5
run mkdir /opt/latch

# install system requirements
copy system-requirements.txt /opt/latch/system-requirements.txt
run apt-get update --yes && xargs apt-get install --yes </opt/latch/system-requirements.txt

# add requirements from `requirements.txt` to python environment
copy requirements.txt /opt/latch/requirements.txt
run pip install --requirement /opt/latch/requirements.txt

# copy all code from package (use .dockerignore to skip files)
copy . /root/

# latch internal tagging system + expected root directory --- changing these lines will break the workflow
arg tag
env FLYTE_INTERNAL_IMAGE $tag
workdir /root
