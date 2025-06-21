import smtplib
from email.mime.text import MIMEText

def send_email_alert(threat_type, timestamp, to_email):
    sender = "tve24csis06@cet.ac.in"
    password = "bvnr pzhn kplu ccgz"  # Not your Gmail password – see below
    subject = f"🚨 IoT Threat Detected: {threat_type}"
    body = f"A threat of type **{threat_type}** was detected at {timestamp}."
    print("dhaneesh")
    print(to_email)
    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to_email

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender, password)
        server.sendmail(sender, [to_email], msg.as_string())
        server.quit()
        print("✅ Email sent.")
    except Exception as e:
        print("❌ Email failed:", e)
