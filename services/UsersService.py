from flask import g
from configs.ServerConfig import logger
import datetime, jwt
from random import shuffle

from repositories import UsersRepository, OtpRepository
from utils import UsersUtils
from templates import UserTemplate, OtpTemplate
from configs import AuthConfig

def register_account(model, request_id):
    username = model["username"]
    password = model["password"].strip()
    first_name = model["first_name"]
    last_name = model["last_name"]
    telephone = model["telephone"]
    contact_email = model["contact_email"]
    hashed_password = UsersUtils.hash_password(password)

    exists_user = UsersRepository.check_if_username_doesnt_exist(username=username,
                                                                 request_id=request_id,
                                                                 errors_code_map={
                                                                     "database_error_code": "0500",
                                                                     "invalid_data_error_code": "0410"
                                                                 })
    if exists_user["error"]:
        return {}

    temp = list(request_id[14:20])
    shuffle(temp)
    verification_token = "".join(temp)
    expires_at = datetime.datetime.now() + datetime.timedelta(minutes=15)
    
    logger.info(f"{request_id} - generated verification OTP: '{verification_token}'")

    registered = UsersRepository.register_user(
        username=username,
        hashed_password=hashed_password,
        first_name=first_name,
        last_name=last_name,
        telephone=telephone,
        contact_email=contact_email,
        verification_token=verification_token,
        verification_expires_at=expires_at,
        request_id=request_id,
        errors_code_map={"database_error_code": "0501"}
    )

    if registered["error"]:
        return {}


    otp_saved = OtpRepository.save_otp(
        user_id=registered["data"]["user_id"],
        otp_token=verification_token,
        type="REGISTRATION",
        request_id=request_id,
        errors_code_map={"database_error_code": "0502"}
    )

    if otp_saved["error"]:
        return {}

    g.send_email_data = {
        "subject": "Verifica tu cuenta - Código de activación",
        "user_email": contact_email,
        "user_firstname": first_name,
        "user_lastname": last_name,
        "html_content": OtpTemplate.render_registration_verification_email(
            first_name=first_name,
            last_name=last_name,
            username=username,
            otp_code=verification_token
        )
    }

    logger.info(f"{request_id} - user registered, verification email sent")
    g.response_code = "0200"
    return {
        "data": {
            "username": username,
            "email": contact_email
        }
    }

def verify_otp_code(username, verification_code, request_id):
    logger.info(f"{request_id} - verifying OTP code for username: {username}")
    
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
        return _handle_registration_verification_new(username, verification_code, registration_data, request_id)
    
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
        return _handle_registration_verification(username, verification_code, initial_registration_data, request_id)
    
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
        return _handle_recovery_verification(username, verification_code, recovery_data, request_id)
    
    # No se encontró en ninguna tabla
    logger.error(f"{request_id} - invalid verification code for username: {username}")
    g.response_code = "0404"
    return {}

def _handle_registration_verification_new(username, verification_code, otp_data, request_id):
    """Maneja verificación de códigos de REGISTRATION desde otp_tokens - Login automático"""
    logger.info(f"{request_id} - handling REGISTRATION verification for username: {username}")
    
    otp_info = otp_data["data"]
    user_id = otp_info["user_id"]
    
    if otp_info["expires_at"] < datetime.datetime.now():
        logger.error(f"{request_id} - verification code expired for user: {username}")
        g.response_code = "0410"
        return {
            "error": "El código de verificación ha expirado. Solicita un nuevo código."
        }

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
        errors_code_map={"database_error_code": "0502"}
    )

    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=AuthConfig.jwt_exp_delta_seconds),
        "user_id": user_id
    }

    logger.info(f"{request_id} - generating JWT token for verified user...")
    token = jwt.encode(payload, AuthConfig.jwt_secret, algorithm=AuthConfig.jwt_algorithm)

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

    logger.info(f"{request_id} - user verified and logged in successfully")
    g.response_code = "0200"
    return {
        "data": {
            "type": "REGISTRATION",
            "message": "¡Cuenta verificada exitosamente! Ya estás logueado.",
            "token": token,
            "user": {
                "username": username,
                "first_name": user_contact["data"]["first_name"],
                "last_name": user_contact["data"]["last_name"],
                "email": user_contact["data"]["contact_email"]
            }
        }
    }

