from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from werkzeug.utils import secure_filename

from datetime import datetime

import os
app = Flask(__name__)



app.config['JWT_SECRET_KEY'] = 'change-this-to-a-random-secret-key'

jwt = JWTManager(app)
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "http://localhost:3000"
            ]
        }
    }
)

app.config['UPLOAD_FOLDER'] = os.path.join(
    app.root_path,
    'static',
    'uploads',
    'menu'
)

# Multipart uploads include file data plus form fields. Allow menu images up to 16 MiB.
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.errorhandler(413)
def request_entity_too_large(_error):
    return jsonify({
        'message': 'Image upload is too large. Maximum size is 16 MB.'
    }), 413

# ---- Database configuration ----
DB_USER = 'root'
DB_PASSWORD = ''
DB_HOST = 'localhost'
DB_NAME = 'restaurant_db'
DB_PORT = '3306'

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# ==================== MODELS (matching the 5-table spec) ====================
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    email = db.Column(
        db.String(120),
        nullable=False,
        unique=True
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default='customer'
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
                if self.created_at else None
        }
class TableModel(db.Model):
    # Named TableModel in Python since "Table" clashes with SQLAlchemy internals;
    # __tablename__ is still exactly "tables" as required by the spec.
    __tablename__ = 'tables'
    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer, nullable=False, unique=True)
    seating_capacity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='available')  # available, occupied, reserved

    def to_dict(self):
        return {
            'id': self.id,
            'table_number': self.table_number,
            'seating_capacity': self.seating_capacity,
            'status': self.status
        }


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    menu_items = db.relationship('MenuItem', backref='category', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class MenuItem(db.Model):
    __tablename__ = 'menu_items'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id'),
        nullable=False
    )
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    is_available = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )
    image_menu = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'name': self.name,
            'price': float(self.price),
            'is_available': self.is_available,
            'image_menu': self.image_menu
        }



class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True
    )

    table_id = db.Column(
        db.Integer,
        db.ForeignKey('tables.id'),
        nullable=False
    )

    order_time = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default='pending'
    )

    total_amount = db.Column(
        db.Float,
        nullable=False,
        default=0.0
    )

    user = db.relationship('User')

    table = db.relationship('TableModel')

    order_details = db.relationship(
        'OrderDetail',
        backref='order',
        cascade='all, delete-orphan'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username
                if self.user else None,
            'table_id': self.table_id,
            'table_number': self.table.table_number
                if self.table else None,
            'order_time': self.order_time.isoformat(),
            'status': self.status,
            'total_amount': float(self.total_amount),
            'order_details': [
                d.to_dict()
                for d in self.order_details
            ]
        }
    

class OrderDetail(db.Model):
    __tablename__ = 'order_details'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    subtotal = db.Column(db.Float, nullable=False)

    menu_item = db.relationship('MenuItem')

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'menu_item_id': self.menu_item_id,
            'menu_item_name': self.menu_item.name if self.menu_item else None,
            'quantity': self.quantity,
            'subtotal': float(self.subtotal)
        }


with app.app_context():
    db.create_all()

     


# ==================== TABLES ENDPOINTS ====================





@app.route('/api/tables', methods=['GET'])
def get_tables():
    tables = TableModel.query.all()
    return jsonify({
        'message': 'Tables retrieved successfully',
        'count': len(tables),
        'data': [t.to_dict() for t in tables]
    }), 200


@app.route('/api/tables', methods=['POST'])
def add_tables():
    """
    Accepts EITHER a single table object OR a list of table objects
    (bulk insert), e.g.:

    Single: { "table_number": 1, "seating_capacity": 4 }
    Bulk:   [ { "table_number": 1, "seating_capacity": 4 }, { ... } ]
    """
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Request body is required'}), 400

    valid_statuses = ['available', 'occupied', 'reserved']

    # ---- Bulk insert ----
    if isinstance(data, list):
        created_tables = []

        for item in data:
            table_number = item.get('table_number')
            seating_capacity = item.get('seating_capacity')
            status = item.get('status', 'available')

            if table_number is None or seating_capacity is None:
                db.session.rollback()
                return jsonify({
                    'message': 'Each table requires table_number and seating_capacity'
                }), 400

            if status not in valid_statuses:
                db.session.rollback()
                return jsonify({
                    'message': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
                }), 400

            table = TableModel(
                table_number=table_number,
                seating_capacity=seating_capacity,
                status=status
            )
            db.session.add(table)
            created_tables.append(table)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Error creating tables', 'error': str(e)}), 400

        return jsonify({
            'message': 'Tables created successfully',
            'count': len(created_tables),
            'data': [t.to_dict() for t in created_tables]
        }), 201

    # ---- Single insert ----
    table_number = data.get('table_number')
    seating_capacity = data.get('seating_capacity')
    status = data.get('status', 'available')

    if table_number is None or seating_capacity is None:
        return jsonify({'message': 'table_number and seating_capacity are required'}), 400

    if status not in valid_statuses:
        return jsonify({
            'message': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
        }), 400

    table = TableModel(
        table_number=table_number,
        seating_capacity=seating_capacity,
        status=status
    )

    try:
        db.session.add(table)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating table', 'error': str(e)}), 400

    return jsonify({
        'message': 'Table created successfully',
        'data': table.to_dict()
    }), 201


