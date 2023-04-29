from typing import Any, List, Optional
import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.pedido import (
    Pedido,
    PedidoCreate,
    PedidoUpdate,
    PedidoSearchResults

)
from app.schemas.item_pedido import (
    ItemPedidoCreate,
)
from app.models.user import User

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/all-pedidos", status_code=200, response_model=PedidoSearchResults)
def fetch_pedido(
    *,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Fetch a single pedido by ID
    """
    results = crud.pedido.get_multi(db=db)
    if not results:
        return {"results": list()}
    logger.debug(results[0].owner_id)
    return {"results": list(results)}


@router.get("/{pedido_id}", status_code=200, response_model=Pedido)
def fetch_pedido(
    *,
    pedido_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Fetch a single pedido by ID
    """
    pedido = crud.pedido.get(db=db, id=pedido_id)
    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado",
        )
    logger.info(f"Pedido {pedido_id} fetched")
    logger.debug(pedido)
    return pedido


@router.get("/{status}", status_code=200, response_model=PedidoSearchResults)
def fetch_pedido_by_status(
    *,
    status: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Fetch a single pedido by ID
    """
    pedidos = crud.pedido.get_multi(db=db)

    if not pedidos:
        return {"results": list()}
    
    results = filter(lambda pedido: status.lower() in pedido.status.lower(), pedidos)

    if not results:
        return {"results": list()}
    
    return results


@router.get("/", status_code=200, response_model=PedidoSearchResults)
def fetch_user_pedidos(
    *,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Fetch all pedidos for the current user
    """
    pedidos = current_user.pedidos
    print(pedidos)
    if not pedidos:
        return {"results": list()}

    return {"results": list(pedidos)}




@router.post("/", status_code=201, response_model=Pedido)
def create_pedido(
    *,
    item_pedido_in: List[ItemPedidoCreate],
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    """
    Create a new pedido in the database.
    """
    
    pedido_in = PedidoCreate(
        owner_id=current_user.id)
    pedido = crud.pedido.create(db=db, obj_in=pedido_in)
    
    for item in item_pedido_in:
        item_pedido = ItemPedidoCreate(
            quantity=item.quantity,
            product_id=item.product_id,
            pedido_id=pedido.id
        )
        crud.item_pedido.create(db=db, obj_in=item_pedido)
    
    return pedido


@router.put("/", status_code=201, response_model=Pedido)
def update_pedido_status(
    *,
    pedido_in: PedidoUpdate,
    db: Session = Depends(deps.get_db),
    user_is_admin_or_vendedor: User = Depends(deps.current_user_is_admin_or_vendedor),
) -> dict:
    """
    Update a pedido in the database.
    """
    pedido = crud.pedido.get(db=db, id=pedido_in.id)
    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido not found",
        )

    pedido = crud.pedido.update(db=db, db_obj=pedido, obj_in=pedido_in)
    return pedido


@router.delete("/{id}", status_code=200, response_model=Pedido)
def delete_pedido(
    *,
    id: int,
    db: Session = Depends(deps.get_db),
    user_is_admin_or_vendedor: User = Depends(deps.current_user_is_admin_or_vendedor),
) -> dict:
    """
    Delete a pedido in the database.
    """
    pedido = crud.pedido.get(db=db, id=id)
    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido not found",
        )
    pedido = crud.pedido.remove(db=db, id=id)
    return pedido
