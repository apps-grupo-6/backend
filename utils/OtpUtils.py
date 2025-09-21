import datetime

from repositories import OtpRepository


def check_token_expired(checked):
    return checked["data"] and checked["data"]["expires_at"] < datetime.datetime.now()

def delete_otp_token(user_id, otp_token, type, request_id, errors_code_map):
    deleted = OtpRepository.delete_otp(user_id=user_id,
                                       otp_token=otp_token,
                                       type=type,
                                       request_id=request_id,
                                       errors_code_map=errors_code_map)

    if deleted["error"]:
        return False

    return True