# routers/client_router.py
import logging
import httpx
from fastapi import APIRouter, status

from sql import schemas 
from .router_utils import raise_and_log_error, ORDER_SERVICE_URL

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get(
    "/",
    summary="Health check endpoint",
    response_model=schemas.Message,
)
async def health_check():
    """Endpoint to check if the client service is running."""
    logger.debug("GET '/' endpoint called.")
    return {"detail": "Client service is OK"}

@router.post(
    "/order",
    response_model=schemas.Order,
    summary="Create a new manufacturing order",
    status_code=status.HTTP_201_CREATED,
    tags=["Client Actions"]
)
async def create_new_order(order_data: schemas.OrderPost):
    """
    Receives an order from the end-user and forwards it to the Order Service.
    """
    logger.info(
        "Forwarding request to create order with %d pieces.",
        order_data.number_of_pieces
    )
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{ORDER_SERVICE_URL}/order",
                json=order_data.model_dump()
            )
            response.raise_for_status()
            return response.json()

    except httpx.RequestError as exc:
        raise_and_log_error(
            logger,
            status.HTTP_503_SERVICE_UNAVAILABLE,
            f"Error calling Order Service: {exc}"
        )
    except httpx.HTTPStatusError as exc:
        raise_and_log_error(
            logger,
            exc.response.status_code,
            f"Order Service returned an error: {exc.response.text}"
        )