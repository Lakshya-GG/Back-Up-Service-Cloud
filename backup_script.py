import os
import time
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import base64
import json
from util import authenticate
import datetime


## Directories
SECRET_DIR = './secrets'
DIRECTORY_TO_WATCH = './myDir'
LOG_FILE_PATH = './backups/file_events.log'
FOLDER_ID = '1e4vML9opX61VLfOmyosQDQacpPP28ggY'
HISTORY_FOLDER_PATH = './backups/History'


# Define scopes and other constants
SCOPES = ['https://www.googleapis.com/auth/drive']
CLIENT_SECRET_FILE = os.path.join(SECRET_DIR,'client_secret_encoded.txt')  # Path to your downloaded credentials file
TOKEN_FILE = os.path.join(SECRET_DIR,'token_encoded.txt')
API_NAME = 'drive'
API_VERSION = 'v3'



def get_parents_list(src_path,service):
    # Split the source path into directory components
    dirs = src_path.split(os.path.sep)
    response = service.files().list(
        q=f"mimeType='application/vnd.google-apps.folder' and name='{dirs[-1]}'",
        fields='files(id)'
    ).execute()
    # Extract the parent directory ID if found
    directories = response.get('files', [])
    parent_id = FOLDER_ID
    if directories:
            parent_id = directories[0]['id']

    return parent_id


def get_file_id(file_name,parent,service):
    query = f"name='{file_name}' and '{parent}' in parents"
    response = service.files().list(q=query, fields='files(id)').execute()
    files = response.get('files', [])
    if files:
        # If file exists, return its ID
        return files[0]['id']
    else:
        # If file doesn't exist, return None
        return None

def get_directory_id(folder_name,parent,service):
    # Construct the query to search for the directory
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and '{parent}' in parents"

    # Execute the query to search for the directory
    results = service.files().list(q=query, fields='files(id)').execute()
    folders = results.get('files', [])

    if folders:
        # Return the ID of the first directory found with the specified name
        return folders[0]['id']
    else:
        # Directory not found
        return None

def create_or_update_file(src_path,service):

    folder_path,file_name = os.path.split(src_path)
    parent = (get_parents_list(folder_path,service))
    file_id = get_file_id(file_name,parent,service)
    file_path = DIRECTORY_TO_WATCH+'/'+src_path
    ## Get contents of file
    media = MediaFileUpload(file_path, resumable=True)
    if file_id:
        # If file exists, update its content
        service.files().update(fileId=file_id, media_body=media).execute()
        print(f"File '{file_name}' updated.")
    else:
        # If file doesn't exist, create it
        file_metadata = {
            'name': file_name,
            'parents': [parent]
        }
        service.files().create(body=file_metadata, media_body=media).execute()
        print(f"File '{file_name}' created.")

def create_dir(src_path,service):
    dirs = [FOLDER_ID]+src_path.split(os.path.sep)
    
    folder_path = dirs[-2]
    folder_name = dirs[-1]
    parent = (get_parents_list(folder_path,service))

    #create metadata for folder
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents':[parent]
    }

    folder = service.files().create(body=folder_metadata, fields='id').execute()

    print('Folder uploaded: %s' % folder.get('id'))

def delete_file(src_path,service):
    folder_path,file_name = os.path.split(src_path)
    parent = (get_parents_list(folder_path,service))
    file_id = get_file_id(file_name,parent,service)
    if file_id:
        # Delete the file using its ID
        service.files().delete(fileId=file_id).execute()
        print(f"File '{file_name}' deleted from directory with ID '{parent}'.")
    else:
        print(f"File '{file_name}' not found in directory with ID '{parent}'.")


def delete_dir(src_path,service):
    dirs = [FOLDER_ID]+src_path.split(os.path.sep)
    
    folder_path = dirs[-2]
    folder_name = dirs[-1]
    parent = (get_parents_list(folder_path,service))
    directory_id = get_directory_id(folder_name,parent,service)
    results = service.files().list(q=f"'{directory_id}' in parents", fields='files(id)').execute()
    files = results.get('files', [])
    
    # Delete all the files and subdirectories
    for file in files:
        if file:
            # Delete the file using its ID
            service.files().delete(fileId=file).execute()
        else:
            pass

    # Delete the directory itself
    service.files().delete(fileId=directory_id).execute()
    print(f"Directory with ID '{directory_id}' deleted.")

def perform_action(event,is_directory,src_path,service):
    if event == "created":
        if is_directory == False:
            create_or_update_file(src_path,service)
        else:
            create_dir(src_path,service)
            # pass
    elif ((event == "modified") & (is_directory == False)):
        create_or_update_file(src_path,service)
    elif event == "deleted":
        if is_directory == False:
            delete_file(src_path,service)  # Delete the file
        else:
            delete_dir(src_path,service) # Delete the directory


def read_log():
    creds = authenticate()
    service = build('drive', 'v3',credentials = creds)
    with open(LOG_FILE_PATH, 'r') as file:
        for line in file:
            log_data = json.loads(line.strip())
            event = log_data['event_name']
            is_directory = log_data['is_directory']
            src_path = os.path.relpath(log_data['src_path'], DIRECTORY_TO_WATCH)
            perform_action(event,is_directory,src_path,service)


def write_history():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    backup_log = f"backup_{timestamp}"
    with open(LOG_FILE_PATH,'r') as src:
        new_backup_path = HISTORY_FOLDER_PATH + '/' + backup_log+'.log'
        with open(new_backup_path,'w') as dest:
            dest.write(backup_log+'\n')
            dest.write(src.read())

def clear_log():
    with open(LOG_FILE_PATH,'w'):
        pass
# Main function to start monitoring the directory
def main():
    folder_id = '1e4vML9opX61VLfOmyosQDQacpPP28ggY'

    read_log()
    write_history()
    clear_log()

if __name__ == "__main__":
    main()