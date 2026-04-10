import smtplib
import os
from email.mime.text import MIMEText

def send_notification():
    # As variáveis virão dos Secrets/Variables do GitHub Actions
    email_sender = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASS")
    email_receiver = os.getenv("EMAIL_RECEIVER")
    test_status = os.getenv("TEST_STATUS", "Desconhecido")
    build_status = os.getenv("BUILD_STATUS", "Desconhecido")

    subject = "Status do Pipeline CI/CD - "
    body = f"""
    O pipeline finalizou a execução.
    
    Status dos Testes: {test_status}
    Status do Build: {build_status}
    
    Verifique os relatórios no GitHub Actions.
    """

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email_sender
    msg['To'] = email_receiver

    try:
        # Configuração para Gmail. Se usar outro, altere o smtp.
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(email_sender, email_password)
        server.sendmail(email_sender, [email_receiver], msg.as_string())
        server.quit()
        print("Notificação enviada com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    send_notification()