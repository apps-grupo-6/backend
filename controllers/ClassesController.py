from flask import Blueprint, g, request
from marshmallow import ValidationError
from configs.ServerConfig import logger
from utils import AuthUtils, ServerUtils

bp = Blueprint('classes', __name__)

from configs import ClassesConfig
from models import ClassesModel
from services import ClassesService

@bp.get("/")
@ServerUtils.configure_request(description_code_map=ClassesConfig.get_all_classes_code_map, method="GET")
@AuthUtils.validate_session
def get_all_classes():
    # Created by Luciana
    logger.info(f"{g.request_id} - starting get_all_classes")
    return ClassesService.get_all_classes(request_id=g.request_id)

@bp.post("/")
@ServerUtils.configure_request(description_code_map=ClassesConfig.create_class_code_map, method="POST")
@AuthUtils.validate_session
def create_class():
    try:
        logger.info(f"{g.request_id} - starting create_class")
        logger.info(f"{g.request_id} - starting mandatory fields check")

        data = request.json
        model = ClassesModel.create_class().load(data)
    except ValidationError as e:
        logger.exception(f"{g.request_id} - there are absent mandatory fields")
        g.response_code = "0400"
        return {
            "detailed_description": e.messages
        }

    logger.info(f"{g.request_id} - finished mandatory fields check")
    return ClassesService.create_class(model=model, request_id=g.request_id)

@bp.get("/upcoming")
@ServerUtils.configure_request(description_code_map=ClassesConfig.upcoming_classes_code_map, method="GET", endpoint="upcoming")
@AuthUtils.validate_session
def get_user_upcoming_classes():
    logger.info(f"{g.request_id} - starting get_user_upcoming_classes")
    return ClassesService.get_user_upcoming_classes(user_id=g.user_id, request_id=g.request_id)

@bp.get("/<int:id>")
@ServerUtils.configure_request(description_code_map=ClassesConfig.get_class_code_map, method="GET", endpoint="<id>")
@AuthUtils.validate_session
def get_class(id):
    logger.info(f"{g.request_id} - starting get_class")
    return ClassesService.get_class(class_id=id, request_id=g.request_id)

@bp.put("/<int:id>")
@ServerUtils.configure_request(description_code_map=ClassesConfig.update_class_code_map, method="PUT", endpoint="<id>")
@AuthUtils.validate_session
def update_class(id):
    try:
        logger.info(f"{g.request_id} - starting update_class")
        logger.info(f"{g.request_id} - starting mandatory fields check")

        data = request.json
        model = ClassesModel.update_class().load(data)
    except ValidationError as e:
        logger.exception(f"{g.request_id} - there are absent mandatory fields")
        g.response_code = "0400"
        return {
            "detailed_description": e.messages
        }

    logger.info(f"{g.request_id} - finished mandatory fields check")
    return ClassesService.update_class(model=model, class_id=id, user_id=g.user_id, request_id=g.request_id)

@bp.put("/<int:id>/finish")
@ServerUtils.configure_request(description_code_map=ClassesConfig.finish_class_code_map, method="PUT", endpoint="<id>/finish")
@AuthUtils.validate_session
def finish_class(id):
    logger.info(f"{g.request_id} - starting finish_class")
    return ClassesService.finish_class(class_id=id, user_id=g.user_id, request_id=g.request_id)

@bp.post("/<int:id>/participant")
@ServerUtils.configure_request(description_code_map=ClassesConfig.add_class_participant_code_map, method="POST", endpoint="<id>/participant")
@AuthUtils.validate_session
def add_class_participant(id):
    logger.info(f"{g.request_id} - starting add_class_participant")
    return ClassesService.add_class_participant(class_id=id, user_id=g.user_id, request_id=g.request_id)

@bp.delete("/<int:id>/participant")
@ServerUtils.configure_request(description_code_map=ClassesConfig.cancel_participant_code_map, method="DELETE", endpoint="<id>/participant")
@AuthUtils.validate_session
def cancel_participant(id):
    logger.info(f"{g.request_id} - starting cancel_participant")
    return ClassesService.cancel_participant(class_id=id, user_id=g.user_id, request_id=g.request_id)

@bp.put("/<int:id>/participant/confirm")
@ServerUtils.configure_request(description_code_map=ClassesConfig.confirm_participant_code_map, method="PUT", endpoint="<id>/participant/confirm")
@AuthUtils.validate_session
def confirm_participant(id):
    logger.info(f"{g.request_id} - starting confirm_participant")
    return ClassesService.confirm_participant(class_id=id, user_id=g.user_id, request_id=g.request_id)
