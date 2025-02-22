# Use official Python 3.11 image as a base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Expose the FastAPI server port
EXPOSE 8000

# Set environment variables (modify as needed)
ENV PYTHONUNBUFFERED=1

# Command to run the FastAPI server
CMD ["python", "-m", "src.server"]
