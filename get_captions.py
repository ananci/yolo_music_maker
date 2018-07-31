class CaptionError(Exception):
    """Exceptions around getting youtube captions."""

def get_caption_id(caption_resp):
    # find the id of the caption in en language
    for item in ddict['items']:
        snippet = item.get('snippet')
        if not snippet:
            continue
        if snippet.get('language') == 'en':
            id = item.get('id')
            video_id = snippet.get('videoId')
            if id:
                return id, video_id
    raise CaptionError('No en captions were found for video: {}'.format(snippet.get('videoId')))


if __name__ == '__main__':
  with open('caption_list_data', 'r') as cld:
      data = cld.read()
  ddict = eval(data)
  print(get_caption_id(ddict))
