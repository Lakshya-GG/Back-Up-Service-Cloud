# Backup Service using Docker and Kubernetes

## Overview
This project aims to create a backup service using Docker and Kubernetes that periodically backs up the contents of a specified folder to Google Drive. The service utilizes Google Drive API for interaction with Google Drive. The backup process is orchestrated and scheduled using Kubernetes CronJobs.

## Pre-Requisites/Pre-Installation
Before getting started with the setup, ensure you have the following prerequisites installed:
- Docker (compatible with Windows, Ubuntu, MacOS)
- Kubernetes (compatible with Windows, Ubuntu, MacOS)

## Week-1: Containerized Google Drive Client
### Technical Breakdown:
1. **Set up Google Drive API:**
   - Obtain credentials for the Google Drive API.
   - Use the `google-api-python-client` library for interaction with Google Drive.
2. **Create a Docker Container:**
   - Write a Dockerfile including all necessary dependencies and the backup script.
   - Build the Docker image.
3. **Write the Backup Script:**
   - Develop a Python script utilizing the Google Drive API for uploading files.
   - Ensure the script can be triggered at regular intervals.

## Week-2: Kubernetes Deployment & Orchestration
### Technical Breakdown:
1. **Kubernetes CronJob:**
   - Define a CronJob resource in Kubernetes to schedule the backup operation.
   - The CronJob will execute the Docker container at specified intervals.
2. **Persistent Volume Claims (PVC):**
   - Utilize PVCs in Kubernetes to grant access to the data intended for backup.
3. **Monitoring and Logging:**
   - Implement logging to track the backup process.
   - Optionally, set up monitoring to alert in case of failures.
4. **Security Considerations:**
   - Securely manage API credentials and sensitive data.
   - Utilize Kubernetes secrets to store sensitive information.

## Testing and Validation
- Test the backup process thoroughly to ensure data integrity.
- Validate the recovery process from the backups.

## Usage
1. Clone this repository.
2. Follow the instructions in the respective directories (`week-1`, `week-2`) to set up and deploy the backup service.

## Contributors
- [Lakshya Singh](https://github.com/Lakshya-GG)
- [Manish I](https://github.com/AlterHoodie)
- Manav Jarial(https://github.com/dantesbane)
- Mohammed Zaid()

## License
This project is licensed under the [MIT License](link-to-license).

---

Feel free to adjust the sections and content as needed for your project's specific requirements and preferences.
