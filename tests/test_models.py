from __future__ import annotations

from decimal import Decimal

from modulo1.crud import add_order_item
from modulo1.crud import create_order
from modulo1.crud import create_user
from modulo1.crud import delete_order
from modulo1.crud import delete_user
from modulo1.crud import get_order
from modulo1.crud import get_user
from modulo1.crud import list_orders
from modulo1.crud import list_users
from modulo1.crud import update_order
from modulo1.crud import update_user


def test_user_crud(session):
    user = create_user(session, "Alice", "alice@example.com")

    assert user.id == 1
    assert get_user(session, user.id).name == "Alice"
    assert [u.email for u in list_users(session)] == ["alice@example.com"]

    updated = update_user(session, user.id, name="Alicia")
    assert updated.name == "Alicia"

    assert delete_user(session, user.id) is True
    assert get_user(session, user.id) is None


def test_order_and_item_crud(session):
    user = create_user(session, "Bob", "bob@example.com")
    order = create_order(session, user.id, status="pending")

    item = add_order_item(session, order.id, "Keyboard", 2, Decimal("49.99"))
    assert item.product_name == "Keyboard"
    assert item.quantity == 2

    stored_order = get_order(session, order.id)
    assert stored_order.total_amount == Decimal("99.98")
    assert len(stored_order.items) == 1

    updated_order = update_order(session, order.id, status="paid")
    assert updated_order.status == "paid"
    assert list_orders(session, user_id=user.id)[0].status == "paid"

    assert delete_order(session, order.id) is True
    assert get_order(session, order.id) is None
