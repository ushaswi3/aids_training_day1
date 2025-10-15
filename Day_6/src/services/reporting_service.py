'''
Reporting Module 
Scenario:
The manager wants to see sales reports.
Tasks:
Show top 5 selling products (by total quantity).
Show total revenue in the last month.
Show total orders placed by each customer.
Show customers who placed more than 2 orders.
'''

# src/services/reporting_service.py
from src.dao.order_dao import OrderDao
from src.dao.order_items_dao import OrderItemsDAO
from src.dao.payment_dao import PaymentDao
from datetime import datetime,timedelta,timezone

class ReportingService:
    def __init__(self):
        self.order_items_dao = OrderItemsDAO()
        self.payment_dao = PaymentDao()
        self.order_dao = OrderDao()

    def top_selling_products(self, top_n=5):
        all_items = self.order_items_dao.list_all_order_items()
        product_qty = {}
        for item in all_items:
            pid = item["prod_id"]
            product_qty[pid] = product_qty.get(pid, 0) + item["quantity"]
        sorted_products = sorted(product_qty.items(), key=lambda x: x[1], reverse=True)
        return sorted_products[:top_n]

    def total_revenue_last_month(self):
        all_payments = self.payment_dao.list_all_payments()
        now = datetime.now(timezone.utc)  # make now offset-aware
        start_last_month = (now.replace(day=1) - timedelta(days=1)).replace(day=1)
        end_last_month = now.replace(day=1) - timedelta(days=1)
    
        revenue = sum(
        p["amount"] 
        for p in all_payments 
        if p["status"] == "PAID" 
        and start_last_month <= datetime.fromisoformat(p["paid_at"]) <= end_last_month
    )
        return revenue

    def total_orders_per_customer(self):
        all_orders = self.order_dao.list_orders()
        cust_count = {}
        for o in all_orders:
            cid = o["customer_id"]
            cust_count[cid] = cust_count.get(cid, 0) + 1
        return cust_count

    def customers_with_more_than_two_orders(self):
        counts = self.total_orders_per_customer()
        return [cid for cid, cnt in counts.items() if cnt > 2]