from django.shortcuts import render
import datetime
import email
import imaplib


def QsMailService(request):
    email_id = "hanumanthareddy2345@gmail.com"
    email_pwd = "reddy123"

    # configure the IMAP
    mail = imaplib.IMAP4_SSL('imap.secureserver.net')
    mail.login(email_id, email_pwd)

    # getting the record
    mail.list()
    mail.select('inbox')
    result, data = mail.uid('search', None, "ALL")  # (ALL/UNSEEN)

    # finding out the last 3 mails
    total_mails = len(data[0].split())
    first_email_id = total_mails - 3
    last_email_id = total_mails

    email_list = []
    for x in range(first_email_id, last_email_id):
        latest_email_uid = data[0].split()[x]
        result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = email_data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)

        # Header Details
        date_tuple = email.utils.parsedate_tz(email_message['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
            local_message_date = "%s" % (str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))
        email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
        email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
        subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))

        # Body details
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                test_body = str(body.decode('utf-8'))
        email_list.append({'From': email_from, 'to': email_to, 'date': local_message_date, 'Subject': subject, 'body': test_body})
    return render(request, 'index.html', {'context': email_list})