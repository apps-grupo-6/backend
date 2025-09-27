import datetime
import jwt
from random import shuffle

from flask import g
from configs.ServerConfig import logger

from repositories import OtpRepository, UsersRepository
from templates import UserTemplate, OtpTemplate
from configs import AuthConfig


def check_token_expired(checked):
    if not checked["data"]:
        return False
    return _check_otp_expiration(checked["data"]["expires_at"], "legacy_check")

def delete_otp_token(user_id, otp_token, type, request_id, errors_code_map):
    deleted = OtpRepository.delete_otp(user_id=user_id,
                                       otp_token=otp_token,
                                       type=type,
                                       request_id=request_id,
                                       errors_code_map=errors_code_map)

    if deleted["error"]:
        return False

    return True

def handle_otp_verification(username, verification_code, request_id):
    logger.info(f"{request_id} - handling OTP verification for username: {username}")
    
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
    
    if not registration_data["error"]:
        return _handle_registration_verification_unified(username, verification_code, registration_data, request_id, "otp_tokens")
    
    initial_registration_data = UsersRepository.get_user_by_verification_code(
        username=username,
        verification_code=verification_code,
        request_id=request_id,
        errors_code_map={
            "database_error_code": "0500",
            "invalid_data_error_code": "0404"
        }
    )
    
    if not initial_registration_data["error"]:
        return _handle_registration_verification_unified(username, verification_code, initial_registration_data, request_id, "users")
    
    recovery_data = OtpRepository.check_otp_token_by_username(
        username=username,
        otp_token=verification_code,
        type="RECOVERY",
        request_id=request_id,
        errors_code_map={
            "database_error_code": "0500",
            "invalid_data_error_code": "0404"
        }
    )
    
    if not recovery_data["error"]:
        return _handle_recovery_otp_verification(username, verification_code, recovery_data, request_id)
    
    # No se encontró en ninguna tabla
    logger.error(f"{request_id} - invalid verification code for username: {username}")
    g.response_code = "0404"
    return {}


def save_otp_token(user_id, otp_token, otp_type, request_id):
    otp_token_save = OtpRepository.save_otp(
        user_id=user_id,
        otp_token=otp_token,
        type=otp_type,
        request_id=request_id,
        errors_code_map={"database_error_code": "0502"}
    )
    
    return not otp_token_save["error"]

def setup_email_unified(email_type, user_contact_data, username=None, otp_token=None):
    """Configura email para OTP"""
    
    email_configs = {
        "REGISTRATION_OTP": {
            "subject": "Código de verificación de cuenta - Reenvío",
            "template": lambda: OtpTemplate.render_registration_verification_email(
                first_name=user_contact_data["first_name"],
                last_name=user_contact_data["last_name"],
                username=username,
                otp_code=otp_token
            )
        },
        "RECOVERY_OTP": {
            "subject": "Código de recuperación de cuenta - Reenvío",
            "template": lambda: OtpTemplate.render_recover_otp_email(
                first_name=user_contact_data["first_name"],
                last_name=user_contact_data["last_name"],
                otp_code=otp_token
            )
        },
        "WELCOME": {
            "subject": "¡Bienvenido/a! Tu cuenta ha sido activada",
            "template": lambda: UserTemplate.render_register_email(
                first_name=user_contact_data["first_name"],
                last_name=user_contact_data["last_name"],
                username=username
            )
        }
    }
    
    config = email_configs[email_type]
    g.send_email_data = {
        "subject": config["subject"],
        "user_email": user_contact_data["contact_email"],
        "user_firstname": user_contact_data["first_name"],
        "user_lastname": user_contact_data["last_name"],
        "html_content": config["template"]()
    }

def setup_otp_email(otp_type, user_contact_data, username, otp_token):
    email_type = f"{otp_type}_OTP"
    setup_email_unified(email_type, user_contact_data, username, otp_token)

def _setup_welcome_email(user_contact_data, username):
    setup_email_unified("WELCOME", user_contact_data, username)

