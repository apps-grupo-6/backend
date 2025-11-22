from flask import Blueprint, g, request
from marshmallow import ValidationError
from configs.ServerConfig import logger
from utils import AuthUtils

bp = Blueprint('classes', __name__)

from models import ClassesModel
from services import ClassesService

@bp.get("/")
@AuthUtils.validate_session
def get_all_classes():
    # Created by Luciana
    logger.info(f"{g.request_id} - starting get_all_classes")
    return ClassesService.get_all_classes(request_id=g.request_id)

@bp.post("/")
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
    return ClassesService.create_class(model=model, user_id=g.user_id, request_id=g.request_id)

@bp.get("/upcoming")
@AuthUtils.validate_session
def get_user_upcoming_classes():
    logger.info(f"{g.request_id} - starting get_user_upcoming_classes")
    return ClassesService.get_user_upcoming_classes(user_id=g.user_id, request_id=g.request_id)

@bp.get("/history")
@AuthUtils.validate_session
def get_user_classes_history():
    logger.info(f"{g.request_id} - starting get_user_classes_history")
    since = request.args.get("since", None)
    until = request.args.get("until", None)
    return ClassesService.get_user_classes_history(user_id=g.user_id, since=since, until=until, request_id=g.request_id)

@bp.get("/<int:id>")
@AuthUtils.validate_session
def get_class(id):
    logger.info(f"{g.request_id} - starting get_class")
    return ClassesService.get_class(class_id=id, request_id=g.request_id)

@bp.put("/<int:id>")
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

@bp.patch("/<int:id>/cancel")
@AuthUtils.validate_session
def cancel_class(id):
    logger.info(f"{g.request_id} - starting cancel_class")
    return ClassesService.cancel_class(class_id=id, user_id=g.user_id, request_id=g.request_id)

@bp.patch("/<int:id>/start")
@AuthUtils.validate_session
def start_class(id):
    logger.info(f"{g.request_id} - starting start_class")
    return ClassesService.start_class(class_id=id, user_id=g.user_id, request_id=g.request_id)

@bp.patch("/<int:id>/finish")
@AuthUtils.validate_session
def finish_class(id):
    logger.info(f"{g.request_id} - starting finish_class")
    return ClassesService.finish_class(class_id=id, user_id=g.user_id, request_id=g.request_id)

@bp.post("/<int:id>/participant")
@AuthUtils.validate_session
def add_participant(id):
    logger.info(f"{g.request_id} - starting add_participant")
    return ClassesService.add_participant(class_id=id, user_id=g.user_id, request_id=g.request_id)

@bp.patch("/<int:id>/participant/cancel")
@AuthUtils.validate_session
def cancel_participant(id):
    logger.info(f"{g.request_id} - starting cancel_participant")
    return ClassesService.cancel_participant(class_id=id, user_id=g.user_id, request_id=g.request_id)

@bp.patch("/<int:id>/participant/confirm")
@AuthUtils.validate_session
def confirm_participant(id):
    logger.info(f"{g.request_id} - starting confirm_participant")
    return ClassesService.confirm_participant(class_id=id, user_id=g.user_id, request_id=g.request_id)

@bp.patch("/<int:id>/participant/check-in")
@AuthUtils.validate_session
def check_in_participant(id):
    logger.info(f"{g.request_id} - starting check_in_participant")
    return ClassesService.check_in_participant(class_id=id, user_id=g.user_id, request_id=g.request_id)