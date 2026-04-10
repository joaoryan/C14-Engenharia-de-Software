import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_notification():
    email_sender = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASS")
    email_receiver = os.getenv("EMAIL_RECEIVER") 
    
    test_status = os.getenv("TEST_STATUS", "Desconhecido")
    build_status = os.getenv("BUILD_STATUS", "Desconhecido")

    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = f"Status: - Testes: {test_status}"

    body = f"""
    O pipeline executou.
    
    Testes: {test_status}
    
    Relatório de testes segue anexo.
    """
    msg.attach(MIMEText(body, 'plain'))

    files_to_attach = ["report.html"] 

    for file_path in files_to_attach:
        if os.path.exists(file_path):
            with open(file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {os.path.basename(file_path)}",
                )
                msg.attach(part)
        else:
            print(f"Erro: {file_path} não encontrado.")

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(email_sender, email_password)
        
        receivers_list = [r.strip() for r in email_receiver.split(",")]
        
        server.sendmail(email_sender, receivers_list, msg.as_string())
        server.quit()
        print("Notificacao enviada com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    send_notification()
    