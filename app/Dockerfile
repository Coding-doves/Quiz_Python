# Use python3.7.2
FROM python:3.7.2-stretch

# Set /app as working directory
WORKDIR /app

# Copy /app dir content into container /app dir
ADD . /app

# Install all dependencies
RUN pip install -r requirements.txt

# Run the command to start uWSGI
CMD ["uwsgi", "app.ini"]
