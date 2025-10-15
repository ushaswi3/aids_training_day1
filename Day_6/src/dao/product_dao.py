# src/dao/product_dao.py
from typing import Optional, List, Dict
from src.config import get_supabase
class ProductDao:
    def __init__(self):
        self._sb=get_supabase()

    def create_product(self,name: str, sku: str, price: float, stock: int = 0, category: str | None = None) -> Optional[Dict]:
        """
        Insert a product and return the inserted row (two-step: insert then select by unique sku).
        """
        payload = {"name": name, "sku": sku, "price": price, "stock": stock}
        if category is not None:
            payload["category"] = category
 
        # Insert (no select chaining)
        self._sb.table("products").insert(payload).execute()
 
        # Fetch inserted row by unique column (sku)
        resp = self._sb.table("products").select("*").eq("sku", sku).limit(1).execute()
        return resp.data[0] if resp.data else None
 
    def get_product_by_id(self,prod_id: int) -> Optional[Dict]:
        resp = self._sb.table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
        return resp.data[0] if resp.data else None
 
    def get_product_by_sku(self,sku: str) -> Optional[Dict]:
        resp = self._sb.table("products").select("*").eq("sku", sku).limit(1).execute()
        return resp.data[0] if resp.data else None
 
    def update_product(self,prod_id: int, fields: Dict) -> Optional[Dict]:
        """
        Update and then return the updated row (two-step).
        """
        self._sb.table("products").update(fields).eq("prod_id", prod_id).execute()
        resp = self._sb.table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
        return resp.data[0] if resp.data else None
 
    def delete_product(self,prod_id: int) -> Optional[Dict]:
        # fetch row before delete (so we can return it)
        resp_before = self._sb.table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
        row = resp_before.data[0] if resp_before.data else None
        self._sb.table("products").delete().eq("prod_id", prod_id).execute()
        return row
 
    def list_products(self,limit: int = 100, category: str | None = None) -> List[Dict]:
        q = self._sb.table("products").select("*").order("prod_id", desc=False).limit(limit)
        if category:
            q = q.eq("category", category)
        resp = q.execute()
        return resp.data or []