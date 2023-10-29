# Use an official nginx runtime as a parent image
FROM nginx:latest

# Copy Nginx Configuration to the container 
# COPY nginx.conf /etc/nginx/nginx.conf

COPY nginx.conf.template /etc/nginx/templates/nginx.conf.template
COPY docker-entrypoint.sh .

# Expose the port on which Nginx license
EXPOSE 80

RUN ["chmod", "+x", "./docker-entrypoint.sh"]

# Command to start Nginx
CMD ["./docker-entrypoint.sh"]
