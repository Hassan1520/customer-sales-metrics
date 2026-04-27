{
    "name": "Customer Metrics Dashboard",
    "version": "19.0.1.0.0",
    "summary": "Dashboard for top customer sales metrics",
    "category": "Sales",
    "author": "Hassan",
    "license": "LGPL-3",
    "depends": ["sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/customer_metrics_views.xml",
    ],
    "installable": True,
    "application": False,
}
