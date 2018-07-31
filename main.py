import requests
import xml.etree.ElementTree as ET
import syll_counter
# import curses
# from curses.ascii import isdigit

# This is what I installed to do syllable counting
# pip install nltk
# cd /Applications/Python\ 2.7/
# ./Install\ Certificates.command
# install the cmudict entry

# import nltk
# from nltk.corpus import cmudict
#
# def count_syllables(syll_str):
#     sylls = 0
#     d = cmudict.dict()
#     word_list = syll_str.split()
#     for word in word_list:
#         word = word.replace('\\u2019s', '\'').replace('\\u2026', '...')
#         if not word:
#             continue
#         try:
#             word_syll = [len(list(y for y in x if isdigit(y[-1]))) for x in d[word.lower()]]
#             print(word_syll)
#             return
#         except Exception as e:
#             print(e)
#     return sylls

def count_syllables(syll_str):
    sylls = 0
    words = []
    word_list = syll_str.split()
    for word in word_list:
        word = word.replace('\\u2019s', '\'').replace('\\u2026', '...')
        word_sylls = syll_counter.sylco(word)
        words.append((word, word_sylls))
        sylls += word_sylls
    return sylls, words


def get_caption_to_timing_list(caption_resp_str):
    caption_ls = []
    print(caption_resp_str)
    tree = ET.fromstring(caption_resp_str)
    for branch in tree:
        sylls, word_list = count_syllables(branch.text)
        caption_ls.append(
            {'caption': branch.text.encode(encoding='UTF-8',errors='ignore'),
             'start': branch.attrib.get('start'),
             'duration': branch.attrib.get('dur'),
             'syllables': sylls,
             'word_sylls_list': word_list})
    return caption_ls

def get_captions(video_id):
  request_query = 'http://video.google.com/timedtext?lang=en&v={}'.format(
    video_id)
  resp = requests.get(request_query)
  if not resp.status_code == 200:
      raise CaptionError('request')
  return get_caption_to_timing_list(resp.content)

if __name__ == '__main__':
    captions = get_captions(video_id='M7FIvfx5J10')
    for caption_dict in captions:
        print(caption_dict)
