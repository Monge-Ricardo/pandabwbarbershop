import uuid
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from decimal import Decimal
from app.database import db
from app.models.schemas.product_schema import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(prefix="/products", tags=["Products CRUD"])

@router.get("", response_model=List[ProductResponse])
async def list_products(barbershop_id: Optional[str] = None):
    """
    Lista todos los productos, permitiendo filtrar por barbershop_id.
    """
    if barbershop_id:
        products = await db.products.find_many(where={"barbershop_id": barbershop_id})
    else:
        products = await db.products.find_many()
    return products

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    """
    Obtiene los detalles de un producto por su ID.
    """
    product = await db.products.find_unique(where={"id": product_id})
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado."
        )
    return product

@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(body: ProductCreate):
    """
    Crea un nuevo producto en la base de datos.
    """
    try:
        new_product = await db.products.create(
            data={
                "id": str(uuid.uuid4()),
                "barbershop_id": body.barbershop_id,
                "name": body.name,
                "description": body.description,
                "price": Decimal(str(body.price)) if body.price is not None else None,
                "stock": body.stock,
                "image_url": body.image_url,
                "is_active": True
            }
        )
        return new_product
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el producto en BD: {str(e)}"
        )

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: str, body: ProductUpdate):
    """
    Actualiza la información de un producto existente.
    """
    product = await db.products.find_unique(where={"id": product_id})
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado."
        )

    update_data = body.model_dump(exclude_unset=True)
    if "price" in update_data and update_data["price"] is not None:
        update_data["price"] = Decimal(str(update_data["price"]))

    if not update_data:
        return product

    try:
        updated = await db.products.update(
            where={"id": product_id},
            data=update_data
        )
        return updated
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el producto en BD: {str(e)}"
        )

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: str):
    """
    Elimina un producto de la base de datos.
    """
    product = await db.products.find_unique(where={"id": product_id})
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado."
        )

    try:
        await db.products.delete(where={"id": product_id})
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el producto de la BD: {str(e)}"
        )
