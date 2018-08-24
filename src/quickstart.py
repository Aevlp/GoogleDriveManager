##!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from googleapiclient.discovery import build, MediaFileUpload
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from oauth2client import file, client, tools
from oauth2client.client import OAuth2WebServerFlow

from httplib2 import Http
import webbrowser
import io

def drive_credentials():
    """
        Get credentials and build the Google Drive service.
    """
    SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.metadata']
    CREDENTIAL_PATH = './credentials/credentials.json'
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(CREDENTIAL_PATH, SCOPES)
        creds = tools.run_flow(flow, store)
    drive_service = build('drive', 'v3', http=creds.authorize(Http()))
    return drive_service


def search_file(FILE_NAME):
    """
        Search and open a file from Google Drive.
            # FILE_NAME: name of the file to be searched for or keyword contained in it.
    """
    results = DRIVE.files().list(fields="nextPageToken,files(id, name, webViewLink)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        for item in items:
            if (FILE_NAME in item['name']):
                webbrowser.open(item['webViewLink'])  # Go to item['webViewLink']

def upload(FILE_PATH, MIME_TYPE):
    """
        Upload a file to Google Drive.
            x FILE_PATH : path of the file to upload
            x MIME_TYPE : output format of the file
                For more informations : https://github.com/odeke-em/drive/wiki/List-of-MIME-type-short-keys

    """
    file_metadata = {'name': 'test.jpeg'}
    media = MediaFileUpload(FILE_PATH, mimetype=MIME_TYPE)
    file_service = DRIVE.files().create(body=file_metadata,
                    media_body=media,
                    fields='id').execute()

    print('File ID: %s' % file_service.get('id'))


def download_file(FILE_ID, MIME_TYPE, FILENAME):
    """
        Download a file from Google Drive.
            x FILE_ID : id of the file on Google Drive
            x MIME_TYPE : output format of the file
              For more informations : https://github.com/odeke-em/drive/wiki/List-of-MIME-type-short-keys
    """
    if "google-apps" in MIME_TYPE:                                        #the file has a google format
        if ("document" or "form") in MIME_TYPE:
            request = DRIVE.files().export_media(fileId=FILE_ID,
                            mimeType="text/plain")
        elif "spreadsheet" in MIME_TYPE:
            request = DRIVE.files().export_media(fileId=FILE_ID,
                            mimeType="text/csv")
    else:
        request = DRIVE.files().get_media(fileId=FILE_ID)
    fh = io.FileIO(FILENAME, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))


if __name__ == '__main__':
    DRIVE = drive_credentials()
    # apply funtion
