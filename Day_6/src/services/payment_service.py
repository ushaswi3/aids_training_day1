# src/services/payment_service.py
from typing import Dict
from src.dao.payment_dao import PaymentDao
from src.dao.order_dao import OrderDao 

class PaymentError(Exception):
    pass

class PaymentService:
    def __init__(self):
        self.dao = PaymentDao()
        self.order_dao = OrderDao()

    def create_pending_payment(self, order_id: int, total_amount: float) -> Dict:
        return self.dao.create_payment(order_id, total_amount)

    # src/services/payment_service.py
    def process_payment(self, order_id: int, method: str) -> Dict:
        order = self.order_dao.get_order_by_id(order_id)
        if not order:
            raise PaymentError("Order not found")
    
        payment = self.dao.get_payment_by_order(order_id) 
        if not payment:
            raise PaymentError("Payment record not found")

        # update payment and order
        self.dao.update_payment(order_id, {"status": "PAID", "method": method})
        self.order_dao.update_order_status(order_id, "COMPLETED")
    
        return self.dao.get_payment_by_order(order_id)  


    def refund_payment(self, order_id: int) -> Dict:
        payment = self.dao.get_payment_by_order(order_id)
        if not payment:
            raise PaymentError("Payment record not found")
        self.dao.update_payment(order_id, {"status": "REFUNDED"})
        return self.dao.get_payment_by_order(order_id)