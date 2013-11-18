#!/usr/bin/env python

import logging
import poplib
import boto.sns
import email

# Logic Steps:
# 1. Conenct to POP3 SSL email account
# 2. If no new email, then exit
# 2a. Else send each message to AWS SNS subscribers
# 3. Delete sent emails from inbox
# Rinse and repeat as cron job...

l = logging.basicConfig(filename='sns.log', level=logging.DEBUG)
logger = logging.getLogger(l)

topicarn = "Your ARN Here"

try:
    # 1. Connect to POP email account
    pop_conn = poplib.POP3_SSL('POP server address here')
    pop_conn.user('Email address here')
    pop_conn.pass_('Email password here')

    messages = [pop_conn.retr(i)
                for i in range(1, len(pop_conn.list()[1]) + 1)]
    messages = ["\n".join(mssg[1]) for mssg in messages]
    #messages = [parser.Parser().parsestr(mssg) for mssg in messages]

    # Print out some POP connection details for logging.
    num_mails = len(pop_conn.list()[1])
    logger.info('POP LIST: %s' % str(pop_conn.list()))
    logger.info("NUMBER OF MAILS: %s" % str(num_mails))
    idlist = pop_conn.uidl()[1]
    logger.info("ID-List: %s" % str(idlist))
    toplist = pop_conn.top
    logger.info("POP Top List: %s" % str(toplist))

    # 2. Check for new emails
    if num_mails > 0:

        # Connect to SNS service
        try:
            conn = boto.sns.connect_to_region('us-east-1')
            logger.info('connection successful...')
        except Exception, ex:
            logger.info('error connection to region' % str(ex))

        try:
            # Go through messages from email service
            for message in messages:
                msg = email.message_from_string(message)
                # this is kind of a hack to find the actual message text
                block = 0
                for part in msg.walk():
                    # 'text' appears twice in content maintype so we need to
                    # do a check for that so we only get the message content
                    if part.get_content_maintype() == 'text' and block == 0:
                        block = 1
                        content = part.get_payload()
                        content = content.decode("quopri_codec")
                        # print message['subject']
                        logger.info('Message Content: %s' % str(content))

                        # 2a. Publish email message to clients with SNS
                        try:
                            publication = conn.publish(topicarn, content)
                            logger.info('publication successful!')
                        except Exception, ex:
                            logger.info('error pushing publication:' % str(ex))
        except Exception, ex:
            logger.info('Message error %s' % str(ex))

        # 3. Delete emails
        logger.info('Deleting messages..')
        for msgid in xrange(1, len(idlist) + 1):
            logger.info('Deleting message id: %s' % str(msgid))
            pop_conn.dele(msgid)

    else:
        logger.info('no new mails')

    pop_conn.quit()
except Exception, ex:
    logger.error('ERROR %s' % ex)
