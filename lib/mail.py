import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send(server, port, sender, receiver, subject, body):

    assert server, "Server address cannot be null or empty."
    assert port, "Port cannot be null or empty."
    assert sender, "Sender cannot be null or empty."
    assert receiver, "Receiver cannot be null or empty."
    assert subject, "Subject cannot be null or empty."
    assert body, "Body cannot be null or empty."

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    # Connect to SMTP server
    try:
        server = smtplib.SMTP(server, port)  # Example: smtp.gmail.com for Gmail
        server.sendmail(sender, receiver, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
    finally:
        # Close the SMTP server connection
        server.quit()