@app.route('/api/tables/<int:table_id>/status', methods=['PUT'])
def update_table_status(table_id):
    data = request.get_json()
    new_status = data.get('status')

    valid_statuses = ['available', 'occupied', 'reserved']
    if new_status not in valid_statuses:
        return jsonify({
            'message': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
        }), 400

    table = TableModel.query.get(table_id)
    if not table:
        return jsonify({'message': 'Table not found'}), 404

    table.status = new_status
    db.session.commit()

    return jsonify({
        'message': 'Table status updated successfully',
        'data': table.to_dict()
    }), 200


# ==================== CATEGORIES ENDPOINTS ====================

@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify({
        'message': 'Categories retrieved successfully',
        'count': len(categories),
        'data': [c.to_dict() for c in categories]
    }), 200


@app.route('/api/categories', methods=['POST'])
def add_category():
    """
    Accepts EITHER a single category object OR a list of category objects.
    """
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Request body is required'}), 400

    # ---- Bulk insert ----
    if isinstance(data, list):
        created_categories = []

        for item in data:
            name = item.get('name')
            description = item.get('description')

            if not name:
                db.session.rollback()
                return jsonify({'message': 'name is required'}), 400

            category = Category(name=name, description=description)
            db.session.add(category)
            created_categories.append(category)

        db.session.commit()

        return jsonify({
            'message': 'Categories created successfully',
            'count': len(created_categories),
            'data': [c.to_dict() for c in created_categories]
        }), 201

    # ---- Single insert ----
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({'message': 'name is required'}), 400

    category = Category(name=name, description=description)
    db.session.add(category)
    db.session.commit()

    return jsonify({
        'message': 'Category created successfully',
        'data': category.to_dict()
    }), 201


# ==================== PRODUCTS (MENU ITEMS) ENDPOINTS ====================

@app.route('/api/products', methods=['GET'])
def get_menu_items():
    items = MenuItem.query.filter_by(is_available=True).all()
    return jsonify({
        'message': 'Products retrieved successfully',
        'count': len(items),
        'data': [item.to_dict() for item in items]
    }), 200

@app.route('/api/products', methods=['POST'])
def add_menu_item():
    # Support JSON requests as well as multipart/form-data image uploads.
    # Use FormData only when an image is being uploaded.
    payload = request.get_json(silent=True) if request.is_json else request.form
    category_id = payload.get('category_id')
    name = payload.get('name')
    price = payload.get('price')
    is_available_value = payload.get('is_available', True)
    is_available = str(is_available_value).lower() == 'true'

    # Get uploaded image
    image = request.files.get('image_menu')

    # Validate required fields
    if not category_id or not name or price is None:
        return jsonify({
            'message': 'category_id, name, and price are required'
        }), 400

    # Validate and check category
    try:
        category_id = int(category_id)
    except (TypeError, ValueError):
        return jsonify({
            'message': 'category_id must be a valid integer'
        }), 400

    category = db.session.get(Category, category_id)

    if not category:
        return jsonify({
            'message': f'Category with id {category_id} not found'
        }), 400

    # Validate price
    try:
        price = float(price)
    except ValueError:
        return jsonify({
            'message': 'price must be a valid number'
        }), 400

    # Image filename
    image_filename = None

    # Handle image upload
    if image:

        if image.filename == '':
            return jsonify({
                'message': 'No image selected'
            }), 400

        if not allowed_file(image.filename):
            return jsonify({
                'message': 'Invalid image type. Allowed: png, jpg, jpeg, webp'
            }), 400

        filename = secure_filename(image.filename)

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')

        name_without_ext = os.path.splitext(filename)[0]
        extension = os.path.splitext(filename)[1].lower()

        filename = f'{name_without_ext}_{timestamp}{extension}'

        file_path = os.path.join(
            app.config['UPLOAD_FOLDER'],
            filename
        )

        image.save(file_path)

        image_filename = f'/static/uploads/menu/{filename}'

    # Create menu item
    item = MenuItem(
        category_id=category_id,
        name=name,
        price=price,
        is_available=is_available,
        image_menu=image_filename
    )

    try:
        db.session.add(item)
        db.session.commit()

    except Exception as e:
        db.session.rollback()

        return jsonify({
            'message': 'Error creating product',
            'error': str(e)
        }), 500

    return jsonify({
        'message': 'Product created successfully',
        'data': item.to_dict()
    }), 201


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    item = MenuItem.query.get(product_id)
    if not item:
        return jsonify({'message': 'Product not found'}), 404

    return jsonify({
        'message': 'Product retrieved successfully',
        'data': item.to_dict()
    }), 200




