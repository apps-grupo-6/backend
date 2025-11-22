from flask import g
from configs.ServerConfig import logger

from repositories import OtpRepository, UsersRepository
from utils import OtpUtils, UsersUtils

def create_otp(model, request_id):
    username = model["username"]
    type = model["type"]

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
    checked = OtpRepository.check_if_user_has_active_otp(user_id=user_id,
                                                         type=type,
                                                         request_id=request_id,
                                                         errors_code_map={
                                                             "database_error_code": "0500",
                                                             "invalid_data_error_code": "0410"
                                                         })

    if checked["error"]:
        return {}

    user_contact = UsersRepository.get_user_contact_information(user_id=user_id,
                                                                request_id=request_id,
                                                                errors_code_map={
                                                                    "database_error_code": "0501",
                                                                    "invalid_data_error_code": "0404"
                                                                })

    if user_contact["error"]:
        return {}

    OtpUtils.create_save_and_send_token(user_id=user_id,
                                        type=type,
                                        user_contact=user_contact,
                                        request_id=request_id,
                                        errors_code_map={"database_error_code": "0502"})

    g.response_code = "0201"
    return {}

def resend_otp(model, request_id):
    username = model["username"]
    type = model["type"]

    user_contact = UsersUtils.check_and_get_user_information(username=username,
                                                             request_id=request_id,
                                                             errors_code_map={
                                                                 "database_error_code": "0500",
                                                                 "invalid_data_error_code": "0404"
                                                             })

    if user_contact["error"]:
        return {}

    user_id = user_contact["data"]["user_id"]
    g.user_id = user_id
    checked = OtpRepository.check_if_user_has_active_otp(user_id=user_id,
                                                         type=type,
                                                         request_id=request_id,
                                                         errors_code_map={
                                                             "database_error_code": "0501",
                                                             "invalid_data_error_code": "0410"
                                                         },
                                                         isError=True)


    if checked["error"]: # if user already has an active otp_token with this type, it throws an error
        if checked["ok"]: # it's just to check if it wasn't a database error
            # so, if user has an active otp_token we just resend it
            otp_token = checked["data"]["otp_token"]
            logger.debug(f"{request_id} - found user otp_token with this type: {otp_token}")
            OtpUtils.generate_otp_mail(otp_token=otp_token,
                                       user_contact=user_contact,
                                       type=type)

            g.response_code = "0200"

        return {}

    # if user does not have any active otp_token, we create, save and send a new one
    OtpUtils.create_save_and_send_token(user_id=user_id,
                                        type=type,
                                        user_contact=user_contact,
                                        request_id=request_id,
                                        errors_code_map={"database_error_code": "0502"})

    g.response_code = "0201"
    return {}

def check_otp(model, request_id):
    username = model["username"]
    type = model["type"]
    otp_token = model["otp_token"]

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
                                                       type=type,
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

    g.response_code = "0200"
    return {
        "data": {
            "otp_id": checked["data"]["id"],
        }
    }

def delete_otp(otp_token_id, request_id):
    deleted = OtpRepository.delete_otp(otp_token_id=otp_token_id,
                                       request_id=request_id,
                                       errors_code_map={
                                           "invalid_data_error_code": "0404",
                                           "database_error_code": "0500"
                                       })

    if deleted["error"]:
        return {}

    g.response_code = "0204"
    return {}