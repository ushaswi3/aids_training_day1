# src/dao/payment_dao.py
from src.config import get_supabase

class PaymentDao:
    def __init__(self):
        self._sb = get_supabase()

    def create_payment(self, order_id: int, amount: float):
        payload = {
            "order_id": order_id,
            "amount": amount,
            "status": "PENDING"
        }
        resp = self._sb.table("payments").insert(payload).execute()
        return resp.data[0] if resp.data else None

    def get_payment_by_order(self, order_id: int):
        resp = self._sb.table("payments").select("*").eq("order_id", order_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def update_payment(self, order_id: int, fields: dict):
        self._sb.table("payments").update(fields).eq("order_id", order_id).execute()

    def list_all_payments(self):
        resp = self._sb.table("payments").select("*").execute()
        return resp.data or []