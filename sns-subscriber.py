#!/usr/bin/env python

import logging
import boto.sns
from flask import Flask
from flask import request
from flask import render_template
# Logic Steps:


l = logging.basicConfig(filename='sns-sub.log', level=logging.DEBUG)
logger = logging.getLogger(l)

topicarn = "Your ARN Here"


app = Flask(__name__)


@app.route('/')
def sns_subscribe():
    return render_template('sns-subscribe-form.html')


@app.route('/', methods=['POST'])
def sns_subscribe_post():
    text = request.form['text']
    c = boto.sns.connect_to_region("us-east-1")
    if '@' in text:
        subscription = c.subscribe(topicarn, 'email', text)
        # print subscription
        response = 'Email subscription sent to: ' + \
            str(text) + str(subscription)
        # print response
        logger.info(response)
        return response
    else:
        subscription = c.subscribe(topicarn, 'sms', text)
        # print subscription
        response = 'Mobile SMS subscription sent to: ' + \
            str(text) + str(subscription)
        # print response
        logger.info(response)
        return response


if __name__ == '__main__':
    app.run(debug=True)
