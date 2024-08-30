from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys, string

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from datetime import date
import datetime

printable = set(string.printable)

if __name__ == "__main__":
    textfile = 'audit.log'
    body = "".join(open(textfile, "r").readlines())
    body = ''.join(filter(lambda x: x in printable, body))

    me = sys.argv[1]
    you = sys.argv[5]

    today = date.today().strftime("%B %d, %Y")
    now = str(datetime.datetime.now().time())

    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'NPM Audit Report for {today}'
    msg['From'] = "Microservices Email Hook"
    msg['To'] = you

    html = f"""\
    <html>
      <head>
        <style>
            code {{
                background-color: #f4f4f4;
                border-left: 3px solid #7f7f7f;
                color: #666;
                page-break-inside: avoid;
                font-size: 15px;
                margin: 1.5em 0;
                padding: 0.5em 10px;
                display: block;
                overflow: auto;
                width: 100%;
                word-wrap: break-word;
            }}
        </style>
    </head>

      <body>
      <h1>NPM Audit Report for <span style="color:blue;">{sys.argv[3]}</span> project.</h1>
      <h3>On {today} at {now}, a commit was pushed to the <span style="color:red;">{sys.argv[4]}</span> branch</h3>
        <code>
           {body}
        </code>
      </body>
    </html>"""

    # Record the MIME type of text/html part
    part = MIMEText(html, 'html')

    # Attach parts into message container.
    msg.attach(part)

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('smtp-mail.outlook.com', 587)

    s.ehlo()
    s.starttls()
    s.login(me, sys.argv[2])
    s.sendmail(me, [you], msg.as_string())
    s.quit()