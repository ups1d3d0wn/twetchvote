from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import requests
import json
import os
import sys


sys.path.insert(0, os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Twetch(db.Model):
    txid = db.Column(db.String(64), primary_key=True, unique=True, nullable=False)
    content_type = db.Column(db.String(20), nullable=False)
    content_text = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, nullable=False)
    mb_user_id = db.Column(db.Integer, nullable=False)
    twetch_user_id = db.Column(db.Integer, nullable=False)
    filepath = db.Column(db.String(100))
    icon_url = db.Column(db.String(180))
    twetch_username = db.Column(db.String(50))
    score = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Twetch {self.txid}>'


class Vote(db.Model):
    txid = db.Column(db.String(64), primary_key=True, nullable=False)
    voted_item_txid = db.Column(db.String(64), nullable=False)
    vote_type = db.Column(db.Boolean, nullable=False)
    datetime_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Vote {self.txid}>'


@app.route('/', methods=['GET'])
def index():
    twetches = Twetch.query.order_by(Twetch.score.desc()).order_by(Twetch.created_at.desc()).filter(Twetch.created_at > datetime.now()-timedelta(days=1)).limit(50)

    return render_template('index.html', twetches=twetches)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    # print(json.dumps(data, indent=2))
    print(data['payment']['status'])
    if data['secret'] != 'top-secret-webhook-phrase':
        print("wrong secret!!!!!!!!!!!!!!!!!!!")
    elif data['payment']['status'] == 'RECEIVED':
        data = data['payment']
        
        correct_outputs = 0
        outputs = data['paymentOutputs']
        for output in outputs:
            if output['to'] == "bigriz@moneybutton.com" and float(output['amountUsd']) >= 0.02:
                correct_outputs += 1
            elif output['to'] == "ins1d30ut@moneybutton.com" and float(output['amountUsd']) >= 0.02:
                correct_outputs += 1
        if correct_outputs >= 2:
            
            if data["buttonId"] == 'upvote':
                vote = Vote(txid=data['txid'], voted_item_txid=data['buttonData'], vote_type=True)
                twetch = db.session.query(Twetch).get(data['buttonData'])
                twetch.score += 1
                # db.session.commit()
                print('upvoted')
    
            elif data["buttonId"] == 'downvote':
                vote = Vote(txid=data['txid'], voted_item_txid=data['buttonData'], vote_type=False)
                twetch = db.session.query(Twetch).get(data['buttonData'])
                twetch.score -= 1
                # db.session.commit()
                print('downvoted')
            try:
                db.session.add(vote)
                db.session.commit()
                return '', 200
            except:
                raise
                return "There was an error voting. Please contact the site admin."
        else:
            print("WRONG OUTPUTS")


    return '', 200
