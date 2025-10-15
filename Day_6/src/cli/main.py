# src/cli/main.py
import argparse
import json
from src.services.product_service import ProductService, ProductError
from src.services.customer_service import CustomerService, CustomerError
from src.services.order_service import OrderService, OrderError
from src.services.payment_service import PaymentService, PaymentError
from src.services.reporting_service import ReportingService

# ------------------- SERVICES -------------------
product_service = ProductService()
customer_service = CustomerService()
order_service = OrderService()
payment_service = PaymentService()
reporting_service = ReportingService()

# ------------------- PRODUCT COMMANDS -------------------
def cmd_product_add(args):
    try:
        p = product_service.add_product(args.name, args.sku, args.price, args.stock, args.category)
        print("Created product:")
        print(json.dumps(p, indent=2, default=str))
    except ProductError as e:
        print("Error:", e)

def cmd_product_list(args):
    ps = product_service.list_products()
    print(json.dumps(ps, indent=2, default=str))

# ------------------- CUSTOMER COMMANDS -------------------
def cmd_customer_add(args):
    try:
        c = customer_service.add_customer(args.name, args.email, args.phone, args.city)
        print("Created customer:")
        print(json.dumps(c, indent=2, default=str))
    except CustomerError as e:
        print("Error:", e)

def cmd_customer_list(args):
    cs = customer_service.list_customers()
    print(json.dumps(cs, indent=2, default=str))

# ------------------- ORDER COMMANDS -------------------
def parse_order_items(raw_items):
    """Convert ['1:2', '3:5'] → [{'prod_id': 1, 'quantity': 2}, ...]"""
    items = []
    for it in raw_items:
        try:
            pid, qty = map(int, it.split(":"))
            items.append({"prod_id": pid, "quantity": qty})
        except Exception:
            raise ValueError(f"Invalid item format: {it}. Use prod_id:qty")
    return items

def cmd_order_create(args):
    try:
        items = parse_order_items(args.item)
        o = order_service.create_order(args.customer, items)
        print("Order created:")
        print(json.dumps(o, indent=2, default=str))
    except (OrderError, ValueError) as e:
        print("Error:", e)

def cmd_order_show(args):
    try:
        o = order_service.get_order_details(args.order)
        print(json.dumps(o, indent=2, default=str))
    except OrderError as e:
        print("Error:", e)

def cmd_order_cancel(args):
    try:
        o = order_service.cancel_order(args.order)
        print("Order cancelled:")
        print(json.dumps(o, indent=2, default=str))
    except OrderError as e:
        print("Error:", e)

# ------------------- PAYMENT COMMANDS -------------------
def cmd_payment_process(args):
    try:
        p = payment_service.process_payment(args.order, args.method)
        print("Payment processed:")
        print(json.dumps(p, indent=2, default=str))
    except PaymentError as e:
        print("Error:", e)

def cmd_payment_refund(args):
    try:
        p = payment_service.refund_payment(args.order)
        print("Payment refunded:")
        print(json.dumps(p, indent=2, default=str))
    except PaymentError as e:
        print("Error:", e)

# ------------------- REPORTING COMMANDS -------------------
def cmd_report_top_products(args):
    top = reporting_service.top_selling_products()
    print("Top Selling Products:")
    print(json.dumps(top, indent=2, default=str))

def cmd_report_revenue(args):
    revenue = reporting_service.total_revenue_last_month()
    print(f"Total Revenue Last Month: {revenue}")

def cmd_report_orders_per_customer(args):
    data = reporting_service.total_orders_per_customer()
    print("Total Orders Per Customer:")
    print(json.dumps(data, indent=2, default=str))

def cmd_report_frequent_customers(args):
    data = reporting_service.customers_with_more_than_two_orders()
    print("Customers with more than 2 orders:")
    print(json.dumps(data, indent=2, default=str))

# ------------------- ARGUMENT PARSER -------------------
def build_parser():
    parser = argparse.ArgumentParser(prog="retail-cli")
    sub = parser.add_subparsers(dest="cmd")

    # Product commands
    p_prod = sub.add_parser("product")
    pprod_sub = p_prod.add_subparsers(dest="action")
    addp = pprod_sub.add_parser("add")
    addp.add_argument("--name", required=True)
    addp.add_argument("--sku", required=True)
    addp.add_argument("--price", type=float, required=True)
    addp.add_argument("--stock", type=int, default=0)
    addp.add_argument("--category", default=None)
    addp.set_defaults(func=cmd_product_add)
    listp = pprod_sub.add_parser("list")
    listp.set_defaults(func=cmd_product_list)

    # Customer commands
    p_cust = sub.add_parser("customer")
    cust_sub = p_cust.add_subparsers(dest="action")
    addc = cust_sub.add_parser("add")
    addc.add_argument("--name", required=True)
    addc.add_argument("--email", required=True)
    addc.add_argument("--phone", required=True)
    addc.add_argument("--city", default=None)
    addc.set_defaults(func=cmd_customer_add)
    listc = cust_sub.add_parser("list")
    listc.set_defaults(func=cmd_customer_list)

    # Order commands
    p_order = sub.add_parser("order")
    order_sub = p_order.add_subparsers(dest="action")
    createo = order_sub.add_parser("create")
    createo.add_argument("--customer", type=int, required=True)
    createo.add_argument("--item", nargs="+", required=True, help="prod_id:qty")
    createo.set_defaults(func=cmd_order_create)
    showo = order_sub.add_parser("show")
    showo.add_argument("--order", type=int, required=True)
    showo.set_defaults(func=cmd_order_show)
    canco = order_sub.add_parser("cancel")
    canco.add_argument("--order", type=int, required=True)
    canco.set_defaults(func=cmd_order_cancel)

    # Payment commands
    p_pay = sub.add_parser("payment")
    pay_sub = p_pay.add_subparsers(dest="action")
    processp = pay_sub.add_parser("process")
    processp.add_argument("--order", type=int, required=True)
    processp.add_argument("--method", required=True)
    processp.set_defaults(func=cmd_payment_process)
    refundp = pay_sub.add_parser("refund")
    refundp.add_argument("--order", type=int, required=True)
    refundp.set_defaults(func=cmd_payment_refund)

    # Reporting commands
    p_report = sub.add_parser("report")
    report_sub = p_report.add_subparsers(dest="action")
    top_products = report_sub.add_parser("top-products")
    top_products.set_defaults(func=cmd_report_top_products)
    revenue = report_sub.add_parser("revenue")
    revenue.set_defaults(func=cmd_report_revenue)
    orders_cust = report_sub.add_parser("orders-per-customer")
    orders_cust.set_defaults(func=cmd_report_orders_per_customer)
    freq_cust = report_sub.add_parser("frequent-customers")
    freq_cust.set_defaults(func=cmd_report_frequent_customers)

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)

if __name__ == "__main__":
    main()