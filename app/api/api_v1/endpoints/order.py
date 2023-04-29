from typing import Any
import logging

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.order import (
    Order,
    OrderCreate,
    OrderUpdate,
    OrderSearchResults

)

from app.models.user import User
from app.schemas.product import ProductUpdate

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/all-orders", status_code=200, response_model=OrderSearchResults)
def get_all_orders(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    """
    Get all orders, used by admin and vendedor
    """

    if current_user.privilege != 1 and current_user.privilege != 2:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to perform this action",
        )


    results = crud.order.get_multi(db=db)
    if not results:
        return {"results": list()}
    logger.debug(results[0].owner_id)
    return {"results": list(results)}


@router.get("/{order_id}", status_code=200, response_model=Order)
def get_order_by_id(
    *,
    order_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get a single order by ID, used by admin and vendedor
    """
    order = crud.order.get(db=db, id=order_id)

    if current_user.privilege != 1 and current_user.privilege != 2:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to perform this action",
        )


    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order no encontrado",
        )
    logger.info(f"Order {order_id} encontrado")
    logger.debug(order)
    return order


@router.get("/", status_code=200, response_model=OrderSearchResults)
def get_own_orders(
    *,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Fetch all orders for the current user
    """
    orders = current_user.orders
    print(orders)
    if not orders:
        return {"results": list()}

    return {"results": list(orders)}


@router.post("/", status_code=201, response_model=Order)
def create_order(
    *,
    order_in: OrderCreate = Body(
        ...,
        example={
            "status": "pending",
            "owner_id": 2,
            "order_items": [
                {
                    "quantity": 1,
                    "product_id": 1000
                },
                {
                    "quantity": 2,
                    "product_id": 1001
                }
            ]
        }
    ),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Order:
    """
    Create a new order in the database.
    """
    
    if order_in.owner_id != current_user.id:
        raise HTTPException(
            status_code=401,
            detail="You can only create orders for yourself",
        )
    
    # Check that there is enough stock for each item in the order
    for item in order_in.order_items:
        product = crud.product.get(db=db, id=item.product_id)
        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product {item.product_id} not found",
            )
        if product.quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Product {item.product_id} has insufficient stock",
            )
    
    order = crud.order.create(db=db, order_in=order_in)
    
    # Update the stock for each item in the order
    for item in order_in.order_items:
        product = crud.product.get(db=db, id=item.product_id)
        product.quantity -= item.quantity
        product_in = ProductUpdate(quantity=product.quantity)
        crud.product.update(db=db, db_obj=product, obj_in=product_in)

    return order


@router.put("/", status_code=201, response_model=Order)
def update_order(
    *,
    order_in: OrderUpdate = Body(
        ...,
        example={
            "id": 1,
            "status": "completed",
        }
    ),

    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    """
    Update a order in the database. Only used by admin and vendedor
    """
    
    if current_user.privilege != 2 and current_user.privilege != 1:
        raise HTTPException(
            status_code=401,
            detail="Not authorized to update order",
        )
    
    order = crud.order.get(db=db, id=order_in.id)

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    order = crud.order.update(db=db, db_obj=order, obj_in=order_in)
    return order


@router.delete("/{order_id}", status_code=200, response_model=Order)
def delete_order(
    *,
    order_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    """
    Delete a order in the database. Only admins and vendedores can delete orders.
    """

    if current_user.privilege != 2 and current_user.privilege != 1:
        raise HTTPException(
            status_code=401,
            detail="Not authorized to delete order",
        )

    order = crud.order.get(db=db, id=order_id)
    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )
    order = crud.order.remove(db=db, id=order_id)
    return order
