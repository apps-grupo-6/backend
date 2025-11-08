import datetime, jwt

from flask import g
from configs.ServerConfig import logger

from utils import UsersUtils, AuthUtils, OtpUtils
from configs import AuthConfig
from repositories import AuthRepository, UsersRepository, OtpRepository
from templates import UserTemplate, OtpTemplate


def login(model, request_id):
    username = model["username"]
    password = model["password"]
    TYPE = "LOGIN"

    logger.info(f"{request_id} - '{username}' is trying to login")
    get_user_info = AuthRepository.get_username_info(username=username,
                                                     request_id=request_id,
                                                     errors_code_map={
                                                         "database_error_code": "0500",
                                                         "invalid_data_error_code": "0404"
                                                     })
    if get_user_info["error"]:
        return {}

    user_id = get_user_info['data']['user_id']
    g.user_id = user_id

    logger.info(f"{request_id} - checking password...")
    if not UsersUtils.verify_password(plain_password=password, hashed_password=get_user_info["data"]["password"]):
        logger.error(f"{request_id} - the password is incorrect")
        g.response_code = "0410"
        return {}

    if not get_user_info['data']['email_verified']:
        logger.error(f"{request_id} - user's account is not verified")
        g.response_code = "0411"
        return {}

    user_contact = UsersRepository.get_user_contact_information(user_id=user_id,
                                                                request_id=request_id,
                                                                errors_code_map={
                                                                    "database_error_code": "0501",
                                                                    "invalid_data_error_code": "0405"
                                                                })
    if user_contact["error"]:
        return {}

    otp_token = OtpUtils.generate_and_save_otp(user_id=user_id,
                                               otp_type=TYPE,
                                               request_id=request_id,
                                               errors_code_map={"database_error_code": "0502"})


    OtpUtils.generate_otp_mail(otp_token=otp_token["data"],
                               type=TYPE,
                               user_contact=user_contact)

    logger.info(f"{request_id} - first step login was done successfully")
    g.response_code = "0200"
    return {}

def login_otp(model, request_id):
    username = model["username"]
    otp_token = model["otp_token"]
    TYPE = "LOGIN"

    exists_username = UsersRepository.get_user_id_by_username(username=username,
                                                              request_id=request_id,
                                                              errors_code_map={
                                                                  "database_error_code": "0500",
                                                                  "invalid_data_error_code": "0404"
                                                              })

    if exists_username["error"]:
        return {}

    user_id = exists_username["data"]["id"]
    g.user_id = user_id

    get_user_token = OtpRepository.check_otp_token_by_user_id(user_id=user_id,
                                                              otp_token=otp_token,
                                                              type=TYPE,
                                                              request_id=request_id,
                                                              errors_code_map={
                                                                  "database_error_code": "0501",
                                                                  "invalid_data_error_code": "0405"
                                                              })
    if get_user_token["error"]:
        return {}

    logger.info(f"{request_id} - checking if otp token is valid...")
    if OtpUtils.check_token_expired(checked=get_user_token, request_id=request_id):
        g.response_code = "0410"
        return {}

    deleted = OtpRepository.delete_otp(user_id=user_id,
                                       otp_token=otp_token,
                                       type=TYPE,
                                       request_id=request_id,
                                       errors_code_map={"database_error_code": "0502"})

    if deleted["error"]:
        return {}

    last_login = AuthRepository.update_user_last_login(user_id=user_id,
                                                       request_id=request_id,
                                                       errors_code_map={"database_error_code": "0503"})

    if last_login["error"]:
        return {}

    logger.info(f"{request_id} - generating jwt token...")
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=AuthConfig.jwt_exp_delta_seconds),
        "user_id": user_id
    }

    token = jwt.encode(payload, AuthConfig.jwt_secret, algorithm=AuthConfig.jwt_algorithm)

    logger.info(f"{request_id} - second step login finished successfully. User has been authenticated")
    g.response_code = "0200"
    return {
        "data": {
            "token": token,
        }
    }

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

    exists_username = UsersRepository.get_user_id_by_username(username=username,
                                                              request_id=request_id,
                                                              errors_code_map={
                                                                  "database_error_code": "0500",
                                                                  "invalid_data_error_code": "0404"
                                                              })

    if exists_username["error"]:
        return {}

    user_id = exists_username["data"]["id"]
    g.user_id = user_id

    user_contact = UsersRepository.get_user_contact_information(user_id=user_id,
                                                                request_id=request_id,
                                                                errors_code_map={"database_error_code": "0501"})

    if user_contact["error"]:
        return {}

    otp_token = OtpUtils.generate_and_save_otp(user_id=user_id,
                                               otp_type="RECOVER",
                                               request_id=request_id,
                                               errors_code_map={"database_error_code": "0502"})
    g.send_email_data = {
        "subject": "Recuperación de cuenta",
        "user_email": user_contact["data"]["contact_email"],
        "user_firstname": user_contact["data"]["first_name"],
        "user_lastname": user_contact["data"]["last_name"],
        "html_content": OtpTemplate.render_recover_otp_email(first_name=user_contact["data"]["first_name"],
                                                             last_name=user_contact["data"]["last_name"],
                                                             otp_code=otp_token["data"])
    }

    g.response_code = "0200"
    return {}

