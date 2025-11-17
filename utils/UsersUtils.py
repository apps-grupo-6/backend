import bcrypt

from repositories import UsersRepository

def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def check_and_get_user_information(username, request_id, errors_code_map):
    exists_user = UsersRepository.get_user_id_by_username(username=username,
                                                          request_id=request_id,
                                                          errors_code_map=errors_code_map)

    if exists_user["error"]:
        return {"error": True}

    user_id = exists_user["data"]["id"]

    user_information = UsersRepository.get_user_contact_information(user_id=user_id,
                                                                    request_id=request_id,
                                                                    errors_code_map=errors_code_map)

    if user_information["error"]:
        return {"error": True}

    user_information["data"]["user_id"] = user_id
    return user_information

def update_class_fields_formatter(model):
    columns = []
    values = []
    error = False

    for key in model:
        if model[key]:
            columns.append(f"{key} = %s")
            values.append(model[key])

    return {
        "error": error,
        "columns": columns,
        "values": values
    }