# Use python3.7.2
FROM python:3.7.2-stretch

# Set /app as working directory
WORKDIR /app

# Copy /app dir content into container /app dir
ADD . /app

# Install all dependencies
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

# Run the command to start uWSGI
CMD ["flask", "run", "--host=0.0.0.0"]
