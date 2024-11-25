# Use the latest Ubuntu LTS version as the base image
FROM ubuntu:22.04

# File Author / Maintainer
LABEL maintainer Manuel Rueda <manuel.rueda@cnag.eu>

# Set the environment variable to prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install system dependencies
RUN apt-get update && \
    apt-get install -y \
        build-essential \
        git \
        perl \
        cpanminus \
        python3 \
        python3-pip \
        python3-tk \
        python3-pil \
        python3-pil.imagetk \
        tk-dev \
        tcl-dev && \
    rm -rf /var/lib/apt/lists/*

# Install required Python packages
RUN pip3 install --no-cache-dir \
    customtkinter \
    Pillow

# Install the Pheno::Ranker Perl module from CPAN
RUN cpanm --notest Pheno::Ranker

# Clone your Git repository containing the application code
RUN git clone https://github.com/mrueda/pheno-ranker-app.git /opt/pheno-ranker-app

# Set the working directory to the cloned repository
WORKDIR /opt/pheno-ranker-app

# Expose any necessary ports (if your application uses them)
# EXPOSE 8000

# Set the command to run your application
# Replace 'your_script.py' with the entry point of your application
CMD ["python3", "your_script.py"]
