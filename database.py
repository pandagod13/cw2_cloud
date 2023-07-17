from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine("sqlite:///waiter_mobile_app.db")
Base = declarative_base()

class Waitstaff(Base):
    __tablename__ = "waitstaff"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    photo = Column(String)
    mobile_phone = Column(String)
    address = Column(String)
    orders = relationship("Order", back_populates="waitstaff")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    waitstaff_id = Column(Integer, ForeignKey("waitstaff.id"))
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    menu_item = Column(String)
    quantity = Column(Integer)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Database Operations
def create_waitstaff(username, password, photo, mobile_phone, address):
    waitstaff = Waitstaff(
        username=username,
        password=password,
        photo=photo,
        mobile_phone=mobile_phone,
        address=address
    )
    session.add(waitstaff)
    session.commit()

def get_waitstaff_by_username(username):
    return session.query(Waitstaff).filter_by(username=username).first()

def create_order(waitstaff, items):
    order = Order(waitstaff=waitstaff)
    for item in items:
        order_item = OrderItem(menu_item=item["menu_item"], quantity=item["quantity"])
        order.items.append(order_item)
    session.add(order)
    session.commit()

def get_orders():
    return session.query(Order).all()

# Example usage of database operations
create_waitstaff("waiter", "password", "photo.jpg", "1234567890", "123 Street")
waitstaff = get_waitstaff_by_username("waiter")
create_order(waitstaff, [{"menu_item": "Burger", "quantity": 2}, {"menu_item": "Pizza", "quantity": 1}])
orders = get_orders()
for order in orders:
    print(f"Order ID: {order.id}, Waitstaff: {order.waitstaff.username}, Items: {len(order.items)}")

