# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Set environment variables (you can also set these in a .env file)
ENV SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN}
ENV SLACK_SIGNING_SECRET=${SLACK_SIGNING_SECRET}
ENV SLACK_BOT_USER_ID=${SLACK_BOT_USER_ID}

# Expose the port that the Flask app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "slack/app.py"]
