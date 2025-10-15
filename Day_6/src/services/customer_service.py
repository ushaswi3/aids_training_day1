'''  Customers Module
Scenario:
The store now wants to manage customer information. Each customer can place multiple orders. You must build features to handle Customer Management.
Tasks:
Create a new customer with details → name, email, phone, city.
Validate that email must be unique.
If email already exists, show an error.
Update a customer’s phone or city.
Delete a customer:
Allow deletion only if the customer has no orders.
If orders exist, block deletion with an error message.
List all customers.
Search customer by email or city.
'''

from typing import List, Dict
from src.dao.customer_dao import CustomerDao

class CustomerError(Exception):
    pass

class CustomerService:
    def __init__(self):
        self.dao = CustomerDao()

    def add_customer(self, name: str, email: str, phone: str, city: str | None = None) -> Dict:
        existing = self.dao.get_customer_by_email(email)
        if existing:
            raise CustomerError(f"Email already exists: {email}")
        return self.dao.create_customer(name, email, phone, city)

    def update_customer(self, cust_id: int, phone: str | None = None, city: str | None = None) -> Dict:
        fields = {}
        if phone:
            fields["phone"] = phone
        if city:
            fields["city"] = city
        if not fields:
            raise CustomerError("Nothing to update")
        return self.dao.update_customer(cust_id, fields)

    def delete_customer(self, cust_id: int, has_orders: bool = False) -> Dict:
        if has_orders:
            raise CustomerError("Cannot delete customer with existing orders")
        return self.dao.delete_customer(cust_id)

    def list_customers(self) -> List[Dict]:
        return self.dao.list_customers()