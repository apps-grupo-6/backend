from configs.ServerConfig import logger
from flask import g
from random import shuffle
import datetime

from managers import OtpManager
from configs import OtpConfig

def create_otp(model, request_id):
    user_id = model["user_id"]

    logger.info(f"{request_id} - checking if the user_id '{user_id}' already has an active otp token")
    checked = OtpManager.check_otp(user_id=user_id, request_id=request_id)

    if not checked["ok"]:
        logger.critical(f"{request_id} - database failed while checking")
        g.response_code = "0500"
        return {"code": "0500", "description": OtpConfig.create_otp_code_map["0500"]}, 500

    if checked["data"]:
        logger.info(f"{request_id} - the user already has an otp")

        if checked["data"]["expires_at"] >= datetime.datetime.utcnow():
            logger.info(f"{request_id} - user's otp_token is not expired, it's not required to proceed")
            g.response_code = "0410"
            return {"code": "0410", "description": OtpConfig.create_otp_code_map["0410"]}, 400
        else:
            logger.info(f"{request_id} - user's otp_token is expired, creating a new one...")

    temp = list(request_id[:6])
    shuffle(temp)
    otp_token = "".join(temp)
    logger.info(f"{request_id} - generated OTP '{otp_token}'")

    otp_token_saved = OtpManager.create_otp(otp_token=otp_token,
                                            user_id=user_id,
                                            request_id=request_id)

    if not otp_token_saved["ok"]:
        logger.critical(f"{g.request_id} - there was an error creating otp_token'")
        g.response_code = "0501"
        return {"code": "0501", "description": OtpConfig.create_otp_code_map["0501"]}, 500

    g.notification_data = {
        "subject": "Código de inicio de sesión para Excuses 404",
        "message": f"Se detectó un intento de inicio de sesión de tu cuenta. \nEn caso de haber sido vos, ingresa el siguiente código: {otp_token}\n\nEn caso de no haber sido vos, por favor cambia la contraseña inmediatamente.\n\nAtentamente, el equipo de Excuses 404"
    }

    g.response_code = "0200"
    return {
        "code": "0200",
        "data": {
            "otp_token": otp_token
        }
    }, 200