def _handle_registration_verification(username, verification_code, user_data, request_id):
    """Maneja verificación de códigos de REGISTRATION - Login automático"""
    logger.info(f"{request_id} - handling REGISTRATION verification for username: {username}")
    
    user_info = user_data["data"]
    user_id = user_info["id"]
    
    if user_info["verification_expires_at"] < datetime.datetime.now():
        logger.error(f"{request_id} - verification code expired for user: {username}")
        g.response_code = "0410"
        return {
            "error": "El código de verificación ha expirado. Solicita un nuevo código."
        }

    verified = UsersRepository.mark_user_as_verified(
        user_id=user_id,
        request_id=request_id,
        errors_code_map={"database_error_code": "0501"}
    )

    if verified["error"]:
        return {}

    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=AuthConfig.jwt_exp_delta_seconds),
        "user_id": user_id
    }

    logger.info(f"{request_id} - generating JWT token for verified user...")
    token = jwt.encode(payload, AuthConfig.jwt_secret, algorithm=AuthConfig.jwt_algorithm)

    g.send_email_data = {
        "subject": "¡Bienvenido/a! Tu cuenta ha sido activada",
        "user_email": user_info["contact_email"],
        "user_firstname": user_info["first_name"],
        "user_lastname": user_info["last_name"],
        "html_content": UserTemplate.render_register_email(
            first_name=user_info["first_name"],
            last_name=user_info["last_name"],
            username=username
        )
    }

    logger.info(f"{request_id} - user verified and logged in successfully")
    g.response_code = "0200"
    return {
        "data": {
            "type": "REGISTRATION",
            "message": "¡Cuenta verificada exitosamente! Ya estás logueado.",
            "token": token,
            "user": {
                "username": username,
                "first_name": user_info["first_name"],
                "last_name": user_info["last_name"],
                "email": user_info["contact_email"]
            }
        }
    }

def _handle_recovery_verification(username, verification_code, otp_data, request_id):
    logger.info(f"{request_id} - handling RECOVERY verification for username: {username}")
    
    otp_info = otp_data["data"]
    
    if otp_info["expires_at"] < datetime.datetime.now():
        logger.error(f"{request_id} - recovery code expired for user: {username}")
        g.response_code = "0410"
        return {
            "error": "El código de recuperación ha expirado. Solicita un nuevo código."
        }
    
    OtpRepository.delete_otp(
        user_id=otp_info["user_id"],
        otp_token=verification_code,
        type="RECOVERY",
        request_id=request_id,
        errors_code_map={"database_error_code": "0502"}
    )
    
    # Generar token temporal para cambio de contraseña (válido por 10 minutos)
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

def update_user_information(model, user_id, request_id):
    logger.info(f"{request_id} - formatting fields...")
    formatted_update = UsersUtils.update_class_fields_formatter(model=model, request_id=request_id)

    error = formatted_update["error"]
    columns = formatted_update["columns"]
    values = formatted_update["values"]

    if error:
        return {}

    if not columns:
        logger.error(f"{request_id} - all updatable fields are empty")
        g.response_code = "0410"
        return {}

    update_columns = ", ".join(columns)
    values.append(user_id)
    logger.debug(f"{request_id} - columns to update: {update_columns}")
    updated = UsersRepository.update_user(update_columns=update_columns,
                                          update_values=values,
                                          request_id=request_id,
                                          errors_code_map={"database_error_code": "0500"})

    if updated["error"]:
        return {}

    g.response_code = "0200"
    return {}

def get_user_information(user_id, request_id):
    user_information = UsersRepository.get_user_contact_information(user_id=user_id,
                                                                    request_id=request_id,
                                                                    errors_code_map={"database_error_code": "0500"})

    if user_information["error"]:
        return {}

    g.response_code = "0200"
    return {
        "data": user_information['data']
    }

