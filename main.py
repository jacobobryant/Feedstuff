from flask import Flask, request, Response
import os
import requests
import time
import json
from replit import db
from apscheduler.schedulers.background import BackgroundScheduler
from feedgen.feed import FeedGenerator
import re

# todo
# fetch only new records (use filterByFormula)
# paginate the atom feed

app = Flask('app')

def fetch():
  headers={'Authorization': 'Bearer ' + os.environ['AIRTABLE_KEY']}
  url = ('https://api.airtable.com/v0/' + os.environ['BASE_ID'] +
      '/' + os.environ['TABLE'])
  offset = None
  keys = set()
  while True:
    params={'pageSize': 1, 'offset': offset}
    time.sleep(0.2)
    result = requests.get(url, headers=headers, params=params).json()
    records = result['records']
    for row in records:
      key = row['createdTime'] + '_' + row['id']
      db[key] = json.dumps(row['fields'])
      keys.add(key)
    offset = result.get('offset')
    if not offset:
      break

  for k in db.keys():
    if k not in keys:
      del db[k]

sched = BackgroundScheduler()
sched.add_job(fetch, 'interval', seconds=300)
sched.start() 
fetch()

@app.route('/')
def feed():
  gen = FeedGenerator()
  gen.id(os.environ['SELF'])
  gen.title(os.environ['TITLE'])
  gen.link(href=os.environ['SELF'], rel='self')
  gen.link(href=os.environ['LINK'], rel='alternate')
  for k in sorted(db.keys()):
    fields = json.loads(db[k])
    if 'URL' not in fields or fields.get('Save for later'):
      continue

    entry = gen.add_entry()
    entry.link(href=fields['URL'])
    entry.id(fields['URL'])
    entry.title(fields.get('Title', fields['URL']))
    entry.updated(k.split('_')[0])

    commentary = fields.get('Commentary')
    desc = fields.get('Description')
    summary = ''
    if commentary:
      summary += commentary
    if commentary and desc:
      summary += "\n\n"
    if desc:
      summary += "> " + desc
    if summary:
      entry.summary(summary)

    tags = [re.sub(r'[^a-z]+', '-', tag.lower())
            for tag in fields.get('Tags', '').split(',')]
    rating = fields.get('Rating')
    if rating:
      tags.append(str(rating) + '-stars')
    for t in tags:
      if t:
        entry.category(term=t)

  body = gen.atom_str(pretty=True)
  return Response(body, mimetype='application/atom+xml')

app.run(host='0.0.0.0', port=8080)