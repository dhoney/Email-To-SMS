Email-To-SMS
============

Script that sends/publishes Emails to SMS subscribers using Amazon Web Services SNS and a Flask frontend for enrollment.


To run do the following:

Perlimenaries
--------------

1. Have an AWS account.
2. Use the SNS service to create a topic and add subscribers either through the web console or the web subscriber(below). 
You can also use the code in the web subscriber(sns-subscriber.py) to write your own script that handles subscriptions.
3. If your running the publisher on an AWS node then set up one up as well, I used a micro instance and it seemed to handle this just fine.


WebSubscriber
###

1. Get flask installed
2. Enter your topicarn in the file
3. Run flask server: nohup python sns-pulbisher.py &
4. Make sure firewall rules are set and you have an elastic ip (recommended).
5. Go to web page.
6. Enter mobile phone number or email address you wish to subscribe, confirmation will be sent shortly after.
*Note: At the tiem of this writing, SMS only works on east region hosts and US numbers are only supported.

Publisher
###

1. Enter POP3 email and credential details into the sns-publish.py file.
2. Enter topicarn.
3. Run as cronjob. For example to run every 5 minutes: crontab */5 * * * * python sns-publish.py


References and usefull links
####

http://awsadvent.tumblr.com/post/37531769345/simple-notification-service-sns
http://stackoverflow.com/questions/1225586/checking-email-with-python
http://bytes.com/topic/python/answers/627485-way-extract-only-message-pop3