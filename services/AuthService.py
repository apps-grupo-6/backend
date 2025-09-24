import datetime, jwt

from flask import g
from configs.ServerConfig import logger

from utils import UsersUtils, AuthUtils, OtpUtils
from configs import AuthConfig
from repositories import AuthRepository, UsersRepository, OtpRepository
from services import UsersService
from templates import UserTemplate

def login(model, request_id):
    username = model["username"]
    password = model["password"]

    logger.info(f"{request_id} - '{username}' is trying to login")
    get_user_info = AuthRepository.get_username_info(username=username,
                                                     request_id=request_id,
                                                     errors_code_map={
                                                         "database_error_code": "0500",
                                                         "invalid_data_error_code": "0404"
                                                     })
    if get_user_info["error"]:
        return {}

    if not get_user_info['data']['email_verified']:
        logger.error(f"{request_id} - user's account is not verified")
        g.response_code = "0412"
        return {}

    user_id = get_user_info['data']['user_id']
    g.user_id = user_id

    logger.info(f"{request_id} - checking password...")
    if not UsersUtils.verify_password(plain_password=password, hashed_password=get_user_info["data"]["password"]):
        logger.error(f"{request_id} - the password is incorrect")
        g.response_code = "0410"
        return {}

    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=AuthConfig.jwt_exp_delta_seconds),
        "user_id": user_id
    }

    logger.info(f"{request_id} - generating jwt token...")
    token = jwt.encode(payload, AuthConfig.jwt_secret, algorithm=AuthConfig.jwt_algorithm)

    logger.info(f"{request_id} - first step login was done successfully")
    g.response_code = "0200"
    return {
        "data": {
            "token": token
        }
    }

def login_otp(model, user_id, request_id):
    otp_token = model["otp_token"]
    TYPE = "LOGIN"

    get_user_token = AuthRepository.check_otp_token(user_id=user_id,
                                                    otp_token=otp_token,
                                                    type=TYPE,
                                                    request_id=request_id,
                                                    errors_code_map={
                                                        "database_error_code": "0500",
                                                        "invalid_data_error_code": "0404"
                                                    })
    if get_user_token["error"]:
        return {}

    logger.info(f"{request_id} - checking if otp token is valid...")
    if OtpUtils.check_token_expired(checked=get_user_token):
        logger.error(f"{request_id} - user's login otp_token is expired")
        g.response_code = "0410"
        return {}

    deleted = OtpUtils.delete_otp_token(user_id=user_id,
                                        otp_token=otp_token,
                                        type=TYPE,
                                        request_id=request_id,
                                        errors_code_map={"database_error_code": "0501"})

    if not deleted:
        return {}

    last_login = AuthRepository.update_user_last_login(user_id=user_id,
                                                       request_id=request_id,
                                                       errors_code_map={"database_error_code": "0502"})

    if last_login["error"]:
        return {}

    logger.info(f"{request_id} - second login step finished successfully; user has been authenticated")
    g.response_code = "0200"
    return {}

def refresh_token(model, request_id):
    jwt_token = model["jwt_token"]

    logger.info(f"{request_id} - checking if needed to refresh jwt token...")
    decoded = AuthUtils.check_jwt_token(jwt_token)

    if decoded["error"]:
        if decoded["error_code"] == 0:
            logger.error(f"{request_id} - the requested jwt token is valid and did not expire yet")
            g.response_code = "0410"
        else:
            logger.error(f"{request_id} - the requested jwt token is invalid")
            g.response_code = "0411"

        return {}
    else:
        logger.debug(f"{g.request_id} - jwt token is expired (ok)")

    decoded["data"]["exp"] += AuthConfig.jwt_exp_delta_seconds
    refreshed = jwt.encode(decoded, AuthConfig.jwt_secret, algorithm=AuthConfig.jwt_algorithm)

    last_login = AuthRepository.update_user_last_login(user_id=decoded["data"]["user_id"],
                                                       request_id=request_id,
                                                       errors_code_map={"database_error_code": "0500"})

    if last_login["error"]:
        return {}

    g.response_code = "0200"
    return {
        "data": {
            "token": refreshed
        }
    }
