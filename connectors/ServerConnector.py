import sib_api_v3_sdk, requests
from configs.ServerConfig import logger, email_configuration, SENDER_EMAIL, SENDER_NAME
from sib_api_v3_sdk.rest import ApiException
from sib_api_v3_sdk import CreateContact, SendSmtpEmail

def send_email(email, request_id):
    api_client = sib_api_v3_sdk.ApiClient(email_configuration)
    contact_api = sib_api_v3_sdk.ContactsApi(api_client)
    email_api = sib_api_v3_sdk.TransactionalEmailsApi(api_client)

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
        logger.info(f"{request_id} - sending email...")
        contact_api.create_contact(contact)
        logger.debug(f"{request_id} - {user_email} added or updated.")
    except ApiException as e:
        if e.status == 400 and "already exist" in str(e.body):
            logger.debug(f"{request_id} - {user_email} already exists.")
        else:
            logger.exception(f"{request_id} - error while creating the contact")
            return

    # 2. Sending email
    email = SendSmtpEmail(
        to=[{"email": user_email, "name": user_first_name}],
        subject=email["subject"],
        html_content=email['html_content'],
        sender={"name": SENDER_NAME, "email": SENDER_EMAIL}
    )

    try:
        response = email_api.send_transac_email(email)
        logger.debug(f"{request_id} - email sent to '{user_email}'. ID: '{response.message_id}'")
    except ApiException:
        logger.exception(f"{request_id} - an error occurred while trying to sending email")

def send_push_notification(expo_push_token, title, body, request_id):
    message = {
        "to": expo_push_token,
        "sound": "default",
        "title": title,
        "body": body,
        "data": {},
    }

    try:
        requests.post("https://exp.host/--/api/v2/push/send", json=message, timeout=5)
    except:
        logger.exception(f"{request_id} - an error occurred while trying to sending push notification")