def resend_otp(model, request_id):
    username = model["username"]
    otp_type = model["type"]
    
    logger.info(f"{request_id} - resending OTP for username '{username}' with type '{otp_type}'")
    
    user_data = UsersRepository.get_user_id_by_username(
        username=username,
        request_id=request_id,
        errors_code_map={
            "database_error_code": "0500",
            "invalid_data_error_code": "0404"
        }
    )
    
    if user_data["error"]:
        return {}
    
    user_id = user_data["data"]["id"]
    
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
    
    temp = list(request_id[14:20])
    shuffle(temp)
    otp_token = "".join(temp)
    logger.info(f"{request_id} - generated new OTP: '{otp_token}'")
    
    if otp_type == "REGISTRATION":
        user_verification_status = UsersRepository.check_user_verification_status(
            username=username,
            request_id=request_id,
            errors_code_map={
                "database_error_code": "0500",
                "invalid_data_error_code": "0411"
            }
        )
        
        if user_verification_status["error"]:
            logger.error(f"{request_id} - user '{username}' is already verified or doesn't exist, cannot request REGISTRATION OTP")
            g.response_code = "0411"
            return {
                "error": "La cuenta ya está verificada o no existe. No es posible reenviar el código de verificación."
            }
        
        
        otp_token_save = OtpRepository.save_otp(
            user_id=user_id,
            otp_token=otp_token,
            type=otp_type,
            request_id=request_id,
            errors_code_map={"database_error_code": "0502"}
        )
        
        if otp_token_save["error"]:
            return {}
        
        g.send_email_data = {
            "subject": "Código de verificación de cuenta - Reenvío",
            "user_email": user_contact["data"]["contact_email"],
            "user_firstname": user_contact["data"]["first_name"],
            "user_lastname": user_contact["data"]["last_name"],
            "html_content": OtpTemplate.render_registration_verification_email(
                first_name=user_contact["data"]["first_name"],
                last_name=user_contact["data"]["last_name"],
                username=username,
                otp_code=otp_token
            )
        }
        
    elif otp_type == "RECOVERY":
        user_verification_status = UsersRepository.check_user_verification_status(
            username=username,
            request_id=request_id,
            errors_code_map={
                "database_error_code": "0500",
                "invalid_data_error_code": "0412"
            }
        )
        
        if user_verification_status["error"]:
            logger.error(f"{request_id} - user '{username}' is not verified, cannot request RECOVERY OTP")
            g.response_code = "0412"
            return {
                "error": "La cuenta debe estar verificada para poder solicitar recuperación. Usa el tipo REGISTRATION para verificar tu cuenta primero."
            }
        otp_token_save = OtpRepository.save_otp(
            user_id=user_id,
            otp_token=otp_token,
            type=otp_type,
            request_id=request_id,
            errors_code_map={"database_error_code": "0502"}
        )
        
        if otp_token_save["error"]:
            return {}
            
        g.send_email_data = {
            "subject": "Código de recuperación de cuenta - Reenvío",
            "user_email": user_contact["data"]["contact_email"],
            "user_firstname": user_contact["data"]["first_name"],
            "user_lastname": user_contact["data"]["last_name"],
            "html_content": OtpTemplate.render_recover_otp_email(
                first_name=user_contact["data"]["first_name"],
                last_name=user_contact["data"]["last_name"],
                otp_code=otp_token
            )
        }
    
    logger.info(f"{request_id} - OTP resent successfully")
    g.response_code = "0200"
    return {
        "data": {
            "message": f"Código OTP de {otp_type.lower()} reenviado exitosamente",
            "email": user_contact["data"]["contact_email"]
        }
    }

def reset_password_with_token(model, request_id):
    reset_token = model["reset_token"]
    new_password = model["new_password"]
    
    logger.info(f"{request_id} - resetting password with token")
    
    try:
        # Decodificar y validar el token temporal
        decoded = jwt.decode(reset_token, AuthConfig.jwt_secret, algorithms=[AuthConfig.jwt_algorithm])
        
        # Verificar que sea un token de reset de contraseña
        if decoded.get("purpose") != "password_reset":
            logger.error(f"{request_id} - invalid token purpose: {decoded.get('purpose')}")
            g.response_code = "0413"
            return {
                "error": "Token inválido para cambio de contraseña."
            }
        
        username = decoded.get("username")
        user_id = decoded.get("user_id")
        
        if not username or not user_id:
            logger.error(f"{request_id} - missing username or user_id in token")
            g.response_code = "0413"
            return {
                "error": "Token inválido o corrupto."
            }
            
    except jwt.ExpiredSignatureError:
        logger.error(f"{request_id} - reset token has expired")
        g.response_code = "0414"
        return {
            "error": "El token de recuperación ha expirado. Solicita un nuevo código de recuperación."
        }
    except jwt.InvalidTokenError:
        logger.error(f"{request_id} - invalid reset token")
        g.response_code = "0413"
        return {
            "error": "Token de recuperación inválido."
        }
    
    hashed_password = UsersUtils.hash_password(new_password)
    
    password_updated = UsersRepository.update_user_password(
        user_id=user_id,
        new_password=hashed_password,
        request_id=request_id,
        errors_code_map={"database_error_code": "0500"}
    )
    
    if password_updated["error"]:
        return {}
    
    user_contact = UsersRepository.get_user_contact_information(
        user_id=user_id,
        request_id=request_id,
        errors_code_map={
            "database_error_code": "0501",
            "invalid_data_error_code": "0204"
        }
    )
    
    if not user_contact["error"]:
        g.send_email_data = {
            "subject": "Contraseña actualizada exitosamente",
            "user_email": user_contact["data"]["contact_email"],
            "user_firstname": user_contact["data"]["first_name"],
            "user_lastname": user_contact["data"]["last_name"],
            "html_content": UserTemplate.render_password_changed_email(
                first_name=user_contact["data"]["first_name"],
                last_name=user_contact["data"]["last_name"],
                username=username
            )
        }
    
    logger.info(f"{request_id} - password reset successfully for user: {username}")
    g.response_code = "0200"
    return {
        "data": {
            "message": "Contraseña actualizada exitosamente. Ya puedes iniciar sesión con tu nueva contraseña.",
            "username": username
        }
    }
