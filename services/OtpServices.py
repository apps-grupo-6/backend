from configs.ServerConfig import logger
from flask import g
import datetime

from templates import OtpTemplate
from repositories import OtpRepository, UsersRepository
from utils import UsersUtils, OtpUtils

def create_otp(model, user_id, request_id):
    type = model["type"]
    checked = OtpRepository.check_if_user_has_active_otp(user_id=user_id,
                                                         type=type,
                                                         request_id=request_id,
                                                         errors_code_map={"database_error_code": "0500"})

    if checked["error"]:
        return {}

    logger.info(f"{request_id} - checking if otp_token expired...")
    if checked["data"] and checked["data"]["expires_at"] >= datetime.datetime.now():
        logger.error(f"{request_id} - user's otp_token is not expired, it's not required to proceed")
        g.response_code = "0410"
        return {}


    user_contact = UsersUtils.check_and_get_user_information(user_id=user_id,
                                                             request_id=request_id,
                                                             error_code_maps={
                                                                 "database_error_code": "0501",
                                                                 "invalid_data_error_code": "0204"
                                                             })
    if user_contact["error"]:
        return {}

    logger.info(f"{request_id} - creating a new otp_token...")
    otp_token = OtpUtils.generate_and_save_otp(user_id, type, request_id)
    if not otp_token:
        return {}

    g.send_email_data = {
        "otp_token": otp_token,
        "user_email": user_contact["data"]["contact_email"],
        "user_firstname": user_contact["data"]["first_name"],
        "user_lastname": user_contact["data"]["last_name"]
    }

    if type == "LOGIN":
        g.send_email_data["subject"] = "Código de inicio de sesión"
        g.send_email_data["html_content"] = OtpTemplate.render_login_otp_email(otp_code=otp_token)
    elif type == "REGISTRATION":
        username_data = UsersRepository.get_username_by_user_id(
            user_id=user_id,
            request_id=request_id,
            errors_code_map={"database_error_code": "0500"}
        )
        username = username_data["data"]["username"] if not username_data["error"] else "usuario"
        
        g.send_email_data["subject"] = "Verifica tu cuenta - Código de activación"
        g.send_email_data["html_content"] = OtpTemplate.render_registration_verification_email(
            first_name=user_contact["data"]["first_name"],
            last_name=user_contact["data"]["last_name"],
            username=username,
            otp_code=otp_token
        )
    elif type == "RECOVERY":
        g.send_email_data["subject"] = "Código de recuperación de cuenta"
        g.send_email_data["html_content"] = OtpTemplate.render_recover_otp_email(
            first_name=user_contact["data"]["first_name"],
            last_name=user_contact["data"]["last_name"],
            otp_code=otp_token
        )
    else:
        g.send_email_data["subject"] = "Código de verificación"
        g.send_email_data["html_content"] = OtpTemplate.render_account_recovery_email(otp_code=otp_token)

    g.response_code = "0200"
    return {}
