# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Install necessary system utilities and libraries
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    git \
    build-essential \
    libhdf5-dev  # Add HDF5 development library necessary for h5py

# Install Python libraries from requirements.txt
COPY customer-targeting-data-pipeline/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container at /app
COPY customer-targeting-data-pipeline/ .

# Handle special installations like Pyke
RUN wget  https://sourceforge.net/projects/pyke/files/pyke/1.1.1/pyke3-1.1.1.zip \
 && unzip pyke3-1.1.1.zip  -d /pyke \
 && ls /pyke/*  # This line lists the contents of the directory to verify the structure

WORKDIR /pyke/pyke-1.1.1
RUN python setup.py build
RUN python setup.py install

WORKDIR /app

# Copy the shell script into the container
COPY customer-targeting-data-pipeline/run_pipeline.sh /app/run_pipeline.sh

# Run the shell script
CMD ["./run_pipeline.sh"]

