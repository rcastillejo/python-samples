# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START docs_quickstart]
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# The ID of a sample document.
DOCUMENT_ID = '1vp3O4RQzPsPlkvnjhWP3ax8CIRHw_uEaHniPDLTntso'

def main():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    #if os.path.exists('token.pickle'):
    #    with open('token.pickle', 'rb') as token:
    #        creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
    #    with open('token.pickle', 'wb') as token:
    #        pickle.dump(creds, token)

    service = build('docs', 'v1', credentials=creds)

    get_document(service)
    #create_document(service)
    #create_table(service)
    delete_table(service)

def get_document(service):
    # Retrieve the documents contents from the Docs service.
    document = service.documents().get(documentId=DOCUMENT_ID).execute()

    print('The title of the document is: {}'.format(document.get('title')))

def create_document(service):
    title = 'My Document'
    body = {
        'title': title
    }

    doc = service.documents() \
        .create(body=body).execute()

    print('Created document with title: {0}'.format(doc))

def create_table(service):
    # Insert a table at the end of the body.
    # (An empty or unspecified segmentId field indicates the document's body.)

    requests = [{
        'insertTable': {
            'rows': 3,
            'columns': 3,
            'endOfSegmentLocation': {
                'segmentId': ''
            }
        },
    }
    ]

    result = service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()

    print('Updated document with table: {0}'.format(result))


def delete_table(service):
    # Delete a table that was inserted at the start of the body.
    # (The table is the second element in the body: ['body']['content'][2].)

    document = service.documents().get(documentId=DOCUMENT_ID).execute()
    table = document['body']['content'][2]

    requests = [{
        'deleteContentRange': {
            'range': {
                'segmentId': '',
                'startIndex': table['startIndex'],
                'endIndex':   table['endIndex']
            }
        },
    }
    ]

    result = service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()

    print('Deleted table from document: {0}'.format(result))

if __name__ == '__main__':
    main()
# [END docs_quickstart]
