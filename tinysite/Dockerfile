# Use an official Python base image
FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt && rm -rf /root/.cache/pip

# Expose the port the app runs on
EXPOSE 8080

# Command to run the app
CMD ["gunicorn","--config", "gunicorn_config.py", "app:app"]
