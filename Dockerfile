# Use a lightweight Python image
FROM python:slim

# Set environment variables to prevent Python from writing .pyc files & Ensure Python output is not buffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    GOOGLE_APPLICATION_CREDENTIALS=/app/keys/gcp-credentials.json

    # ARG

ARG GOOGLE_APPLICATION_CREDENTIALS_PATH
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/keys/gcp-credentials.json

#ENV GOOGLE_APPLICATION_CREDENTIALS=/app/keys/gcp-credentials.json
# Set the working directory
WORKDIR /app

# Install system dependencies required by LightGBM
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY . .
COPY keys/gcp-credentials.json /app/keys/gcp-credentials.json

# Install the package in editable mode
RUN pip install --no-cache-dir -e .

# Train the model before running the application
#RUN python pipeline/training_pipeline.py

# Expose the port that Flask will run on
EXPOSE 5000

# Command to run the app
CMD ["python", "application.py"]