# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any necessary Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on (if applicable)
EXPOSE 3000

# Run the bot
CMD ["python", "app.py"]
