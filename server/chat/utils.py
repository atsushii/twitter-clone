from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler

from django.db import IntegrityError

import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, IntegrityError):
        response.data['status_code'] = response.status_code
        logger.info("CONFLICT DATA IN DB: $s" % exc)

    elif isinstance(exc, ValidationError):
        response.data['status_code'] = response.status_code
        logger.info("BAD VALIDATION MESSAGE: %d" % exc)

    elif isinstance(exc, ObjectDoesNotExist):
        response.data['status_code'] = response.status_code
        logger.info("OBJECT DOESN'T EXIST: %s" % exc)

    elif response is not None:
        response.data['status_code'] = response.status_code
        logger.info("UNEXPECTED ERROR: %s" % exc)

    return response
