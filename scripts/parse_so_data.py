import os
import csv
import json
from slugify import slugify

DATAFILE = os.path.abspath(os.getcwd() + '/data/stack_overflow_posts.csv')
INDEX = "stack_overflow"

class Post:
    _data = {}

    def __init__(self, raw_row):
        self._data['id'] = raw_row[0] if raw_row[0] else None
        self._data['parent'] = raw_row[3] if raw_row[3] else None
        self._data['created'] = raw_row[4] if raw_row[4] else None
        self._data['deleted'] = raw_row[5] if raw_row[5] else None
        self._data['score'] = int(raw_row[6]) if raw_row[6] else None
        self._data['views'] = int(raw_row[7]) if raw_row[7] else None
        self._data['body'] = raw_row[8] if raw_row[8] else None
        self._data['user_id'] = raw_row[9] if raw_row[9] else None
        self._data['title'] = raw_row[15] if raw_row[15] else None
        self._data['tags'] = self.parse_tags(raw_row[16]) if raw_row[16] else []
        self._data['answers'] = int(raw_row[17]) if raw_row[17] else None
        self._data['comments'] = int(raw_row[18]) if raw_row[18] else None
        self._data['post_type'] = raw_row[23] if raw_row[23] else None
        self._data['url'] = self.create_url(self._data['id'], self._data['title'], raw_row[22])

    def get_control(self):
        return {
            "index": {
                "_index": INDEX,
                "_type": "post",
                "_id": self._data['id']
            }
        }

    def get_document(self):
        return self._data

    def parse_tags(self, tags):
        return str(tags).strip('<>').replace('><', ' ').split()

    def create_url(self, id, title, post_type_code):
        interstitial = 'a' if int(post_type_code) == 2 else 'questions'
        slug = slugify(title) if title else ""
        return "http://stackoverflow.com/{}/{}/{}".format(interstitial, id, slug)

    def __repr__(self, *args, **kwargs):
        return json.dumps(self.get_control()) + "\n" + json.dumps(self.get_document())


with open(DATAFILE) as datafile:
    reader = csv.reader(datafile)
    next(reader, None)
    for row in reader:
        post = Post(row)
        print(post)
