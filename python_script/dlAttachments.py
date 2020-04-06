# Saves of .jpeg image files from google gmail account (only scans google nest gmail email notifications coming from google nest cams) 
# After saving moves email to Thrash if you select that option --Trash True
# Make sure you have IMAP enabled in your gmail settings.
# v1.1 April 4, 2020

import email
import imaplib
import os
import sys
import errno
import mimetypes
import dateutil.tz
import dateutil.parser
import argparse
import netrc


parser = argparse.ArgumentParser(description='This script takes in gmail userid/password and directory to store embedded email jpg files')
parser.add_argument('-d','--dir', help='Attachment directory.', required=True)
parser.add_argument('-t','--thrash', help='Move email to Thrash?.', required=True)
args = parser.parse_args()

HOST = 'your.gmail.host.name'
secrets = netrc.netrc()

userName, account,  passwd = secrets.authenticators( HOST )

# sys.exit()
 
thrash_email = args.thrash
attach_dir = args.dir
nbr_deleted_emails = 0

if not os.path.exists(attach_dir):
   os.mkdir(attach_dir)



try:
    imapSession = imaplib.IMAP4_SSL('imap.gmail.com')
    typ, accountDetails = imapSession.login(userName, passwd)
    print('logged in')
    if typ != 'OK':
        print 'Not able to sign in!'
        raise
    
    imapSession.select('[Gmail]/All Mail')
    typ, data = imapSession.search(None, 'ALL')
    if typ != 'OK':
        print 'Error searching Inbox.'
        raise
    
    # Iterating over all emails
    for msgId in data[0].split():
        typ, messageParts = imapSession.fetch(msgId, '(RFC822)')
       
        if typ != 'OK':
            print 'Error fetching mail.'
            raise

        emailBody = messageParts[0][1]
        mail = email.message_from_string(emailBody)
        
        for part in mail.walk():
            date = mail["Date"]
            dt = dateutil.parser.parse(date)
            file_name_tag = dt.astimezone(dateutil.tz.tzlocal()).strftime('%Y%m%d_%I%M%S')
            

            if part.get_content_maintype() == 'image' and part.get_content_type() == 'image/jpeg':
               image = part.get_filename().split('.')
               image_name =  image[0] + '_' + file_name_tag + "." + image[1]
               
               open(attach_dir + '/' + image_name, 'wb').write(part.get_payload(decode=True))
            else:
                continue
        if thrash_email:
           imapSession.store(msgId, '+X-GM-LABELS', '\\Trash') 
           nbr_deleted_emails = nbr_deleted_emails + 1
    if thrash_email:
       imapSession.expunge()
       print('Number of emails processed and deleted: ', nbr_deleted_emails)
       
    imapSession.close()
    imapSession.logout()
except :
    print 'Not able to download all attachments.'