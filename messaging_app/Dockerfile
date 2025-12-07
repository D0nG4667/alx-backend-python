# Use official Python base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Expose Django default port
EXPOSE 8000

# Reminder: run container with port mapping
# Example: docker run -d -p 8000:8000 messaging_app:latest

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
