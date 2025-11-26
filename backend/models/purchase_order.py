
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    id = Column(Integer, primary_key=True)
    procurement_id = Column(Integer, ForeignKey("procurements.id"))
    total_price = Column(Integer)
    delivery_time = Column(String)
    delivery_conditions = Column(String)
    warranty = Column(String)
    place_of_delivery = Column(String)
    payment_schedule = Column(String)
    file_path = Column(String)
