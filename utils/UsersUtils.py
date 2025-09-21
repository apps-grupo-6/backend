import bcrypt

from repositories import UsersRepository

def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def check_and_get_user_information(user_id, request_id, error_code_maps):
    exists_user = UsersRepository.check_if_user_exists(user_id=user_id,
                                                       request_id=request_id,
                                                       errors_code_map=error_code_maps)

    if exists_user["error"]:
        return {"error": True}

    user_information = UsersRepository.get_user_contact_information(user_id=user_id,
                                                                    request_id=request_id,
                                                                    errors_code_map=error_code_maps
                                                                    )

    if user_information["error"]:
        return {"error": True}

    return user_information