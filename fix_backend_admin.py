import os

# Find the project root
for entry in os.scandir('C:\\Users\\aDMIN'):
    if 'OneDrive' in entry.name:
        full = entry.path
        test_path = os.path.join(full, 'Desktop', 'restaurant', 'Project-scholarship', 'frontend', 'app', 'pages', 'orders.vue')
        if os.path.exists(test_path):
            project_root = os.path.join(full, 'Desktop', 'restaurant', 'Project-scholarship')
            print(f'Project root: {project_root}')

            # === FIX backend/orders.py ===
            orders_py = os.path.join(project_root, 'backend', 'app', 'routes', 'orders.py')
            with open(orders_py, 'r', encoding='utf-8') as f:
                content = f.read()

            # Modify create_order to handle items without product_id (admin manual tickets)
            old_item_loop = """    order_items = []
    total_price = 0.0
    for raw_item in raw_items:
        if not isinstance(raw_item, dict):
            return jsonify({"message": "Invalid order item"}), 400
        try:
            product_id = int(raw_item.get("product_id"))
            quantity = int(raw_item.get("quantity"))
        except (TypeError, ValueError):
            return jsonify({"message": "Invalid order item"}), 400
        if quantity < 1:
            return jsonify({"message": "Order item quantity must be at least 1"}), 400

        product = db.session.get(Product, product_id)
        if not product:
            return jsonify({"message": f"Product {product_id} not found"}), 404

        total_price += product.price * quantity
        order_items.append(
            OrderItem(
                product_id=product.id,
                quantity=quantity,
                price=product.price,
                product_name=product.name,
                product_image=product.image or "",
            )
        )"""

            new_item_loop = """    order_items = []
    total_price = 0.0
    for raw_item in raw_items:
        if not isinstance(raw_item, dict):
            return jsonify({"message": "Invalid order item"}), 400
        try:
            quantity = int(raw_item.get("quantity"))
        except (TypeError, ValueError):
            return jsonify({"message": "Invalid order item"}), 400
        if quantity < 1:
            return jsonify({"message": "Order item quantity must be at least 1"}), 400

        product_id = raw_item.get("product_id")
        if product_id is not None:
            try:
                product_id = int(product_id)
            except (TypeError, ValueError):
                return jsonify({"message": "Invalid order item"}), 400
            product = db.session.get(Product, product_id)
            if not product:
                return jsonify({"message": f"Product {product_id} not found"}), 404
            item_name = product.name
            item_image = product.image or ""
            item_price = product.price
        else:
            item_name = str(raw_item.get("name", ""))
            item_image = str(raw_item.get("image", "") or "")
            item_price = float(raw_item.get("price", 0))

        total_price += item_price * quantity
        order_items.append(
            OrderItem(
                product_id=product_id if product_id else 0,
                quantity=quantity,
                price=item_price,
                product_name=item_name,
                product_image=item_image,
            )
        )"""

            content = content.replace(old_item_loop, new_item_loop)

            with open(orders_py, 'w', encoding='utf-8') as f:
                f.write(content)
            print('  backend orders.py: updated')

            # === FIX admin/orders.vue saveOrder ===
            admin_orders = os.path.join(project_root, 'frontend', 'app', 'pages', 'admin', 'orders.vue')
            with open(admin_orders, 'r', encoding='utf-8') as f:
                content = f.read()

            # Fix saveOrder to send proper fields
            old_save = """    try {
      const items = editingOrder.value.items.map(item => ({
        name: item.name,
        quantity: item.quantity,
        price: item.price,
      }))
      const res = await $fetch('/orders', {
        baseURL: config.public.apiBase,
        method: 'POST',
        headers: { Authorization: `Bearer ${token.value}`, 'Content-Type': 'application/json' },
        body: { items },
      })"""

            new_save = """    try {
      const items = editingOrder.value.items.map(item => ({
        name: item.name,
        quantity: item.quantity,
        price: item.price,
      }))
      const res = await $fetch('/orders', {
        baseURL: config.public.apiBase,
        method: 'POST',
        headers: { Authorization: `Bearer ${token.value}`, 'Content-Type': 'application/json' },
        body: {
          items,
          order_type: 'dine-in',
          payment_method: 'cash',
          customer_name: editingOrder.value.customerName,
          notes: '',
        },
      })"""

            content = content.replace(old_save, new_save)

            with open(admin_orders, 'w', encoding='utf-8') as f:
                f.write(content)
            print('  admin/orders.vue: updated')

            print('\nBackend and admin fixes applied!')
            break
