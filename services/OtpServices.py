from configs.ServerConfig import logger
from flask import g
from random import shuffle
import datetime

from templates import OtpTemplate
from repositories import OtpRepository
from utils import UsersUtils

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
    temp = list(request_id[14:20]) # last 6 digits
    shuffle(temp)
    otp_token = "".join(temp)
    logger.info(f"{request_id} - generated OTP: '{otp_token}'")

    otp_token_save = OtpRepository.save_otp(user_id=user_id,
                                            otp_token=otp_token,
                                            type=type,
                                            request_id=request_id,
                                            errors_code_map={"database_error_code": "0502"})

    if otp_token_save["error"]:
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
    else:
        g.send_email_data["subject"] = "Código de recuperación de cuenta"
        g.send_email_data["html_content"] = OtpTemplate.render_account_recovery_email(otp_code=otp_token)

    g.response_code = "0200"
    return {}