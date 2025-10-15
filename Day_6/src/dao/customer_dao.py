'''  Customers Module
Scenario:
The store now wants to manage customer information. Each customer can place multiple orders. 
You must build features to handle Customer Management.
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


# src/dao/customer_dao.py
from typing import Optional, List, Dict
from src.config import get_supabase

class CustomerDao:
    def __init__(self):
        self._sb = get_supabase()

    def create_customer(self, name: str, email: str, phone: str, city: str | None = None) -> Optional[Dict]:
        # check uniqueness
        if self.get_customer_by_email(email):
            return None
        payload = {"name": name, "email": email, "phone": phone}
        if city:
            payload["city"] = city
        self._sb.table("customers").insert(payload).execute()
        resp = self._sb.table("customers").select("*").eq("email", email).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_customer_by_email(self, email: str) -> Optional[Dict]:
        resp = self._sb.table("customers").select("*").eq("email", email).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_customer_by_id(self, cust_id: int) -> Optional[Dict]:
        resp = self._sb.table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def update_customer(self, cust_id: int, fields: Dict) -> Optional[Dict]:
        self._sb.table("customers").update(fields).eq("cust_id", cust_id).execute()
        resp = self._sb.table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def delete_customer(self, cust_id: int) -> Optional[Dict]:
        # check if customer has orders
        orders = self._sb.table("orders").select("*").eq("customer_id", cust_id).execute()
        if orders.data:
            raise Exception("Cannot delete customer with existing orders")
        resp_before = self._sb.table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
        row = resp_before.data[0] if resp_before.data else None
        self._sb.table("customers").delete().eq("cust_id", cust_id).execute()
        return row

    def list_customers(self, limit: int = 100) -> List[Dict]:
        resp = self._sb.table("customers").select("*").order("cust_id", desc=False).limit(limit).execute()
        return resp.data or []

    def search_customers(self, email: str | None = None, city: str | None = None) -> List[Dict]:
        q = self._sb.table("customers").select("*")
        if email:
            q = q.eq("email", email)
        if city:
            q = q.eq("city", city)
        resp = q.execute()
        return resp.data or []