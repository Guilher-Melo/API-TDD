from typing import List
from uuid import UUID

import pytest

from store.core.exceptions import NotFoundException
from store.schemas.product import ProductOut, ProductUpdateOut
from store.usecases.product import product_usecase


async def test_usecases_create_should_return_success(product_in):
    result = await product_usecase.create(body=product_in)

    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 pro max"


async def test_usecases_get_should_return_success(product_id):
    result = await product_usecase.get(id=product_id)

    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 pro max"


async def test_usecases_get_should_return_not_found():
    with pytest.raises(NotFoundException) as err:
        await product_usecase.get(id=UUID("dcadf1a3-c437-4980-bf25-ade7d1fa6ddc"))

    assert err.value.message == "Product not found with filter: dcadf1a3-c437-4980-bf25-ade7d1fa6ddc"


async def test_usecases_query_should_return_success():
    result = await product_usecase.query()

    assert isinstance(result, List)


async def test_usecases_update_should_return_success(product_id, product_up):
    product_up.price = 7500.70
    result = await product_usecase.update(id=product_id, body=product_up)

    assert isinstance(result, ProductUpdateOut)
