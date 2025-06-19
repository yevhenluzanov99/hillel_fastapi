from typing import Union, Annotated

from fastapi import APIRouter, status, Depends, Response

from src.catalogue.models.pydantic import ProductModel
from src.catalogue.services import get_product_service
from src.common.schemas.common import ErrorResponse

product_router = APIRouter(prefix="/products")


@product_router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=list[ProductModel]
)
async def get_products_list(product_service=Depends(get_product_service)) -> list[ProductModel]:
    """
    Get list of products

    :param product_service:
    :return: Response with list of ProductModels
    """
    return await product_service.list()


@product_router.get(
    path="/{pk}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": ProductModel},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}
    },
    response_model=Union[ProductModel, ErrorResponse]
)
async def get_product_details(
        response: Response,
        pk: int,
        service: Annotated[get_product_service, Depends()],
) -> Union[ProductModel, ErrorResponse]:
    """
    Get list of products

    :return: Response with list of ProductModels
    """
    try:
        response = await service.details(pk)
    except ValueError as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return response
