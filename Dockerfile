# our base image
FROM ubuntu:18.04

# Upgrade installed packages
RUN apt-get update && apt-get upgrade -y && apt-get clean

# Python package management and basic dependencies
RUN apt-get install -y curl python3.7 python3.7-dev python3.7-distutils

# Register the version in alternatives
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1

# Set python 3 as the default python
RUN update-alternatives --set python /usr/bin/python3.7

# Upgrade pip to latest version
RUN curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python get-pip.py --force-reinstall && \
    rm get-pip.py

# copy the requirements.txt 
COPY requirements.txt ./usr/src/app/requirements.txt

# copy files required for the app to run
COPY . /usr/src/app

WORKDIR /usr/src/app/src/util

# install Python modules needed by the Python app
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

# remove jwt as it is causing conficts 
RUN pip uninstall jwt 

# tell the port number the container should expose
EXPOSE 8000

# run the application
CMD ["python", "/usr/src/app/app.py"]