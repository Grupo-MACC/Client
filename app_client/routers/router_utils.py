# router_utils.py
import logging
from fastapi import HTTPException

# URL del servicio con el que nos comunicaremos
ORDER_SERVICE_URL = "http://127.0.0.1:5000"  # Puerto del servicio de pedidos

logger = logging.getLogger(__name__)


def raise_and_log_error(my_logger, status_code: int, message: str):
    """Raises HTTPException and logs an error."""
    my_logger.error(message)
    raise HTTPException(status_code, message)