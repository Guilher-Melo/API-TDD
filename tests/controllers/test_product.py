from typing import List

import pytest
from fastapi import status

from tests.factories import product_data


async def test_controller_create_should_return_success(client, products_url):
    response = await client.post(products_url, json=product_data())

    content = response.json()
    del content['created_at']
    del content['updated_at']
    del content['id']

    assert response.status_code == status.HTTP_201_CREATED
    assert content == {
        "name": "Iphone 14 pro max",
        "quantity": 10,
        "price": "8.500",
        "status": True
    }


async def test_controller_get_should_return_success(client,
                                                    products_url,
                                                    product_inserted):
    response = await client.get(f'{products_url}{product_inserted.id}')

    content = response.json()
    del content['created_at']
    del content['updated_at']
    del content['id']

    assert content == {
        "name": "Iphone 14 pro max",
        "quantity": 10,
        "price": "8.500",
        "status": True
    }

    assert response.status_code == status.HTTP_200_OK


async def test_controller_get_should_return_not_found(client, products_url):
    id = '2549f3cf-0b76-40c0-be32-59618b3dd5bd'
    response = await client.get(f'{products_url}{id}')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        'detail': f'Product not found with filter: {id}'}


@pytest.mark.usefixtures("products_inserted")
async def test_controller_query_should_return_success(client,
                                                      products_url):
    response = await client.get(products_url)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), List)
    assert len(response.json()) > 1


async def test_controller_patch_should_return_success(client,
                                                      products_url,
                                                      product_inserted):

    response = await client.patch(f'{products_url}{product_inserted.id}',
                                  json={"price": "7.500"})

    content = response.json()

    del content['created_at']
    del content['updated_at']

    assert response.status_code == status.HTTP_200_OK

    assert content == {
        "id": str(product_inserted.id),
        "name": "Iphone 14 pro max",
        "quantity": 10,
        "price": "7.500",
        "status": True
    }


async def test_controller_delete_should_return_no_content(
        client, products_url, product_inserted
):
    response = await client.delete(f'{products_url}{product_inserted.id}')

    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_controller_delete_should_return_not_found(client, products_url):
    id = '2549f3cf-0b76-40c0-be32-59618b3dd5bd'
    response = await client.delete(f'{products_url}{id}')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        'detail': f'Product not found with filter: {id}'}
