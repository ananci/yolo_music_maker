
# per instructions on https://google-developers.appspot.com/youtube/v3/code_samples/code_snippet_instructions#toggle-code-snippets-and-full-samples
# pip install --upgrade google-api-python-client
# pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2
# pip install --upgrade requests
# created music-memes-maker in app engine
# made a client_secret.json file for my project
# added client_secret*.json to .gitignore


# -*- coding: utf-8 -*-

import os

import google.oauth2.credentials

import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

# Build a resource based on a list of properties given as key-value pairs.
# Leave properties with empty values out of the inserted resource.
def build_resource(properties):
  resource = {}
  for p in properties:
    # Given a key like "snippet.title", split into "snippet" and "title", where
    # "snippet" will be an object and "title" will be a property in that object.
    prop_array = p.split('.')
    ref = resource
    for pa in range(0, len(prop_array)):
      is_array = False
      key = prop_array[pa]

      # For properties that have array values, convert a name like
      # "snippet.tags[]" to snippet.tags, and set a flag to handle
      # the value as an array.
      if key[-2:] == '[]':
        key = key[0:len(key)-2:]
        is_array = True

      if pa == (len(prop_array) - 1):
        # Leave properties without values out of inserted resource.
        if properties[p]:
          if is_array:
            ref[key] = properties[p].split(',')
          else:
            ref[key] = properties[p]
      elif key not in ref:
        # For example, the property is "snippet.title", but the resource does
        # not yet have a "snippet" object. Create the snippet object here.
        # Setting "ref = ref[key]" means that in the next time through the
        # "for pa in range ..." loop, we will be setting a property in the
        # resource's "snippet" object.
        ref[key] = {}
        ref = ref[key]
      else:
        # For example, the property is "snippet.description", and the resource
        # already has a "snippet" object.
        ref = ref[key]
  return resource

# Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.iteritems():
      if value:
        good_kwargs[key] = value
  return good_kwargs

def captions_list(client, **kwargs):
  # See full sample for function
  kwargs = remove_empty_kwargs(**kwargs)

  response = client.captions().list(
    **kwargs).execute()

  return response

def download_caption(youtube, caption_id, tfmt):
  subtitle = youtube.captions().download(
    id=caption_id,
    tfmt=tfmt).execute()
  return subtitle

if __name__ == '__main__':
  # When running locally, disable OAuthlib's HTTPs verification. When
  # running in production *do not* leave this option enabled.
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
  client = get_authenticated_service()
  # 
  # caption_resp = captions_list(client,
  #   part='snippet',
  #   videoId='M7FIvfx5J10',
  #   onBehalfOfContentOwner='')
  #
  # with open('/Users/demouser/misc_project/yolo_music_maker/caption_list_data', 'w') as cld:
  #     cld.write(str(caption_resp))


  captions = download_caption(
    client, '8yMV7mc691aTqjNxZ9zPHOdwpkL_e11j', 'srt')
  with open('/Users/demouser/misc_project/yolo_music_maker/srt_captions', 'w') as cptn:
      cptn.write(str(captions))
