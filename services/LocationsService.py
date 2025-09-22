from configs.ServerConfig import logger
from flask import g

from managers import LocationsManager
from repositories import UsersRepository, LocationsRepository


def create_location(model, user_id, request_id):
    country_code = model['country_code']
    city = model['city']
    address = model['address']

    exists_user = UsersRepository.check_if_user_exists(user_id=user_id,
                                                       request_id=request_id,
                                                       errors_code_map={
                                                           "database_error_code": "0500",
                                                           "invalid_data_error_code": "0410"
                                                       })

    if exists_user["error"]:
        return {}

    created = LocationsRepository.create_location(owner_id=user_id,
                                                  country_code=country_code,
                                                  city=city,
                                                  address=address,
                                                  request_id=request_id,
                                                  errors_code_map={"database_error_code": "0501"})

    if created["error"]:
        return {}

    g.response_code = "0200"
    return {}
