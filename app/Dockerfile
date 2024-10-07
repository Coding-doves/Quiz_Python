# Use python3.10
FROM python:3.10-slim

# Set /app as working directory
WORKDIR /app

# Copy only requirements.txt initially to install dependencies
COPY requirements.txt .

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y curl build-essential

# Install Rust and Cargo
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y && \
    . "$HOME/.cargo/env" && \
    echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> $HOME/.bashrc

# Ensure Rust is added to PATH
ENV PATH="/root/.cargo/bin:${PATH}"
    
# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the application code
COPY . /app

# Install uWSGI (if not in requirements.txt)
RUN pip install uwsgi

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable for Flask
ENV FLASK_APP=app.py

# Run the uWSGI server
CMD ["uwsgi", "--http", "0.0.0.0:5000", "--wsgi-file", "app.py", "--callable", "app", "--processes", "4", "--threads", "2"]
