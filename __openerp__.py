{
    'name': 'Mage2Odoo',
    'version': '1.1',
    'author': 'Kyle Waid',
    'category': 'Sales Management',
    'depends': ['payment_method', 'delivery', 'stock_package', 'product_sku_upc', 'sale_stock', 'asin_label'],
    'website': 'https://www.gcotech.com',
    'description': """ 
    """,
    'data': ['security/mage2odoo_groups.xml',
	     'views/core.xml',
	     'views/attribute.xml',
	     'views/sites.xml',
	     'views/mapping.xml',
	     'views/jobs.xml',
	     'views/product.xml',
	     'views/import_export.xml',
	     'views/product_category.xml',
	     'views/model.xml',
	     'views/misc.xml',
	     'views/sale.xml',
	     'views/stock.xml',
	     'views/delivery.xml',
	     'views/partner.xml',
	     'views/import_exception.xml',
	     'views/export_exception.xml',
	     'views/exception.xml',
	     'views/amazon.xml',
	     'data/mage_shipping.xml',
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'external_dependencies': {
	'python': ['magento', 'pycountry'],
    },
}
