import sib_api_v3_sdk
from configs.ServerConfig import logger, email_configuration, SENDER_EMAIL, SENDER_NAME
from sib_api_v3_sdk.rest import ApiException
from sib_api_v3_sdk import CreateContact, SendSmtpEmail

from templates import otp

def send_email(email, request_id):
    try:
        api_client = sib_api_v3_sdk.ApiClient(email_configuration)
        contact_api = sib_api_v3_sdk.ContactsApi(api_client)
        email_api = sib_api_v3_sdk.TransactionalEmailsApi(api_client)

        logger.info(f"{request_id} - Sending email: {email}")
        user_email = email["user_email"]
        user_first_name = email["user_firstname"]
        user_last_name = email["user_lastname"]

        # 1. add or update the contact
        contact = CreateContact(
            email=user_email,
            attributes={"FIRSTNAME": user_first_name, "LASTNAME": user_last_name},
            update_enabled=True
        )

        try:
            contact_api.create_contact(contact)
            logger.info(f"{request_id} - {user_email} added or updated.")
        except ApiException as e:
            if e.status == 400 and "already exist" in str(e.body):
                logger.info(f"{request_id} - {user_email} already exists.")
            else:
                logger.error(f"{request_id} - {e}")
                return

        # 2. Enviar el correo
        email = SendSmtpEmail(
            to=[{"email": user_email, "name": user_first_name}],
            subject=email["subject"],
            html_content=otp.render_otp_email(otp_code=email['otp_token']),
            sender={"name": SENDER_NAME, "email": SENDER_EMAIL}
        )

        try:
            response = email_api.send_transac_email(email)
            logger.info(f"Email enviado a {user_email}. ID: {response['message_id']}")
        except ApiException as e:
            print(f"Error al enviar el correo: {e}")

    except:
        logger.exception(f"{request_id} - there was an error while trying to send email")