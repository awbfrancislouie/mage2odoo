PRODUCT_DEFAULT_MAP = [
{'external_type': 'unicode',
 'field_model': 'product.template',
 'field_name': 'weight',
 'function_name': '',
 'mage_fieldname': 'weight',
 'mapping_type': 'direct',
 'name': 'Product',
 'type': 'in_out'},
{'external_type': 'unicode',
 'field_model': 'product.template',
 'field_name': 'standard_price',
 'function_name': '',
 'mage_fieldname': 'cost',
 'mapping_type': 'direct',
 'name': 'Product',
 'type': 'in_out'},
{'external_type': 'unicode',
 'field_model': 'product.template',
 'field_name': 'upc',
 'function_name': '',
 'mage_fieldname': 'upc',
 'mapping_type': 'direct',
 'name': 'Product',
 'type': 'in_out'},
{'external_type': 'unicode',
 'field_model': 'product.template',
 'field_name': 'list_price',
 'function_name': '',
 'mage_fieldname': 'price',
 'mapping_type': 'direct',
 'name': 'Product',
 'type': 'in_out'},
]


DEFAULT_JOBS = [
                {'name': 'Sync All Products',
                 'mapping_model_name': 'product.product',
                 'python_function_name': 'import_all_products',
                 'job_type': 'system',
		 'scheduler': False,
		 'mapping_name': 'Product',
		 'mapping_lines': PRODUCT_DEFAULT_MAP},
                {'name': 'Sync Updated Products',
                 'mapping_model_name': 'product.product',
                 'python_function_name': 'import_updated_products',
                 'job_type': 'system',
		 'scheduler': True,
		 'mapping_name': 'Product',
		 'mapping_lines': PRODUCT_DEFAULT_MAP},
                {'name': 'Sync Sales Orders',
                 'mapping_model_name': 'sale.order',
                 'python_function_name': 'import_sales_orders',
                 'job_type': 'system',
		 'scheduler': True,
                 'mapping_name': 'Sale Order',
                 'mapping_lines': ''},
                {'name': 'Sync Categories',
                 'mapping_model_name': 'product.category',
                 'python_function_name': 'import_categories',
                 'job_type': 'system',
                 'scheduler': False,
                 'mapping_name': 'Category',
                 'mapping_lines': ''},
                {'name': 'Sync Packages',
                 'mapping_model_name': '',
                 'python_function_name': 'sync_packages',
                 'job_type': 'system',
		 'scheduler': True,
                 'mapping_name': '',
                 'mapping_lines': ''},
                {'name': 'Sync Payments',
                 'mapping_model_name': '',
                 'python_function_name': 'sync_invoices',
                 'job_type': 'system',
		 'scheduler': True,
                 'mapping_name': '',
                 'mapping_lines': ''},
                {'name': 'Sync Configurable Relationship',
                 'mapping_model_name': 'product.template',
                 'python_function_name': 'import_configurable_links',
                 'job_type': 'system',
                 'scheduler': False,
                 'mapping_name': '',
                 'mapping_lines': ''},
                {'name': 'Sync Metadata',
                 'mapping_model_name': '',
                 'python_function_name': 'sync_mage_metadata',
                 'job_type': 'system',
                 'scheduler': False,
                 'mapping_name': '',
                 'mapping_lines': ''},
                {'name': 'Sync Attribute Data',
		 'mapping_model_name': '',
                 'python_function_name': 'sync_mage_attribute_data',
                 'job_type': 'system',
                 'scheduler': False,
                 'mapping_name': '',
                 'mapping_lines': ''},
]