def delete_otp_helper(user_id, otp_token, otp_type, request_id):
    """Eliminar OTP"""
    return OtpRepository.delete_otp(
        user_id=user_id,
        otp_token=otp_token,
        type=otp_type,
        request_id=request_id,
        errors_code_map={"database_error_code": "0502"}
    )

def _check_otp_expiration(expires_at, request_id):
    """Verifica si un OTP ha expirado"""
    if expires_at < datetime.datetime.now():
        logger.error(f"{request_id} - verification code expired")
        g.response_code = "0410"
        return True
    return False

def _generate_jwt_token(username, user_id):
    """Genera un JWT token para login automático"""
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=AuthConfig.jwt_exp_delta_seconds),
        "user_id": user_id
    }
    return jwt.encode(payload, AuthConfig.jwt_secret, algorithm=AuthConfig.jwt_algorithm)


def _create_registration_success_response(username, token, user_contact_data):
    return {
        "type": "REGISTRATION",
        "message": "¡Cuenta verificada exitosamente! Ya estás logueado.",
        "token": token,
        "user": {
            "username": username,
            "first_name": user_contact_data["first_name"],
            "last_name": user_contact_data["last_name"],
            "email": user_contact_data["contact_email"]
        }
    }

def _handle_registration_verification_unified(username, verification_code, data, request_id, source="otp_tokens"):
    logger.info(f"{request_id} - handling REGISTRATION verification from {source}")
    
    info = data["data"]
    user_id = info.get("user_id") or info.get("id")
    expires_at = info.get("expires_at") or info.get("verification_expires_at")
    
    if _check_otp_expiration(expires_at, request_id):
        return {}

    if source == "otp_tokens":
        user_contact = UsersRepository.get_user_contact_information(
            user_id=user_id,
            request_id=request_id,
            errors_code_map={
                "database_error_code": "0501",
                "invalid_data_error_code": "0204"
            }
        )
        
        if user_contact["error"]:
            return {}
        
        user_data = user_contact["data"]
        
        delete_otp_helper(user_id, verification_code, "REGISTRATION", request_id)
    else:
        user_data = info

    verified = UsersRepository.mark_user_as_verified(
        user_id=user_id,
        request_id=request_id,
        errors_code_map={"database_error_code": "0501"}
    )

    if verified["error"]:
        return {}

    token = _generate_jwt_token(username, user_id)

    _setup_welcome_email(user_data, username)

    logger.info(f"{request_id} - user verified and logged in successfully")
    g.response_code = "0200"
    return {
        "data": _create_registration_success_response(username, token, user_data)
    }


def _handle_recovery_otp_verification(username, verification_code, otp_data, request_id):
    """Maneja verificación de RECOVERY desde otp_tokens - Token temporal"""
    logger.info(f"{request_id} - handling RECOVERY OTP verification")
    
    otp_info = otp_data["data"]
    
    if _check_otp_expiration(otp_info["expires_at"], request_id):
        return {}
    
    delete_otp_helper(otp_info["user_id"], verification_code, "RECOVERY", request_id)
    
    payload = {
        "username": username,
        "user_id": otp_info["user_id"],
        "purpose": "password_reset",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }
    
    temp_token = jwt.encode(payload, AuthConfig.jwt_secret, algorithm=AuthConfig.jwt_algorithm)
    
    logger.info(f"{request_id} - recovery code verified, generated temporary token")
    g.response_code = "0200"
    return {
        "data": {
            "type": "RECOVERY",
            "message": "Código verificado correctamente. Ahora puedes cambiar tu contraseña.",
            "reset_token": temp_token,
            "username": username
        }
    }

def generate_and_save_otp(user_id, otp_type, request_id):
    """Helper reutilizable para generar y guardar OTP"""
    
    temp = list(request_id[14:20])
    shuffle(temp)
    otp_token = "".join(temp)
    logger.info(f"{request_id} - generated new OTP: '{otp_token}'")
    
    otp_token_save = OtpRepository.save_otp(
        user_id=user_id,
        otp_token=otp_token,
        type=otp_type,
        request_id=request_id,
        errors_code_map={"database_error_code": "0502"}
    )
    
    if otp_token_save["error"]:
        return None
    
    return otp_token
