import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from src.config import settings
from src.database import async_session_maker_null_pool
from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DBManager


@celery_instance.task
def validation_email(receiver_email, code):
    sender_email = settings.EMAIL
    receiver_email = receiver_email
    sender_password = settings.SENDER_PASSWORD
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    message = MIMEMultipart("alternative")
    message["Subject"] = "Подтверждение электронной почты"
    message["From"] = sender_email
    message["To"] = receiver_email

    html = f"""\
    <html>
      <body>
        <p>Здравствуйте!<br><br>
           Подтвердите свой адрес электронной почты на bels-company.<br>
           <b>Ваш проверочный код: {code}</b><br><br>
           С уважением, команда bels company.
        </p>
      </body>
    </htm
    """

    part2 = MIMEText(html, "html")

    message.attach(part2)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("Письмо отправлено!")