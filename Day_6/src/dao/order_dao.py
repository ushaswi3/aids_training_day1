''' Orders Module
Scenario:
A customer comes to buy products. The system must create an order, assign products to it, 
calculate total amount, and manage stock.
Tasks:
Create a new order for a customer.
Input: customer_id and a list of products with quantities (e.g., [{prod_id: 1, qty: 2},
 {prod_id: 3, qty: 1}]).
Check that the customer exists.
Check each product’s stock → if not enough stock, reject order with error.
Deduct stock for purchased products.
Insert order into orders table and order_items table.
Save the total_amount.
Fetch full details of an order (order info + customer info + order items).
List all orders of a customer.
Cancel an order:
Allowed only if status = PLACED.
Restore product stock.
Update order status = CANCELLED.
Mark an order as Completed after payment is successful
'''


# src/dao/order_dao.py
from typing import Optional, List, Dict
from src.config import get_supabase

class OrderDao:
    def __init__(self):
        self._sb = get_supabase()

    # Create order and return the inserted row
    def create_order(self, customer_id: int, total_amount: float = 0.0, status: str = "PLACED") -> Optional[Dict]:
        payload = {"customer_id": customer_id, "total_amount": total_amount, "status": status}
        self._sb.table("orders").insert(payload).execute()
        # Fetch latest order for this customer
        resp = self._sb.table("orders")\
            .select("*")\
            .eq("customer_id", customer_id)\
            .order("order_id", desc=True)\
            .limit(1)\
            .execute()
        return resp.data[0] if resp.data else None

   
    def create_order_items(self, items: list) -> None:
   
        self._sb.table("order_items").insert(items).execute()

    # Fetch order by ID
    def get_order_by_id(self, order_id: int) -> Optional[Dict]:
        resp = self._sb.table("orders").select("*").eq("order_id", order_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    # Fetch order items
    def get_order_items(self, order_id: int) -> List[Dict]:
        resp = self._sb.table("order_items").select("*").eq("order_id", order_id).execute()
        return resp.data or []

    # List orders by customer
    def list_orders_by_customer(self, customer_id: int) -> List[Dict]:
        resp = self._sb.table("orders").select("*").eq("customer_id", customer_id).execute()
        return resp.data or []

    # Update order status
    def update_order_status(self, order_id: int, status: str) -> Optional[Dict]:
        self._sb.table("orders").update({"status": status}).eq("order_id", order_id).execute()
        return self.get_order_by_id(order_id)
    # List all orders
    def list_orders(self) -> list:
        resp = self._sb.table("orders").select("*").execute()
        return resp.data or []