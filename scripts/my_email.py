import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email_with_code(user_email, code):
    mail_content = "Thanks for choosing BRIO,\nyou can find your result using the following identifier:\n" + code + "\n\n\nBest regards,\nBRIO Team"
    # The mail addresses and password
    sender_address = 'email@email.com'
    sender_pass = 'password'
    receiver_address = user_email
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'BRIO Team: your results'  # The subject line
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')
