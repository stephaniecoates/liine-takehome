# Use the official Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose Flask port
EXPOSE 8000

# Command to run the app
CMD ["python", "app.py"]
