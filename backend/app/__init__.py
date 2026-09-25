from flask import Flask
from flask_cors import CORS
from sqlalchemy import inspect, text
from app.config import Config
from app.extensions import db, migrate, jwt
from app.routes import auth, categories, contact, products, orders, tables
from app.routes import reservations
from app.routes import event_inquiries
from app.routes import contact_messages
from app.models.contact_detail import ContactDetail
from app.models.category import Category
from app.models.product import Product
from app.models.user import User
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.restaurant_table import RestaurantTable
from app.models.event_inquiry import EventInquiry
from app.models.contact_message import ContactMessage


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(categories.bp)
    app.register_blueprint(contact.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(orders.bp)
    app.register_blueprint(reservations.bp)
    app.register_blueprint(tables.bp)
    app.register_blueprint(event_inquiries.bp)
    app.register_blueprint(contact_messages.bp)

    @app.get("/")
    def health_check():
        return {"message": "Restaurant API is running"}

    with app.app_context():
        db.create_all()
        ensure_category_columns()
        ensure_product_columns()
        ensure_order_columns()
        ensure_order_item_columns()
        ensure_order_item_product_id_nullable()
        ensure_reservation_columns()
        ensure_table_columns()
        ensure_user_columns()
        seed_categories()
        seed_products()
        seed_tables()
        seed_contact_details()

    return app


def seed_contact_details():
    if ContactDetail.query.first():
        return

    details = [
        {
            "label": "Reservations",
            "details": "Recommended for dinner and weekend visits",
            "contact": "+1 234 567 8900",
            "contact_url": "tel:+12345678900",
            "sort_order": 1,
        },
        {
            "label": "General inquiries",
            "details": "Menu questions, dietary needs, and feedback",
            "contact": "hello@flavoria.com",
            "contact_url": "mailto:hello@flavoria.com",
            "sort_order": 2,
        },
        {
            "label": "Private events",
            "details": (
                "Intimate dinners, weddings, and corporate celebrations"
            ),
            "contact": "events@flavoria.com",
            "contact_url": "mailto:events@flavoria.com",
            "sort_order": 3,
        },
        {
            "label": "Location",
            "details": "123 Culinary Avenue, Gourmet District",
            "contact": "New York, NY 10001, USA",
            "sort_order": 4,
        },
        {
            "label": "Parking",
            "details": "Valet service available after 5:00 PM",
            "contact": "Street parking nearby",
            "sort_order": 5,
        },
        {
            "label": "Dress code",
            "details": "Smart casual",
            "contact": "Jackets welcome, never required",
            "sort_order": 6,
        },
    ]
    db.session.add_all(ContactDetail(**item) for item in details)
    db.session.commit()



def slugify_category(text):
    return text.lower().replace(" ", "-").replace("&", "and")

def seed_categories():
    category_seeds = (
        ("Starters", "Small plates and appetizers to begin your meal.", "salad", "Pastry & Cold", "https://images.unsplash.com/photo-1541544741938-0af808871cc0?auto=format&fit=crop&w=700&q=80"),
        ("Main Course", "Signature dishes prepared fresh by our kitchen.", "utensils", "Kitchen Grill", "https://images.unsplash.com/photo-1621996346565-e3d5d6281273?auto=format&fit=crop&w=700&q=80"),
        ("Desserts", "Cakes, pastries, and sweet finishes.", "cake", "Pastry & Cold", "https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=700&q=80"),
        ("Beverages", "Refreshing drinks to enjoy with your meal.", "drink", "Bar & Drinks", "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&w=700&q=80"),
        ("Pizza", "Hand-stretched pizzas baked until golden.", "pizza", "Pizza Oven", "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=700&q=80"),
        ("Chef Specials", "Seasonal creations from our chef.", "utensils", "Main Line", "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=700&q=80"),
        ("Salads", "Fresh greens, seasonal vegetables, and house dressings.", "salad", "Pastry & Cold", "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=700&q=80"),
        ("Soups", "Comforting soups prepared with seasonal ingredients.", "utensils", "Main Line", "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=700&q=80"),
        ("Seafood", "Fresh fish and seafood prepared by our kitchen.", "utensils", "Kitchen Grill", "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=700&q=80"),
        ("Pasta", "Classic and house-made pasta dishes.", "pasta", "Main Line", "https://images.unsplash.com/photo-1621996346565-e3d5d6281273?auto=format&fit=crop&w=700&q=80"),
        ("Burgers & Sandwiches", "Handheld favorites made to order.", "burger", "Kitchen Grill", "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=700&q=80"),
        ("Grilled & BBQ", "Fire-grilled favorites with bold, smoky flavor.", "steak", "Kitchen Grill", "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=700&q=80"),
        ("Sides", "Shareable sides and extras for your table.", "utensils", "Main Line", "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&w=700&q=80"),
        ("Kids Menu", "Family-friendly favorites for younger guests.", "burger", "Main Line", "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=700&q=80"),
        ("Breakfast & Brunch", "Morning and brunch dishes for a relaxed start.", "utensils", "Main Line", "https://images.unsplash.com/photo-1533089860892-a7c6f0a88666?auto=format&fit=crop&w=700&q=80"),
        ("Wine & Cocktails", "Wine, cocktails, and thoughtfully mixed drinks.", "drink", "Bar & Drinks", "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&w=700&q=80"),
    )
    existing_names = {category.name for category in Category.query.all()}
    existing_slugs = {category.slug for category in Category.query.all() if category.slug}
    missing_categories = [
        Category(
            name=name,
            slug=slugify_category(name),
            description=description,
            icon=icon,
            station=station,
            image=image,
            status="Active",
            display_order=idx + 1,
        )
        for idx, (name, description, icon, station, image) in enumerate(category_seeds)
        if name not in existing_names and slugify_category(name) not in existing_slugs
    ]
    if missing_categories:
        db.session.add_all(missing_categories)
        db.session.commit()

    # Backfill slugs for legacy categories
    for category in Category.query.all():
        if not category.slug:
            category.slug = (
                category.name.lower().replace(" ", "-").replace("&", "and")
            )
    db.session.commit()


def seed_products():
    product_seeds = (
        ("SEED-001", "Crispy Calamari", "Lightly fried calamari with lemon and house herb aioli.", 14.00, "Starters", "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?auto=format&fit=crop&w=900&q=80"),
        ("SEED-002", "Burrata & Heirloom Tomato", "Creamy burrata, ripe tomatoes, basil, and toasted sourdough.", 16.00, "Starters", "https://images.unsplash.com/photo-1608039829572-78524f79c4c7?auto=format&fit=crop&w=900&q=80"),
        ("SEED-003", "Truffle Parmesan Arancini", "Golden risotto bites with parmesan and black truffle aioli.", 13.00, "Starters", "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=80"),
        ("SEED-004", "Filet Mignon", "Grilled tenderloin with roasted garlic mash and red wine jus.", 38.00, "Main Course", "https://images.unsplash.com/photo-1600891964092-4316c288032e?auto=format&fit=crop&w=900&q=80"),
        ("SEED-005", "Herb Roasted Chicken", "Roasted half chicken with seasonal vegetables and pan jus.", 27.00, "Main Course", "https://images.unsplash.com/photo-1532550907401-a500c9a57435?auto=format&fit=crop&w=900&q=80"),
        ("SEED-006", "Wild Mushroom Risotto", "Creamy arborio rice with wild mushrooms, parmesan, and thyme.", 25.00, "Main Course", "https://images.unsplash.com/photo-1476124369491-e7addf5db371?auto=format&fit=crop&w=900&q=80"),
        ("SEED-007", "Classic Tiramisu", "Espresso-soaked ladyfingers layered with mascarpone cream.", 11.00, "Desserts", "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?auto=format&fit=crop&w=900&q=80"),
        ("SEED-008", "Chocolate Lava Cake", "Warm chocolate cake with a molten center and vanilla gelato.", 12.00, "Desserts", "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=900&q=80"),
        ("SEED-009", "Lemon Meringue Tart", "Bright lemon curd in a crisp pastry shell with toasted meringue.", 10.00, "Desserts", "https://images.unsplash.com/photo-1519915028121-7d3463d20b13?auto=format&fit=crop&w=900&q=80"),
        ("SEED-010", "Strawberry Basil Lemonade", "Fresh strawberries, basil, and house-squeezed lemon.", 7.00, "Beverages", "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&w=900&q=80"),
        ("SEED-011", "Vanilla Bean Cold Brew", "Slow-steeped coffee finished with house vanilla cream.", 6.50, "Beverages", "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=900&q=80"),
        ("SEED-012", "Margherita Pizza", "Wood-fired pizza with tomato, mozzarella, basil, and olive oil.", 19.00, "Pizza", "https://images.unsplash.com/photo-1579751626657-72bc17010498?auto=format&fit=crop&w=900&q=80"),
        ("SEED-013", "Spicy Soppressata Pizza", "Crisp crust topped with soppressata, chili honey, and mozzarella.", 23.00, "Pizza", "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=900&q=80"),
        ("SEED-014", "Pan-Seared Salmon", "Salmon with citrus beurre blanc, greens, and crushed potatoes.", 31.00, "Seafood", "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=900&q=80"),
        ("SEED-015", "Garlic Butter Prawns", "Sautéed prawns with garlic butter, parsley, and grilled bread.", 28.00, "Seafood", "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?auto=format&fit=crop&w=900&q=80"),
        ("SEED-016", "Tagliatelle Bolognese", "Silky tagliatelle with slow-braised beef and parmesan.", 24.00, "Pasta", "https://images.unsplash.com/photo-1551183053-bf91a1d81141?auto=format&fit=crop&w=900&q=80"),
        ("SEED-017", "Truffle Mushroom Burger", "Grilled beef, wild mushrooms, swiss cheese, and truffle mayo.", 22.00, "Burgers & Sandwiches", "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=900&q=80"),
        ("SEED-018", "Slow-Cooked BBQ Ribs", "Tender glazed ribs with smoky barbecue sauce and slaw.", 32.00, "Grilled & BBQ", "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=900&q=80"),
        ("SEED-019", "Harvest Garden Salad", "Mixed greens, seasonal fruit, toasted seeds, and honey vinaigrette.", 16.00, "Salads", "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=900&q=80"),
        ("SEED-020", "Parmesan Truffle Fries", "Crisp fries tossed with parmesan, herbs, and truffle oil.", 9.00, "Sides", "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&w=900&q=80"),
        ("SEED-021", "French Onion Soup", "Slow-caramelized onions, rich beef broth, and bubbling gruyere toast.", 12.00, "Soups", "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=80"),
        ("SEED-022", "Roasted Tomato Bisque", "Velvety roasted tomato soup finished with cream and basil oil.", 11.00, "Soups", "https://images.unsplash.com/photo-1476718406336-bb5a9690ee2a?auto=format&fit=crop&w=900&q=80"),
        ("SEED-023", "Avocado Citrus Salad", "Avocado, orange, baby greens, toasted almonds, and citrus vinaigrette.", 15.00, "Salads", "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=900&q=80"),
        ("SEED-024", "Grilled Lamb Chops", "Rosemary grilled lamb chops with whipped potatoes and mint jus.", 39.00, "Grilled & BBQ", "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=900&q=80"),
        ("SEED-025", "Crispy Chicken Sandwich", "Buttermilk fried chicken, pickles, slaw, and pepper mayo on a brioche bun.", 18.00, "Burgers & Sandwiches", "https://images.unsplash.com/photo-1606755962773-d324e0a13086?auto=format&fit=crop&w=900&q=80"),
        ("SEED-026", "Lemon Ricotta Pancakes", "Fluffy ricotta pancakes with fresh berries and maple butter.", 16.00, "Breakfast & Brunch", "https://images.unsplash.com/photo-1528207776546-365bb710ee93?auto=format&fit=crop&w=900&q=80"),
        ("SEED-027", "Truffle Mac & Cheese", "Baked cavatappi in a three-cheese sauce with a hint of truffle.", 17.00, "Chef Specials", "https://images.unsplash.com/photo-1543339494-b4cd4f7ba686?auto=format&fit=crop&w=900&q=80"),
        ("SEED-028", "Mini Cheeseburger Trio", "Three little beef sliders with cheddar, house sauce, and fries.", 14.00, "Kids Menu", "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=900&q=80"),
        ("SEED-029", "Mediterranean Sharing Platter", "Hummus, olives, grilled pita, marinated vegetables, and feta.", 27.00, "Chef Specials", "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=80"),
        ("SEED-030", "Date Night Dinner Set for Two", "A shareable chef set with burrata, two pastas, and a dessert to finish.", 49.00, "Chef Specials", "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?auto=format&fit=crop&w=900&q=80"),
        ("SEED-031", "Tuscan Pasta Set for Two", "Two bowls of house pasta with garlic bread and a pair of lemonades.", 42.00, "Chef Specials", "https://images.unsplash.com/photo-1551183053-bf91a1d81141?auto=format&fit=crop&w=900&q=80"),
        ("SEED-032", "Family Pizza Feast", "Two wood-fired pizzas with parmesan fries and four soft drinks.", 58.00, "Chef Specials", "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=900&q=80"),
        ("SEED-033", "Seafood Celebration Set", "Pan-seared salmon and garlic prawns served with greens and potatoes.", 69.00, "Chef Specials", "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=900&q=80"),
        ("SEED-034", "Brunch for Two Set", "Ricotta pancakes, a garden salad, and two freshly brewed coffees.", 36.00, "Chef Specials", "https://images.unsplash.com/photo-1528207776546-365bb710ee93?auto=format&fit=crop&w=900&q=80"),
        ("SEED-035", "Sweet Finish Dessert Set", "A tasting trio of tiramisu, lava cake, and lemon tart for sharing.", 28.00, "Chef Specials", "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?auto=format&fit=crop&w=900&q=80"),
        ("SEED-036", "Roasted Red Pepper Hummus", "Creamy hummus with roasted peppers, herbs, and warm grilled pita.", 12.00, "Starters", "https://images.unsplash.com/photo-1577906096429-f73c2c312435?auto=format&fit=crop&w=900&q=80"),
        ("SEED-037", "Crispy Zucchini Fritters", "Golden zucchini fritters with lemon yogurt and fresh dill.", 13.00, "Starters", "https://images.unsplash.com/photo-1608039829572-78524f79c4c7?auto=format&fit=crop&w=900&q=80"),
        ("SEED-038", "Creamy Seafood Linguine", "Linguine with shrimp, mussels, and a light white wine cream sauce.", 29.00, "Pasta", "https://images.unsplash.com/photo-1551183053-bf91a1d81141?auto=format&fit=crop&w=900&q=80"),
        ("SEED-039", "Spinach Ricotta Ravioli", "Pillowy ravioli with spinach ricotta filling and sage butter.", 24.00, "Pasta", "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?auto=format&fit=crop&w=900&q=80"),
        ("SEED-040", "Honey Glazed Pork Belly", "Slow-roasted pork belly with apple slaw and a honey soy glaze.", 26.00, "Grilled & BBQ", "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=900&q=80"),
        ("SEED-041", "Blackened Mahi Mahi Tacos", "Three soft tacos with blackened mahi, cabbage, and lime crema.", 21.00, "Seafood", "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=900&q=80"),
        ("SEED-042", "Wild Berry Cheesecake", "Baked vanilla cheesecake with seasonal berry compote.", 12.00, "Desserts", "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&w=900&q=80"),
        ("SEED-043", "Pistachio Panna Cotta", "Silky vanilla panna cotta with toasted pistachios and honey.", 11.00, "Desserts", "https://images.unsplash.com/photo-1488477181946-6428a0291777?auto=format&fit=crop&w=900&q=80"),
        ("SEED-044", "Mango Passionfruit Spritz", "Sparkling mango and passionfruit with citrus and fresh mint.", 8.00, "Beverages", "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&w=900&q=80"),
        ("SEED-045", "Rosemary Peach Iced Tea", "House-brewed black tea with ripe peach and rosemary.", 6.50, "Beverages", "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=900&q=80"),
        ("SEED-046", "Smoky Chipotle Chicken Burger", "Grilled chicken, pepper jack, avocado, and smoky chipotle sauce.", 20.00, "Burgers & Sandwiches", "https://images.unsplash.com/photo-1606755962773-d324e0a13086?auto=format&fit=crop&w=900&q=80"),
        ("SEED-047", "Roasted Beet & Goat Cheese Salad", "Roasted beets, whipped goat cheese, walnuts, and baby greens.", 16.00, "Salads", "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=900&q=80"),
        ("SEED-048", "Crispy Parmesan Polenta", "Golden polenta bites with parmesan and marinara for dipping.", 10.00, "Sides", "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&w=900&q=80"),
        ("SEED-049", "Buttermilk Chicken Tenders", "Crispy chicken tenders served with fries and honey mustard.", 13.00, "Kids Menu", "https://images.unsplash.com/photo-1562967914-608f82629710?auto=format&fit=crop&w=900&q=80"),
        ("SEED-050", "Steakhouse Chopped Salad", "Chopped greens with sliced steak, tomato, egg, and blue cheese.", 23.00, "Salads", "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=900&q=80"),
    )
    category_ids = {category.name: category.id for category in Category.query.all()}
    existing_skus = {product.sku for product in Product.query.filter(Product.sku.like("SEED-%")).all()}
    new_products = []
    for sku, name, description, price, category_name, image in product_seeds:
        if sku in existing_skus or category_name not in category_ids:
            continue
        new_products.append(Product(
            name=name,
            description=description,
            price=price,
            previous_price={"SEED-024": 46.00, "SEED-025": 22.00, "SEED-030": 58.00}.get(sku),
            rating="4.8",
            image=image,
            category_id=category_ids[category_name],
            sku=sku,
            cost_price=round(price * 0.38, 2),
            stock_quantity=25,
            reorder_level=5,
            status="In Stock",
        ))
    if new_products:
        db.session.add_all(new_products)
        db.session.commit()


def seed_tables():
    if RestaurantTable.query.first():
        return

    tables = [
        RestaurantTable(table_number=1, seats=2, status="available", zone="Main Dining", shape="round", bg_image="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?q=80&w=800&auto=format&fit=crop"),
        RestaurantTable(table_number=2, seats=4, status="occupied", zone="Main Dining", shape="square", bg_image="https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?q=80&w=800&auto=format&fit=crop"),
        RestaurantTable(table_number=3, seats=4, status="occupied", zone="Main Dining", shape="square", bg_image="https://images.unsplash.com/photo-1559339352-11d035aa65de?q=80&w=800&auto=format&fit=crop"),
        RestaurantTable(table_number=4, seats=6, status="reserved", zone="Main Dining", shape="long", bg_image="https://images.unsplash.com/photo-1544161515-4ab6ce6db874?q=80&w=800&auto=format&fit=crop"),
        RestaurantTable(table_number=5, seats=2, status="cleaning", zone="Main Dining", shape="round", bg_image="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?q=80&w=800&auto=format&fit=crop"),
        RestaurantTable(table_number=101, seats=8, status="reserved", zone="VIP Lounge", shape="long", bg_image="https://images.unsplash.com/photo-1578474846511-04ba529f0b88?q=80&w=800&auto=format&fit=crop"),
        RestaurantTable(table_number=102, seats=12, status="occupied", zone="VIP Lounge", shape="long", bg_image="https://images.unsplash.com/photo-1578474846511-04ba529f0b88?q=80&w=800&auto=format&fit=crop"),
        RestaurantTable(table_number=201, seats=4, status="available", zone="Terrace", shape="square", bg_image="https://images.unsplash.com/photo-1537047902294-62a40c20a6ae?q=80&w=800&auto=format&fit=crop"),
        RestaurantTable(table_number=202, seats=4, status="available", zone="Terrace", shape="square", bg_image="https://images.unsplash.com/photo-1537047902294-62a40c20a6ae?q=80&w=800&auto=format&fit=crop"),
        RestaurantTable(table_number=301, seats=2, status="available", zone="Bar", shape="round", bg_image="https://images.unsplash.com/photo-1514933651103-005eec06c4b?q=80&w=800&auto=format&fit=crop"),
    ]
    db.session.add_all(tables)
    db.session.commit()


def ensure_category_columns():
    existing_columns = {
        column["name"]
        for column in inspect(db.engine).get_columns("categories")
    }
    columns = {
        "slug": "VARCHAR(120) NOT NULL DEFAULT ''",
        "description": "TEXT NOT NULL DEFAULT ''",
        "image": "VARCHAR(500) NOT NULL DEFAULT ''",
        "icon": "VARCHAR(40) NOT NULL DEFAULT 'utensils'",
        "station": "VARCHAR(80) NOT NULL DEFAULT 'Main Line'",
        "status": "VARCHAR(20) NOT NULL DEFAULT 'Active'",
        "display_order": "INTEGER NOT NULL DEFAULT 1",
    }
    missing_columns = [
        (name, definition)
        for name, definition in columns.items()
        if name not in existing_columns
    ]
    for name, definition in missing_columns:
        db.session.execute(
            text(f"ALTER TABLE categories ADD COLUMN {name} {definition}")
        )
    if missing_columns:
        db.session.commit()


def ensure_product_columns():
    existing_columns = {
        column["name"] for column in inspect(db.engine).get_columns("products")
    }
    columns = {
        "sku": "VARCHAR(80) NOT NULL DEFAULT ''",
        "previous_price": "FLOAT NULL",
        "cost_price": "FLOAT NOT NULL DEFAULT 0",
        "stock_quantity": "INTEGER NOT NULL DEFAULT 0",
        "reorder_level": "INTEGER NOT NULL DEFAULT 5",
        "status": "VARCHAR(20) NOT NULL DEFAULT 'Out of Stock'",
    }
    missing_columns = [
        (name, definition)
        for name, definition in columns.items()
        if name not in existing_columns
    ]
    for name, definition in missing_columns:
        db.session.execute(
            text(f"ALTER TABLE products ADD COLUMN {name} {definition}")
        )
    if missing_columns:
        db.session.commit()


def ensure_order_columns():
    existing_columns = {
        column["name"] for column in inspect(db.engine).get_columns("orders")
    }
    columns = {
        "order_type": "VARCHAR(20) NOT NULL DEFAULT 'dine-in'",
        "payment_method": "VARCHAR(20) NOT NULL DEFAULT 'cash'",
        "delivery_fee": "FLOAT NOT NULL DEFAULT 0",
        "notes": "TEXT NULL",
        "customer_name": "VARCHAR(160) NULL",
        "customer_email": "VARCHAR(120) NULL",
        "customer_phone": "VARCHAR(40) NULL",
        "table_number": "VARCHAR(20) NULL",
        "delivery_address": "VARCHAR(255) NULL",
        "created_at": "DATETIME NULL",
    }
    missing_columns = [
        (name, definition)
        for name, definition in columns.items()
        if name not in existing_columns
    ]
    for name, definition in missing_columns:
        db.session.execute(
            text(f"ALTER TABLE orders ADD COLUMN {name} {definition}")
        )
    if missing_columns:
        db.session.execute(
            text("UPDATE orders SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL")
        )
        db.session.commit()


def ensure_order_item_product_id_nullable():
    existing_columns = {
        column["name"]
        for column in inspect(db.engine).get_columns("order_items")
    }
    if "product_id" not in existing_columns:
        return
    cols = inspect(db.engine).get_columns("order_items")
    for col in cols:
        if col["name"] == "product_id" and col.get("nullable", False):
            return
    dialect = db.engine.dialect.name
    if dialect == "postgresql":
        db.session.execute(text("ALTER TABLE order_items ALTER COLUMN product_id DROP NOT NULL"))
        db.session.commit()
    elif dialect == "mysql":
        db.session.execute(text("ALTER TABLE order_items MODIFY COLUMN product_id INT NULL"))
        db.session.commit()
    elif dialect == "sqlite":
        db.session.execute(text(
            "CREATE TABLE _order_items_new ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "order_id INTEGER NOT NULL REFERENCES orders(id), "
            "product_id INTEGER REFERENCES products(id), "
            "quantity INTEGER NOT NULL, "
            "price FLOAT NOT NULL, "
            "product_name VARCHAR(120) NOT NULL DEFAULT '', "
            "product_image VARCHAR(500) NOT NULL DEFAULT ''"
            ")"
        ))
        db.session.execute(text(
            "INSERT INTO _order_items_new (id, order_id, product_id, quantity, price, product_name, product_image) "
            "SELECT id, order_id, product_id, quantity, price, product_name, product_image FROM order_items"
        ))
        db.session.execute(text("DROP TABLE order_items"))
        db.session.execute(text("ALTER TABLE _order_items_new RENAME TO order_items"))
        db.session.commit()


def ensure_order_item_columns():
    existing_columns = {
        column["name"] for column in inspect(db.engine).get_columns("order_items")
    }
    columns = {
        "product_name": "VARCHAR(120) NOT NULL DEFAULT ''",
        "product_image": "VARCHAR(500) NOT NULL DEFAULT ''",
    }
    missing_columns = [
        (name, definition)
        for name, definition in columns.items()
        if name not in existing_columns
    ]
    for name, definition in missing_columns:
        db.session.execute(
            text(f"ALTER TABLE order_items ADD COLUMN {name} {definition}")
        )
    if missing_columns:
        db.session.commit()


def ensure_reservation_columns():
    reservation_columns = inspect(db.engine).get_columns("reservations")
    existing_columns = {column["name"] for column in reservation_columns}
    columns = {
        "guest_name": "VARCHAR(160) NULL",
        "guest_email": "VARCHAR(120) NULL",
        "guest_phone": "VARCHAR(40) NULL",
        "booking_type": "VARCHAR(20) NOT NULL DEFAULT 'dining'",
        "area_name": "VARCHAR(100) NOT NULL DEFAULT 'Main Dining Room'",
        "occasion": "VARCHAR(100) NOT NULL DEFAULT 'Casual Fine Dining'",
        "dietary_preferences": "VARCHAR(500) NOT NULL DEFAULT '[]'",
    }
    missing_columns = [
        (name, definition)
        for name, definition in columns.items()
        if name not in existing_columns
    ]
    for name, definition in missing_columns:
        db.session.execute(
            text(f"ALTER TABLE reservations ADD COLUMN {name} {definition}")
        )
    if missing_columns:
        db.session.commit()
    table_id_column = next((column for column in reservation_columns if column["name"] == "table_id"), None)
    if table_id_column and not table_id_column.get("nullable", True) and db.engine.dialect.name == "mysql":
        table_foreign_key = next(
            (
                key for key in inspect(db.engine).get_foreign_keys("reservations")
                if "table_id" in key.get("constrained_columns", [])
            ),
            None,
        )
        if table_foreign_key:
            constraint_name = table_foreign_key["name"].replace("`", "``")
            db.session.execute(text(f"ALTER TABLE reservations DROP FOREIGN KEY `{constraint_name}`"))
        db.session.execute(text("ALTER TABLE reservations MODIFY table_id INT NULL"))
        if table_foreign_key:
            constraint_name = table_foreign_key["name"].replace("`", "``")
            db.session.execute(
                text(
                    f"ALTER TABLE reservations ADD CONSTRAINT `{constraint_name}` "
                    "FOREIGN KEY (table_id) REFERENCES restaurant_tables (id) "
                    "ON UPDATE CASCADE ON DELETE RESTRICT"
                )
            )
        db.session.commit()
    user_id_column = next((column for column in reservation_columns if column["name"] == "user_id"), None)
    if user_id_column and not user_id_column.get("nullable", True) and db.engine.dialect.name == "mysql":
        user_foreign_key = next(
            (
                key for key in inspect(db.engine).get_foreign_keys("reservations")
                if "user_id" in key.get("constrained_columns", [])
            ),
            None,
        )
        if user_foreign_key:
            constraint_name = user_foreign_key["name"].replace("`", "``")
            db.session.execute(text(f"ALTER TABLE reservations DROP FOREIGN KEY `{constraint_name}`"))
        db.session.execute(text("ALTER TABLE reservations MODIFY user_id INT NULL"))
        if user_foreign_key:
            constraint_name = user_foreign_key["name"].replace("`", "``")
            db.session.execute(
                text(
                    f"ALTER TABLE reservations ADD CONSTRAINT `{constraint_name}` "
                    "FOREIGN KEY (user_id) REFERENCES users (id) "
                    "ON UPDATE CASCADE ON DELETE CASCADE"
                )
            )
        db.session.commit()


def ensure_table_columns():
    existing_columns = {
        column["name"]
        for column in inspect(db.engine).get_columns("restaurant_tables")
    }
    columns = {
        "zone": "VARCHAR(40) NOT NULL DEFAULT 'Main Dining'",
        "shape": "VARCHAR(20) NOT NULL DEFAULT 'square'",
        "bg_image": "VARCHAR(500) NOT NULL DEFAULT ''",
    }
    missing_columns = [
        (name, definition)
        for name, definition in columns.items()
        if name not in existing_columns
    ]
    for name, definition in missing_columns:
        db.session.execute(
            text(f"ALTER TABLE restaurant_tables ADD COLUMN {name} {definition}")
        )
    if missing_columns:
        db.session.commit()


def ensure_user_columns():
    existing_columns = {
        column["name"]
        for column in inspect(db.engine).get_columns("users")
    }
    columns = {
        "phone": "VARCHAR(20) NULL",
        "avatar": "VARCHAR(500) NULL",
    }
    missing_columns = [
        (name, definition)
        for name, definition in columns.items()
        if name not in existing_columns
    ]
    for name, definition in missing_columns:
        db.session.execute(
            text(f"ALTER TABLE users ADD COLUMN {name} {definition}")
        )
    if missing_columns:
        db.session.commit()
