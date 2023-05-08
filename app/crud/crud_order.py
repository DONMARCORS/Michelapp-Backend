import datetime

from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.order import Order
from app.models.order_item import OrderItem
from app.schemas.order import OrderCreate, OrderUpdate


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    def create(self, db: Session, *, order_in: OrderCreate) -> Order:
        # take datetime and add to created_at
        created_at = datetime.datetime.now()


        order = Order(
            status=order_in.status,
            owner_id=order_in.owner_id,
            created_at=created_at
        )
        db.add(order)
        db.commit()
        db.refresh(order)

        # create the order items in the database
        order_items = []
        for item in order_in.order_items:
            order_item = OrderItem(
                quantity=item.quantity,
                product_id=item.product_id,
                order_id=order.id
            )
            db.add(order_item)
            order_items.append(order_item)
        db.commit()
        db.refresh(order)
        return order


order = CRUDOrder(Order)