# Use a base image with Python installed
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the backup script into the container
COPY backup_script.py /app/backup_script.py

# Install any required dependencies for the backup script
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Define volume mount point
VOLUME /data

# Set the command to run the backup script
CMD ["python", "backup_script.py"]
