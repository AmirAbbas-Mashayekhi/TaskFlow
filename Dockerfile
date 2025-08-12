FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install necessary system dependencies for building Python packages like mysqlclient
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    libmariadb-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user (No user switch yet)
RUN addgroup --system app && adduser --system --ingroup app app

# Set the working directory
WORKDIR /app

# Copy the requirements file (Change ownership from root to app user)
COPY --chown=app:app requirements.txt ./

# Install Python dependencies as root
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files (Change ownership form root to app user)
COPY --chown=app:app . .

# Switch to app user
USER app

# Run the Django development server after waiting for the database to run
CMD ["scripts/wait-for-it.sh", "db:3306", "--", "python3", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000
