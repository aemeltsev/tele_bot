# Use official Python 3.10 image
FROM python:3.10-slim-buster

# Install and update pip
RUN pip install --upgrade pip

# Install work directory
WORKDIR /app

# Copy requirements files and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt --use-pep517

# Copying all project files
COPY . .

# Install environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Specify the command to launch the bot
CMD ["python", "bot.py"]