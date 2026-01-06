from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from src.config import settings


conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


async def send_verification_email(email: str, token: str):
    protocol = "https" if "tuitrox" in settings.DOMAIN_NAME else "http"
    url = f"{protocol}://{settings.DOMAIN_NAME}/verify?token={token}"

    html = f"""
    <h1>Подтверждение регистрации Myriad</h1>
    <p>Привет! Спасибо за регистрацию.</p>
    <p>Нажми на кнопку ниже, чтобы активировать аккаунт:</p>
    <a href="{url}" style="padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none;">Подтвердить Email</a>
    <br><br>
    <p>Или перейди по ссылке: {url}</p>
    """

    message = MessageSchema(
        subject="Myriad: Подтверждение почты",
        recipients=[email],
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)