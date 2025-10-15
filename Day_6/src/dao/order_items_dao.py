# src/dao/order_items_dao.py
from typing import Optional, List, Dict
from src.config import get_supabase

class OrderItemsDAO:
    def __init__(self):
        self._sb = get_supabase()

    def create_order_item(self, order_id: int, prod_id: int, quantity: int) -> Optional[Dict]:
        payload = {"order_id": order_id, "prod_id": prod_id, "quantity": quantity}
        self._sb.table("order_items").insert(payload).execute()
        resp = self._sb.table("order_items").select("*").eq("order_id", order_id).eq("prod_id", prod_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def list_items_by_order(self, order_id: int) -> List[Dict]:
        resp = self._sb.table("order_items").select("*").eq("order_id", order_id).execute()
        return resp.data or []

    def list_all_order_items(self) -> List[Dict]:
        resp = self._sb.table("order_items").select("*").execute()
        return resp.data or []

    def update_quantity(self, order_id: int, prod_id: int, quantity: int) -> Optional[Dict]:
        self._sb.table("order_items").update({"quantity": quantity}).eq("order_id", order_id).eq("prod_id", prod_id).execute()
        resp = self._sb.table("order_items").select("*").eq("order_id", order_id).eq("prod_id", prod_id).limit(1).execute()
        return resp.data[0] if resp.data else None