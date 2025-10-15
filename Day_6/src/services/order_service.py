# src/services/order_service.py
from typing import List, Dict
from src.dao.order_dao import OrderDao
from src.dao.product_dao import ProductDao
from src.dao.customer_dao import CustomerDao

class OrderError(Exception):
    pass

class OrderService:
    def __init__(self):
        self.dao = OrderDao()
        self.prod_dao = ProductDao()
        self.cust_dao = CustomerDao()

    def create_order(self, customer_id: int, items: List[Dict]) -> Dict:
        # 1️⃣ Check if customer exists
        if not self.cust_dao.get_customer_by_id(customer_id):
            raise OrderError("Customer not found")

        # 2️⃣ Validate stock for all items first
        for item in items:
            prod = self.prod_dao.get_product_by_id(item["prod_id"])
            if not prod:
                raise OrderError(f"Product {item['prod_id']} not found")
            if (prod.get("stock") or 0) < item["quantity"]:
                raise OrderError(f"Not enough stock for product {prod['name']}")

        # 3️⃣ Deduct stock & add price_per_unit
        for item in items:
            prod = self.prod_dao.get_product_by_id(item["prod_id"])
            new_stock = prod["stock"] - item["quantity"]
            self.prod_dao.update_product(item["prod_id"], {"stock": new_stock})
            item["price_per_unit"] = prod["price"]

        # 4️⃣ Calculate total amount
        total_amount = sum(item["quantity"] * item["price_per_unit"] for item in items)

        # 5️⃣ Insert order
        order = self.dao.create_order(customer_id, total_amount)

        # 6️⃣ Insert all order items in batch
        payloads = []
        for item in items:
            payloads.append({
                "order_id": order["order_id"],
                "prod_id": item["prod_id"],
                "quantity": item["quantity"],
                "price": item["price_per_unit"]
            })
        self.dao.create_order_items(payloads)

        # 7️⃣ Return full order with items
        order["items"] = items
        return order

    # Fetch full order details
    def get_order_details(self, order_id: int) -> Dict:
        order = self.dao.get_order_by_id(order_id)
        if not order:
            raise OrderError("Order not found")
        order["items"] = self.dao.get_order_items(order_id)
        order["customer"] = self.cust_dao.get_customer_by_id(order["customer_id"])
        return order

    # Cancel an order
    def cancel_order(self, order_id: int) -> Dict:
        order = self.dao.get_order_by_id(order_id)
        if not order:
            raise OrderError("Order not found")
        if order["status"] != "PLACED":
            raise OrderError("Only PLACED orders can be cancelled")

        # Restore stock
        items = self.dao.get_order_items(order_id)
        for item in items:
            prod = self.prod_dao.get_product_by_id(item["prod_id"])
            new_stock = (prod.get("stock") or 0) + item["quantity"]
            self.prod_dao.update_product(item["prod_id"], {"stock": new_stock})

        # Update status
        return self.dao.update_order_status(order_id, "CANCELLED")

    # Complete an order
    def complete_order(self, order_id: int) -> Dict:
        order = self.dao.get_order_by_id(order_id)
        if not order:
            raise OrderError("Order not found")
        return self.dao.update_order_status(order_id, "COMPLETED")

    # List orders for a customer
    def list_orders_by_customer(self, customer_id: int) -> List[Dict]:
        orders = self.dao.list_orders_by_customer(customer_id)
        for order in orders:
            order["items"] = self.dao.get_order_items(order["order_id"])
        return orders