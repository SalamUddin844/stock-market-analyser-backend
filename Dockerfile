# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 to allow communication to/from the container
EXPOSE 5000

# Define environment variables (optional)
ENV FLASK_APP=main.py
ENV FLASK_ENV=production

# Run the application
CMD ["python", "api/main.py"]
