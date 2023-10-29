# syntax=docker/dockerfile:1

# Pull base image
FROM python:3.11-slim-buster

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    && rm -rf /var/lib/apt/lists/*

# Set work directory (similiar to cd)
WORKDIR /cursus

# Copy project to docker container
COPY . .

# Install dependencies
RUN pip install --upgrade pip 
RUN pip install -e .

# Expose port
EXPOSE 50001

# Run the command as entry point
CMD ["cursus", "run"]
