"""
Run this once to populate the database from seed_data.json.

Usage:
    python seed_db.py
"""

import json

from app import app, db, User, TableModel, Category, MenuItem, Order, OrderDetail


with open("seed_data.json", "r", encoding="utf-8") as f:
    seed = json.load(f)


with app.app_context():

    # --------------------------------------------------
    # Insert users
    # --------------------------------------------------

    username_to_id = {}

    for user_data in seed.get("users", []):

        existing = User.query.filter_by(
            username=user_data["username"]
        ).first()

        if existing:
            username_to_id[user_data["username"]] = existing.id

            print(
                f"User already exists, skipping: "
                f"{user_data['username']}"
            )

            continue

        user = User(
            username=user_data["username"],
            email=user_data["email"],
            full_name=user_data["full_name"],
            role=user_data.get("role", "customer")
        )
        user.set_password(user_data["password"])

        db.session.add(user)
        db.session.flush()

        username_to_id[user_data["username"]] = user.id

        print(
            f"Created user: {user_data['username']} "
            f"(role={user_data.get('role', 'customer')})"
        )

    db.session.commit()

    # --------------------------------------------------
    # Insert tables
    # --------------------------------------------------

    table_number_to_id = {}

    for table_data in seed.get("tables", []):

        existing = TableModel.query.filter_by(
            table_number=table_data["table_number"]
        ).first()

        if existing:
            table_number_to_id[table_data["table_number"]] = existing.id

            print(
                f"Table already exists, skipping: "
                f"Table {table_data['table_number']}"
            )

            continue

        table = TableModel(
            table_number=table_data["table_number"],
            seating_capacity=table_data["seating_capacity"],
            status=table_data.get("status", "available")
        )

        db.session.add(table)
        db.session.flush()

        table_number_to_id[table_data["table_number"]] = table.id

        print(
            f"Created table: Table {table_data['table_number']} "
            f"(seats {table_data['seating_capacity']})"
        )

    db.session.commit()

    # --------------------------------------------------
    # Insert categories
    # --------------------------------------------------

    category_name_to_id = {}

    for cat_data in seed["categories"]:

        existing = Category.query.filter_by(
            name=cat_data["name"]
        ).first()

        if existing:
            category_name_to_id[cat_data["name"]] = existing.id

            print(
                f"Category already exists, skipping: "
                f"{cat_data['name']}"
            )

            continue

        category = Category(
            name=cat_data["name"],
            description=cat_data.get("description")
        )

        db.session.add(category)
        db.session.flush()

        category_name_to_id[cat_data["name"]] = category.id

        print(
            f"Created category: {cat_data['name']}"
        )

    db.session.commit()

    # --------------------------------------------------
    # Insert menu items
    # --------------------------------------------------

    menu_item_name_to_id = {}

    for item_data in seed["menu_items"]:

        existing = MenuItem.query.filter_by(
            name=item_data["name"]
        ).first()

        if existing:
            menu_item_name_to_id[item_data["name"]] = existing.id

            print(
                f"Menu item already exists, skipping: "
                f"{item_data['name']}"
            )

            continue

        category_id = category_name_to_id.get(
            item_data["category"]
        )

        if category_id is None:
            print(
                f"Skipping '{item_data['name']}' — "
                f"category '{item_data['category']}' not found"
            )

            continue

        item = MenuItem(
            category_id=category_id,
            name=item_data["name"],
            price=item_data["price"],
            is_available=item_data.get(
                "is_available",
                True
            )
        )

        db.session.add(item)
        db.session.flush()

        menu_item_name_to_id[item_data["name"]] = item.id

        print(
            f"Created menu item: "
            f"{item_data['name']} "
            f"(${item_data['price']})"
        )

    db.session.commit()

    # --------------------------------------------------
    # Insert orders + order details
    # --------------------------------------------------

    for order_data in seed.get("orders", []):

        table_id = table_number_to_id.get(
            order_data["table_number"]
        )

        if table_id is None:
            print(
                f"Skipping order — "
                f"table {order_data['table_number']} not found"
            )

            continue

        username = order_data.get("username")
        user_id = username_to_id.get(username) if username else None

        order = Order(
            user_id=user_id,
            table_id=table_id,
            status=order_data.get("status", "pending")
        )

        db.session.add(order)
        db.session.flush()

        total = 0.0

        for detail_data in order_data["order_details"]:

            menu_item_id = menu_item_name_to_id.get(
                detail_data["menu_item"]
            )

            if menu_item_id is None:
                print(
                    f"Skipping order detail — "
                    f"menu item '{detail_data['menu_item']}' not found"
                )

                continue

            menu_item = db.session.get(MenuItem, menu_item_id)
            subtotal = menu_item.price * detail_data["quantity"]
            total += subtotal

            order_detail = OrderDetail(
                order_id=order.id,
                menu_item_id=menu_item_id,
                quantity=detail_data["quantity"],
                subtotal=subtotal
            )

            db.session.add(order_detail)

        order.total_amount = total

        print(
            f"Created order: Table {order_data['table_number']} "
            f"(status={order_data.get('status', 'pending')}, total=${total:.2f})"
        )

    db.session.commit()


print("\nSeeding complete.")