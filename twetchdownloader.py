import requests
from app import db, Twetch
from datetime import datetime, timedelta
from sqlalchemy import exc
from sqlite3 import IntegrityError
import time

db.create_all()


# todo: add init_query vs recursive query

query = '''query MyQuery {
              allPosts(orderBy: CREATED_AT_DESC, first: 20) {
                nodes {
                  createdAt
                  bContent
                  bContentType
                  moneyButtonUserId
                  transaction
                  userId
                  type
                  mediaByPostId {
                    nodes {
                      filename
                    }
                  }
                  userByUserId {
                    icon
                    name
                  }
                }
              }
            }

        '''

url = "https://api.twetch.app/v1/graphql"

if __name__ == '__main__':
    while True:
        try:
            r = requests.post(url, data={'query': query})
            data = r.json()['data']
    
            for post in data['allPosts']['nodes']:
                # post = post['node']
                #print(post)
                try:
                    mbuid = int(post['moneyButtonUserId'])
                except TypeError as e:
                    print("ERROR", e)
                    mbuid = None
    
                filepath = None
                if len(post['mediaByPostId']['nodes']) > 0:
                    filepath = post['mediaByPostId']['nodes'][0]['filename']
    
                print(post["type"])
                print(post['createdAt'])
                if post['type'] != "branch":
                    twetch = Twetch(txid=post['transaction'],
                                    content_type=post['bContentType'],
                                    content_text=post['bContent'],
                                    created_at=datetime.strptime(post['createdAt'], "%Y-%m-%dT%H:%M:%S.%f+02:00") - timedelta(hours=7),
                                    mb_user_id=mbuid,
                                    twetch_user_id=int(post['userId']),
                                    filepath=filepath,
                                    icon_url=post['userByUserId']['icon'],
                                    twetch_username=post['userByUserId']['name'])
                    try:
                        db.session.add(twetch)
                        db.session.commit()
                        print("COMMITTED", post)
                    except exc.IntegrityError as e:
                        db.session.rollback()
                        print("ERROR", e)
                        pass
    
            interval = 120
            print(f'sleeping until {datetime.strftime(datetime.now() + timedelta(seconds=interval), "%H:%M:%S")}')
            time.sleep(interval)
        except:
            print('query failed.. retrying...')