def recover_account(model, request_id):
    username = model["username"]
    new_password = model["new_password"]
    otp_token = model["otp_token"]
    TYPE = "RECOVER"

    exists_username = UsersRepository.check_if_username_exists(username=username,
                                                               request_id=request_id,
                                                               errors_code_map={
                                                                   "database_error_code": "0500",
                                                                   "invalid_data_error_code": "0404"
                                                               })

    if exists_username["error"]:
        return {}

    user_id = exists_username["data"]["id"]
    checked = AuthRepository.check_otp_token(user_id=user_id,
                                             otp_token=otp_token,
                                             type=TYPE,
                                             request_id=request_id,
                                             errors_code_map={
                                                 "database_error_code": "0501",
                                                 "invalid_data_error_code": "0405"
                                             })

    if checked["error"]:
        return {}

    if OtpUtils.check_token_expired(checked=checked):
        logger.info(f"{request_id} - user's recovery otp_token is expired")
        g.response_code = "0410"
        return {}

    hashed_password = UsersUtils.hash_password(plain_password=new_password)
    updated = AuthRepository.set_new_password(user_id=user_id,
                                              new_password=hashed_password,
                                              request_id=request_id)

    if not updated:
        logger.critical(f"{request_id} - an error occurred while updating user's password")
        g.response = "0502"
        return {}

    deleted = OtpUtils.delete_otp_token(user_id=user_id,
                                        otp_token=otp_token,
                                        type=TYPE,
                                        request_id=request_id,
                                        errors_code_map={"database_error_code": "0503"})

    if not deleted:
        return {}

    g.response_code = "0200"
    return {}

def confirm_account(username, verification_code, request_id):
    logger.info(f"{request_id} - confirming account for username: {username}")
    
    registration_data = OtpRepository.check_otp_token_by_username(
        username=username,
        otp_token=verification_code,
        type="REGISTRATION",
        request_id=request_id,
        errors_code_map={
            "database_error_code": "0500",
            "invalid_data_error_code": "0404"
        }
    )
    
    if registration_data["error"]:
        logger.error(f"{request_id} - invalid verification code for username: {username}")
        g.response_code = "0404"
        return {}
    
    otp_info = registration_data["data"]
    user_id = otp_info["user_id"]
    
    if otp_info["expires_at"] < datetime.datetime.now():
        logger.error(f"{request_id} - verification code expired for user: {username}")
        g.response_code = "0410"
        return {}
    
    verified = UsersRepository.mark_user_as_verified(
        user_id=user_id,
        request_id=request_id,
        errors_code_map={"database_error_code": "0501"}
    )
    
    if verified["error"]:
        return {}
    
    OtpRepository.delete_otp(
        user_id=user_id,
        otp_token=verification_code,
        type="REGISTRATION",
        request_id=request_id,
        errors_code_map={"database_error_code": "0501"}
    )
    
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=AuthConfig.jwt_exp_delta_seconds),
        "user_id": user_id
    }
    
    token = jwt.encode(payload, AuthConfig.jwt_secret, algorithm=AuthConfig.jwt_algorithm)
    
    user_contact = UsersRepository.get_user_contact_information(
        user_id=user_id,
        request_id=request_id,
        errors_code_map={"database_error_code": "0501"}
    )
    
    # Enviar email de bienvenida
    if not user_contact["error"]:
        g.send_email_data = {
            "subject": "¡Bienvenido/a! Tu cuenta ha sido activada",
            "user_email": user_contact["data"]["contact_email"],
            "user_firstname": user_contact["data"]["first_name"],
            "user_lastname": user_contact["data"]["last_name"],
            "html_content": UserTemplate.render_register_email(
                first_name=user_contact["data"]["first_name"],
                last_name=user_contact["data"]["last_name"],
                username=username
            )
        }
    
    logger.info(f"{request_id} - account confirmed and user logged in successfully")
    g.response_code = "0200"
    return {
        "data": {
            "message": "¡Cuenta verificada exitosamente! Ya estás logueado.",
            "token": token,
            "user": {
                "username": username,
                "first_name": user_contact["data"]["first_name"] if not user_contact["error"] else "",
                "last_name": user_contact["data"]["last_name"] if not user_contact["error"] else "",
                "email": user_contact["data"]["contact_email"] if not user_contact["error"] else ""
            }
        }
    }

def verify_otp_code(username, verification_code, request_id):
    return OtpUtils.handle_otp_verification(username, verification_code, request_id)