@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    item = db.session.get(MenuItem, product_id)
    if not item:
        return jsonify({'message': 'Product not found'}), 404

    # JSON is used by the admin edit form; multipart is used when uploading an image.
    payload = request.get_json(silent=True) if request.is_json else request.form
    category_id = payload.get('category_id')
    name = payload.get('name')
    price = payload.get('price')
    is_available = payload.get('is_available')

    # Update category
    if category_id is not None:
        try:
            category_id = int(category_id)
        except (TypeError, ValueError):
            return jsonify({'message': 'category_id must be a valid integer'}), 400

        category = db.session.get(Category, category_id)

        if not category:
            return jsonify({
                'message': f'Category with id {category_id} not found'
            }), 400

        item.category_id = category_id

    # Update name
    if name:
        item.name = name

    # Update price
    if price is not None:
        try:
            item.price = float(price)
        except (TypeError, ValueError):
            return jsonify({
                'message': 'price must be a valid number'
            }), 400

    # Update availability
    if is_available is not None:
        item.is_available = str(is_available).lower() == 'true'

    # Update image
    image = request.files.get('image_menu')

    if image:

        if image.filename == '':
            return jsonify({
                'message': 'No image selected'
            }), 400

        if not allowed_file(image.filename):
            return jsonify({
                'message': 'Invalid image type'
            }), 400

        filename = secure_filename(image.filename)

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')

        name_without_ext = os.path.splitext(filename)[0]
        extension = os.path.splitext(filename)[1].lower()

        filename = f'{name_without_ext}_{timestamp}{extension}'

        file_path = os.path.join(
            app.config['UPLOAD_FOLDER'],
            filename
        )

        image.save(file_path)

        item.image_menu = f'/static/uploads/menu/{filename}'

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating product', 'error': str(e)}), 500

    return jsonify({
        'message': 'Product updated successfully',
        'data': item.to_dict()
    }), 200


@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    item = db.session.get(MenuItem, product_id)
    if not item:
        return jsonify({'message': 'Product not found'}), 404

    try:
        db.session.delete(item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting product', 'error': str(e)}), 500

    return jsonify({'message': 'Product deleted successfully'}), 200


@app.route('/api/orders', methods=['GET'])
def get_all_orders():
    orders = Order.query.order_by(Order.order_time.desc()).all()
    return jsonify({
        'message': 'Orders retrieved successfully',
        'count': len(orders),
        'data': [o.to_dict() for o in orders]
    }), 200


@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order_by_id(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    return jsonify({
        'message': 'Order retrieved successfully',
        'data': order.to_dict()
    }), 200


@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """
    Expected JSON body: { "status": "preparing" }
    Valid statuses: pending, preparing, served, paid
    """
    data = request.get_json()
    new_status = data.get('status')

    valid_statuses = ['pending', 'preparing', 'served', 'paid']
    if new_status not in valid_statuses:
        return jsonify({
            'message': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
        }), 400

    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    order.status = new_status

    # Free up the table once the bill is paid
    if new_status == 'paid' and order.table:
        order.table.status = 'available'

    db.session.commit()

    return jsonify({
        'message': 'Order status updated successfully',
        'data': order.to_dict()
    }), 200


@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Request body is required'
        }), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')

    if not username or not email or not password or not full_name:
        return jsonify({
            'message': 'username, email, password, and full_name are required'
        }), 400

    if len(password) < 6:
        return jsonify({
            'message': 'Password must be at least 6 characters'
        }), 400

    existing_username = User.query.filter_by(
        username=username
    ).first()

    if existing_username:
        return jsonify({
            'message': 'Username already exists'
        }), 409

    existing_email = User.query.filter_by(
        email=email
    ).first()

    if existing_email:
        return jsonify({
            'message': 'Email already exists'
        }), 409

    user = User(
        username=username,
        email=email,
        full_name=full_name,
        role='customer'
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'Registration successful',
        'data': user.to_dict()
    }), 201



@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({
            'message': 'Username and password are required'
        }), 400

    user = User.query.filter(
        db.or_(
            User.username == username,
            User.email == username
        )
    ).first()

    if not user:
        return jsonify({
            'message': 'Invalid username or password'
        }), 401

    if not user.check_password(password):
        return jsonify({
            'message': 'Invalid username or password'
        }), 401

    if not user.is_active:
        return jsonify({
            'message': 'Account is disabled'
        }), 403

    access_token = create_access_token(
        identity=str(user.id)
    )

    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'data': user.to_dict()
    }), 200


@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()

    user = db.session.get(User, int(user_id))

    if not user:
        return jsonify({
            'message': 'User not found'
        }), 404

    return jsonify({
        'message': 'User retrieved successfully',
        'data': user.to_dict()
    }), 200
@app.route('/api/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.order_by(
        User.created_at.desc()
    ).all()

    return jsonify({
        'message': 'Users retrieved successfully',
        'count': len(users),
        'data': [user.to_dict() for user in users]
    }), 200
@app.route('/api/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = db.session.get(User, user_id)

    if not user:
        return jsonify({
            'message': 'User not found'
        }), 404

    return jsonify({
        'message': 'User retrieved successfully',
        'data': user.to_dict()
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
