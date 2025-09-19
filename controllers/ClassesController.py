from flask import Blueprint, g, request
from marshmallow import ValidationError
from configs.ServerConfig import logger
from utils import AuthUtils, ServerUtils

bp = Blueprint('classes', __name__)

from configs import ClassesConfig
from models import ClassesModel
from services import ClassesService

@bp.post("/")
@AuthUtils.jwt_token_required
@ServerUtils.configure_request(description_code_map=ClassesConfig.create_class_code_map, method="POST")
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

@bp.put("/<int:id>/finish")
@AuthUtils.jwt_token_required
@ServerUtils.configure_request(description_code_map=ClassesConfig.finish_class_code_map, method="PUT", endpoint="<id>/finish")
def finish_class(id):
    try:
        logger.info(f"{g.request_id} - starting finish_class")
        logger.info(f"{g.request_id} - starting mandatory fields check")

        data = {"class_id": id}
        model = ClassesModel.finish_class().load(data)
    except ValidationError as e:
        logger.exception(f"{g.request_id} - there are absent mandatory fields")
        g.response_code = "0400"
        return {
            "detailed_description": e.messages
        }

    logger.info(f"{g.request_id} - finished mandatory fields check")
    return ClassesService.finish_class(model=model, request_id=g.request_id)

@bp.put("/<int:id>")
@AuthUtils.jwt_token_required
@ServerUtils.configure_request(description_code_map=ClassesConfig.update_class_code_map, method="PUT", endpoint="<id>")
def update_class(id):
    try:
        logger.info(f"{g.request_id} - starting update_class")
        logger.info(f"{g.request_id} - starting mandatory fields check")

        data = request.json
        data["class_id"] = id
        model = ClassesModel.update_class().load(data)
    except ValidationError as e:
        logger.exception(f"{g.request_id} - there are absent mandatory fields")
        g.response_code = "0400"
        return {
            "detailed_description": e.messages
        }

    logger.info(f"{g.request_id} - finished mandatory fields check")
    return ClassesService.update_class(model=model, request_id=g.request_id)

@bp.get("/")
@AuthUtils.jwt_token_required
@ServerUtils.configure_request(description_code_map=ClassesConfig.get_all_classes_code_map, method="GET")
def get_all_classes():
    logger.info(f"{g.request_id} - starting get_all_classes")

    return ClassesService.get_all_classes(request_id=g.request_id)