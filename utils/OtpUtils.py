import datetime
from random import shuffle

from flask import g
from configs.ServerConfig import logger

from repositories import OtpRepository
from templates import OtpTemplate

def check_token_expired(checked, request_id):
    expires_at = checked["data"]["expires_at"]

    logger.info(f"{request_id} - checking if otp_token expired...")
    if expires_at < datetime.datetime.now():
        logger.debug(f"{request_id} - verification code expired")
        return True

    logger.debug(f"{request_id} - otp_token did not expire yet...")
    return False

def create_save_and_send_token(user_id, type, user_contact, request_id, errors_code_map):
    otp_token = generate_and_save_otp(user_id=user_id,
                                      otp_type=type,
                                      request_id=request_id,
                                      errors_code_map=errors_code_map)
    if otp_token["error"]:
        return {}

    otp_token = otp_token["data"]
    generate_otp_mail(otp_token=otp_token,
                      type=type,
                      user_contact=user_contact)

def generate_otp_mail(otp_token, type, user_contact):
    g.send_email_data = {
        "otp_token": otp_token,
        "user_email": user_contact["data"]["contact_email"],
        "user_firstname": user_contact["data"]["first_name"],
        "user_lastname": user_contact["data"]["last_name"]
    }

    if type == "LOGIN":
        g.send_email_data["subject"] = "Código de inicio de sesión"
        g.send_email_data["html_content"] = OtpTemplate.render_login_otp_email(otp_code=otp_token)
    elif type == "RECOVER":
        g.send_email_data["subject"] = "Código de recuperación de cuenta"
        g.send_email_data["html_content"] = OtpTemplate.render_recover_otp_email(
            first_name=user_contact["data"]["first_name"],
            last_name=user_contact["data"]["last_name"],
            otp_code=otp_token
        )
    elif type == "REGISTRATION":
        g.send_email_data["subject"] = "Código de activación de cuenta"
        g.send_email_data["html_content"] = OtpTemplate.render_registration_verification_email(
            otp_code=otp_token,
            first_name=user_contact["data"]["first_name"],
            last_name=user_contact["data"]["last_name"],
            username=user_contact["data"]["username"]
        )

def generate_otp(otp_type, request_id):
    """Helper reutilizable para generar OTP"""

    logger.info(f"{request_id} - creating a new otp_token with type: '{otp_type}'...")
    temp = list(request_id[14:20])
    shuffle(temp)
    otp_token = "".join(temp)
    expires_at = datetime.datetime.now() + datetime.timedelta(minutes=15)
    logger.debug(f"{request_id} - generated new OTP: '{otp_token}'")

    return {
        "otp_token": otp_token,
        "expires_at": expires_at
    }

def generate_and_save_otp(user_id, otp_type, request_id, errors_code_map):
    """Helper reutilizable para generar y guardar OTP"""
    result = generate_otp(otp_type=otp_type, request_id=request_id)
    otp_token = result["otp_token"]

    otp_token_save = OtpRepository.save_otp(user_id=user_id,
                                            otp_token=otp_token,
                                            type=otp_type,
                                            request_id=request_id,
                                            errors_code_map=errors_code_map)

    if otp_token_save["error"]:
        return {"error": True}

    otp_token_save["data"] = otp_token
    return otp_token_save