import smtplib
from email.message import EmailMessage

# Email details
sender_email = "abhishek2005.siva@gmail.com"
receiver_email = "cs23b2005@iiitdm.ac.in"
app_password = "Letmein2272"  # NOT your regular Gmail password

subject = "Test Email from Python"
body = "Hello, this is a test email sent using Python!"

# Set up the email
msg = EmailMessage()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject
msg.set_content(body)

# Sending the email using Gmail's SMTP server
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, app_password)
        smtp.send_message(msg)
        print("Email sent successfully!")
except Exception as e:
    print("Failed to send email:", e)
