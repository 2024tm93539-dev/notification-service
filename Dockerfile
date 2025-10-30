# Use an official lightweight Python base image
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Copy only requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose Flask port
EXPOSE 5001

# Set environment variables for Flask
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

# Run the application
CMD ["python", "run.py"]

