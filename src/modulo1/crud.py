from __future__ import annotations

from decimal import Decimal

from models import Order
from models import OrderItem
from models import User
from sqlalchemy import select
from sqlalchemy.orm import Session


def _refresh_and_return(session: Session, model):
    session.commit()
    session.refresh(model)
    return model


def create_user(session: Session, name: str, email: str) -> User:
    user = User(name=name, email=email)
    session.add(user)
    return _refresh_and_return(session, user)


def get_user(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)


def list_users(session: Session) -> list[User]:
    return list(session.scalars(select(User).order_by(User.id)).all())


def update_user(session: Session, user_id: int, **kwargs) -> User | None:
    print(f"Updating user {user_id} with {kwargs}")
    user = session.get(User, user_id)
    if user is None:
        return None

    for field, value in kwargs.items():
        if hasattr(user, field):
            setattr(user, field, value)

    return _refresh_and_return(session, user)


def delete_user(session: Session, user_id: int) -> bool:
    user = session.get(User, user_id)
    if user is None:
        return False
    session.delete(user)
    session.commit()
    return True


def create_order(session: Session, user_id: int, status: str = "pending") -> Order:
    user = session.get(User, user_id)
    if user is None:
        raise ValueError(f"User {user_id} does not exist")

    order = Order(user_id=user_id, status=status)
    session.add(order)
    return _refresh_and_return(session, order)


def get_order(session: Session, order_id: int) -> Order | None:
    return session.get(Order, order_id)


def list_orders(session: Session, user_id: int | None = None) -> list[Order]:
    stmt = select(Order).order_by(Order.id)
    if user_id is not None:
        stmt = stmt.where(Order.user_id == user_id)
    return list(session.scalars(stmt).all())


def _recalculate_order_total(order: Order) -> None:
    total = sum(
        (item.quantity * item.unit_price for item in order.items),
        Decimal("0.00"),
    )
    order.total_amount = total


def add_order_item(
    session: Session,
    order_id: int,
    product_name: str,
    quantity: int,
    unit_price: Decimal | str | int | float,
) -> OrderItem:
    order = session.get(Order, order_id)
    if order is None:
        raise ValueError(f"Order {order_id} does not exist")

    if quantity <= 0:
        raise ValueError("quantity must be greater than zero")

    item = OrderItem(
        order_id=order_id,
        product_name=product_name,
        quantity=quantity,
        unit_price=Decimal(str(unit_price)),
    )
    session.add(item)
    session.flush()
    _recalculate_order_total(order)
    session.commit()
    session.refresh(item)
    session.refresh(order)
    return item


def update_order(session: Session, order_id: int, **kwargs) -> Order | None:
    order = session.get(Order, order_id)
    if order is None:
        return None

    for field, value in kwargs.items():
        if hasattr(order, field):
            setattr(order, field, value)

    if "total_amount" in kwargs:
        order.total_amount = Decimal(str(kwargs["total_amount"]))
    else:
        _recalculate_order_total(order)

    return _refresh_and_return(session, order)


def delete_order(session: Session, order_id: int) -> bool:
    order = session.get(Order, order_id)
    if order is None:
        return False
    session.delete(order)
    session.commit()
    return True
