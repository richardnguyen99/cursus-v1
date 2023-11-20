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
    curl \ 
    && rm -rf /var/lib/apt/lists/*

# Get nodejs from source
RUN curl -sL https://deb.nodesource.com/setup_20.x -o /tmp/nodesource_setup.sh

# Install nodejs
RUN bash /tmp/nodesource_setup.sh
RUN apt-get install -y nodejs

# Set work directory (similiar to cd)
WORKDIR /cursus

# Copy project to docker container
COPY . .

# JavaScript dependencies related to the project
RUN npm install -g sass
RUN npm install -g uglify-js
RUN npm install -g requirejs
RUN npm install -g postcss
RUN npm install -g postcss-cli
RUN npm install -g autoprefixer

# Install dependencies
RUN pip install --upgrade pip 
RUN pip install -e .

# Expose port
EXPOSE 50001

# Remove webassets cache
RUN rm -rf /cursus/cursus/static/.webassets-cache
RUN rm -rf /cursus/cursus/static/css/min.bundle.css
RUN rm -rf /cursus/cursus/static/js/min.bundle.js

# Run the command as entry point
CMD ["cursus", "run"]
