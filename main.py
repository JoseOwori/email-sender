from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
import aiosmtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

current_dir = os.path.dirname(__file__)
dotenv_path = os.path.join(current_dir, '.env')
load_dotenv(dotenv_path)

host: str = os.getenv("SMTP_HOST")
port: int = os.getenv("SMTP_PORT")
user: str = os.getenv("SMTP_USER")
password: str = os.getenv("SMTP_PASSWORD")
receiver: str = os.getenv("RECEIVER")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EmailSchema(BaseModel):
    name: str
    email: EmailStr
    message: str


async def send_email(email_data: EmailSchema):
    message = EmailMessage()
    message["From"] = "rhodinemma10@gmail.com"
    message["To"] = receiver
    message["Subject"] = f"Message from {email_data.name}"

    content = f"""
    You have received a new message from {email_data.name} ({email_data.email}).

    Message:
    {email_data.message}
    """
    message.set_content(content)

    # SMTP configuration
    smtp_host = host
    smtp_port = 587
    smtp_user = user
    smtp_password = password

    try:
        await aiosmtplib.send(
            message,
            hostname=smtp_host,
            port=smtp_port,
            username=smtp_user,
            password=smtp_password,
            start_tls=True,
        )
    except aiosmtplib.SMTPException as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to send email: {e}")


@app.post("/send-email/")
async def send_email_endpoint(email: EmailSchema):
    await send_email(email)
    return {"status": "success", "message": "Email sent successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=4000)
