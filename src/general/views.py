from fastapi import APIRouter, status
from src.common.schemas.common import DetailsResponse

router = APIRouter()

@router.get(
    path="/health-check",
    tags=['Status'],
    response_model=DetailsResponse,
    status_code=status.HTTP_200_OK
)
def health_check() -> DetailsResponse:
    """
    Health check endpoint.

    :return: Response is our app alive
    """
    return DetailsResponse(details="OK")