def recover_account_otp(model, request_id):
    username = model["username"]
    new_password = model["new_password"]
    otp_token = model["otp_token"]
    TYPE = "RECOVER"

    exists_username = UsersRepository.get_user_id_by_username(username=username,
                                                              request_id=request_id,
                                                              errors_code_map={
                                                                  "database_error_code": "0500",
                                                                  "invalid_data_error_code": "0404"
                                                              })

    if exists_username["error"]:
        return {}

    user_id = exists_username["data"]["id"]
    g.user_id = user_id
    checked = OtpRepository.check_otp_token_by_user_id(user_id=user_id,
                                                       otp_token=otp_token,
                                                       type=TYPE,
                                                       request_id=request_id,
                                                       errors_code_map={
                                                           "database_error_code": "0501",
                                                           "invalid_data_error_code": "0405"
                                                       })

    if checked["error"]:
        return {}

    if OtpUtils.check_token_expired(checked=checked, request_id=request_id):
        g.response_code = "0410"
        return {}

    hashed_password = UsersUtils.hash_password(plain_password=new_password)
    updated = AuthRepository.set_new_password(user_id=user_id,
                                              new_password=hashed_password,
                                              request_id=request_id,
                                              errors_code_map={"database_error_code": "0502"})

    if updated["error"]:
        return {}

    deleted = OtpRepository.delete_otp(user_id=user_id,
                                       otp_token=otp_token,
                                       type=TYPE,
                                       request_id=request_id,
                                       errors_code_map={"database_error_code": "0503"})

    if deleted["error"]:
        return {}

    g.response_code = "0200"
    return {}

def confirm_account(model, request_id):
    username = model["username"]
    verification_code = model["otp_token"]
    TYPE = "REGISTRATION"

    logger.info(f"{request_id} - confirming account for username: '{username}'...")
    registration_data = OtpRepository.check_otp_token_by_username(username=username,
                                                                  otp_token=verification_code,
                                                                  type=TYPE,
                                                                  request_id=request_id,
                                                                  errors_code_map={
                                                                      "database_error_code": "0500",
                                                                      "invalid_data_error_code": "0404"
                                                                  })
    
    if registration_data["error"]:
        return {}
    
    otp_info = registration_data["data"]
    user_id = otp_info["user_id"]
    g.user_id = user_id
    if OtpUtils.check_token_expired(checked=registration_data, request_id=request_id):
        g.response_code = "0410"
        return {}
    
    verified = UsersRepository.mark_user_as_verified(user_id=user_id,
                                                     request_id=request_id,
                                                     errors_code_map={"database_error_code": "0501"})
    
    if verified["error"]:
        return {}
    
    OtpRepository.delete_otp(user_id=user_id,
                             otp_token=verification_code,
                             type=TYPE,
                             request_id=request_id,
                             errors_code_map={"database_error_code": "0502"})

    user_contact = UsersRepository.get_user_contact_information(user_id=user_id,
                                                                request_id=request_id,
                                                                errors_code_map={"database_error_code": "0503"})

    if user_contact["error"]:
        return {}

    g.send_email_data = {
        "subject": "¡Bienvenido/a! Tu cuenta ha sido activada",
        "user_email": user_contact["data"]["contact_email"],
        "user_firstname": user_contact["data"]["first_name"],
        "user_lastname": user_contact["data"]["last_name"],
        "html_content": UserTemplate.render_register_email(first_name=user_contact["data"]["first_name"],
                                                           last_name=user_contact["data"]["last_name"],
                                                           username=username)
    }
    
    logger.info(f"{request_id} - account confirmed successfully")
    g.response_code = "0200"
    return {}