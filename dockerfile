# Use the Python 3.10 runtime as a base image
FROM python:3.10

# Environment variable: prevent Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# Environment variable: prevent buffering the output in the standard output (only to the terminal)
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the port that Django is running on
EXPOSE 8000

# Run the Django project at starting
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
