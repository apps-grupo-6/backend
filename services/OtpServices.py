from flask import g

from repositories import OtpRepository, UsersRepository
from utils import OtpUtils, UsersUtils

def create_otp(model, user_id, request_id):
    type = model["type"]

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

    g.response_code = "0200"
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

    checked = OtpRepository.check_if_user_has_active_otp(user_id=user_id,
                                                         type=type,
                                                         request_id=request_id,
                                                         errors_code_map={
                                                             "database_error_code": "0500",
                                                             "invalid_data_error_code": "0410"
                                                         })


    if checked["error"]: # if user already has an active otp_token with this type, it throws an error
        if checked["ok"]: # it's just to check if it wasn't a database error
            # so, if user has an active otp_token we just resend it
            OtpUtils.generate_otp_mail(otp_token=checked["data"]["otp_token"],
                                       user_contact=user_contact,
                                       type=type)

            g.response_code = "0200"

        return {}

    # if user does not have any active otp_token, we create, save and send a new one
    OtpUtils.create_save_and_send_token(user_id=user_id,
                                        type=type,
                                        user_contact=user_contact,
                                        request_id=request_id,
                                        errors_code_map={"database_error_code": "0501"})

    g.response_code = "0201"
    return {}