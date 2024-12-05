# Use the official Ubuntu 20.04 image as the base image
FROM ubuntu:20.04

# Update the package list in the base image
RUN apt-get update -y

# Copy the contents of the current directory to the /app directory in the image
COPY . /app

# Set the working directory to /app
WORKDIR /app

# Install python3-pip and mysql-client packages from the package repositories
RUN set -xe \
    && apt-get update -y \
    && apt-get install -y python3-pip \
    && apt-get install -y mysql-client 

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install the Python dependencies listed in requirements.txt
RUN pip install -r requirements.txt

# Install the boto3 library for AWS integration
RUN pip install boto3

# Expose port 81 to the host system
EXPOSE 81

# Specify the entry point for the container, which is "python3"
ENTRYPOINT [ "python3" ]

# Set the default command to run the app.py script
CMD [ "app.py" ]
