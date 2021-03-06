from openerp.osv import osv, fields
from magento import Product
from pprint import pprint as pp
from openerp.tools.translate import _
import urllib
import base64

PRODUCT_TYPES = {
                'simple': 'product',
                'configurable': 'service',
                'bundle': 'service',
                'grouped': 'product',
                'virtual': 'service',
}


class ProductTemplate(osv.osv):
    _inherit = 'product.template'
    _columns = {
	'msrp': fields.float('MSRP'),
	'special_price': fields.float('Special Price'),
	'mage_last_sync_date': fields.datetime('Last Mage Sync Date', copy=False),
	'sync_stock': fields.boolean('Sync Stock'),
        'always_in_stock': fields.boolean('Always in Stock'),
        'manage_stock': fields.boolean('Manage Stock'),
        'use_config_manage_stock': fields.boolean('Use Config Manage Stock'),
	'shipping_product': fields.boolean('Shipping Product', help="Used to create totals like Magento"),
	'set': fields.many2one('product.attribute.set', 'Attribute Set'),
	'short_description': fields.text('Short Descripton'),
	'msrp': fields.float('MSRP'),
	'img_path': fields.char('Image Path'),
	'url_path': fields.char('URL Path'),
	'categories': fields.many2many('product.category', 'mage_product_categories_rel', \
		'product_id', 'category_id', 'Categories'
	),
	'websites': fields.many2many('mage.website', 'mage_product_website_rel', 'product_tmpl_id', \
		'website_id', 'Websites'
	),
	'associated_products': fields.many2many('product.template', 'associated_products_rel', \
		'parent_id', 'product_tmpl_id', 'Associated Products', domain="[('mage_type', '!=', 'configurable')]"
	),
        'mage_tax_class': fields.many2one('product.attribute.value', 'Mage Tax Class',
                domain="[('attribute_code', '=', 'tax_class_id')]"),
	'special_price': fields.float('Special Price'),
	'visibility': fields.selection([
					('1', 'Not Visible Individually'),
					('2', 'Catalog'),
					('3', 'Search'),
					('4', 'Catalog, Search'),
	], 'Visibility'),
        'mage_status': fields.selection([
                                       ('1', 'Enabled'),
                                       ('2', 'Disabled'),
        ], 'Magento Status'),
        'mage_type': fields.selection([
                                       ('simple', 'Simple Product'),
                                       ('grouped', 'Grouped Product'),
                                       ('configurable', 'Configurable Product'),
                                       ('bundle', 'Bundle Product'),
				       ('ugiftcert', 'Gift Certificate'),
				       ('virtual', 'Virtual'),
        ], 'Mage Product Type'),
	'url_key': fields.char('URL Key'),
	'external_id': fields.integer('External Id', select=True, copy=False),
	'sync_to_mage': fields.boolean('Magento Sync', copy=False),
        'super_attributes': fields.many2many('product.attribute',
                'product_super_attribute_rel', 'product_tmpl_id', 'attribute_id', 'Super Attributes',
		domain="[('scope', '=', '1'), ('is_configurable', '=', True), ('is_user_defined', '=', True), ('frontend_input', '=', 'select')]"),
    }

    def get_or_create_odoo_record(self, cr, uid, job, external_id):
	#This is not allowed
	raise


class ProductProduct(osv.osv):
    _inherit = 'product.product'


    _sql_constraints = [('default_code_uniq', 'unique (default_code)', 'The SKU must be unique!')]

<<<<<<< HEAD
    def button_create_product_in_magento(self, cr, uid, ids, context=None):
	for product_id in ids:
	    self.push_shell_product_to_mage(cr, uid, product_id)

	return True


    def push_shell_product_to_mage(self, cr, uid, product_id, context=None):
	job_obj = self.pool.get('mage.job')
	product = self.browse(cr, uid, product_id)
	vals = {
	    'name': product.name,
	    'set': product.set.external_id,
	    'type': product.mage_type,
	}

	job_obj.create_one_mage_product(cr, uid, product, vals)


    def sql_product_search(self, cr, uid, default_code):
	query = "SELECT id FROM product_product WHERE default_code = '%s'" % default_code
	cr.execute(query)
	results = cr.fetchall()
	product_ids = [res[0] for res in results]
	return product_ids


    def get_or_create_special_product_vals(self, cr, uid, item, context=None):

#	product_ids = self.search(cr, uid, [('default_code', '=', item['sku'])])
	product_ids = self.sql_product_search(cr, uid, item['sku'])
	if product_ids:
	    return self.browse(cr, uid, product_ids[0])

	else:
	    vals = {
		'name': item.get('description') or item['sku'],
		'default_code': item['sku'],
		'active': True,
		'categories': [(5)],
		'type': 'service',
	    }

	    product = self.create(cr, uid, vals)
	    return self.browse(cr, uid, product)


    def get_or_create_odoo_record(self, cr, uid, job, external_id, item=False, context=None):
	if external_id and int(external_id) == 0 and item:
	    return self.get_or_create_special_product_vals(cr, uid, item)

        product_id = self.get_mage_record(cr, uid, external_id)
	if not product_id and item:
	    product_ids = self.sql_product_search(cr, uid, item['sku'])
	   # product_ids = self.search(cr, uid, [('default_code', '=', item['sku'])])
	    if product_ids:
		product_id = product_ids[0]

	if not product_id:
	    product_id = self.get_and_create_mage_record(cr, uid, job, 'oo_catalog_product.info', external_id)

	return self.browse(cr, uid, product_id)


    def apply_taxes(self, cr, uid, job, record, context=None):
	instance = job.mage_instance
	if instance.default_product_tax:
	    product_tax_class = record.get('tax_class_id')
	    if not product_tax_class:
		return [(6, 0, [])]

	    if instance.nontaxable_tax_class_id and instance.nontaxable_tax_class_id == str(product_tax_class):
		return [(6, 0, [])]

	    return [(6, 0, [instance.default_product_tax.id])]
	else:
	    return [(6, 0, [])]


    def prepare_odoo_record_vals(self, cr, uid, job, record, context=None):
	set_obj = self.pool.get('product.attribute.set')
	base_url = job.mage_instance.url
	media_ext = 'media/catalog/product'
	img_url = base_url + media_ext

        image_path = record.get('thumbnail')
        if not image_path:
            image_path = record.get('small_image')

	if image_path:
	    get_url = img_url + image_path
	else:
	    get_url = False

        vals = {
		'active': True,
		'weight': record.get('weight'),
		'standard_price': record.get('cost'),
		'upc': record.get('upc'),
		'special_price': record.get('special_price'),
		'msrp': record.get('msrp'),
		'manufacturer': record.get('manufacturer'),
		'list_price': record.get('price'),
                'description': record.get('description', ' '),
                'mage_status': record['status'],
#                'name': record['name'],
                'default_code': record['sku'],
                'mage_type': record['type_id'],
                'set': set_obj.get_mage_record(cr, uid, record['attribute_set_id']),
                'super_attributes': [(5)],
                'websites': [(5)],
                'external_id': record['entity_id'],
                'url_key': record.get('url_key', ''),
                'short_description': record.get('short_description', ''),
                'categories': [(5)],
                'type': PRODUCT_TYPES.get(record['type_id']) or 'product',
                'sync_to_mage': True,
        }

	if record.get('weight') and float(record.get('weight')) > 0:
	    vals['weight'] = record.get('weight')

	vals['taxes_id'] = self.apply_taxes(cr, uid, job, record)

        if record.get('categories'):
           categ_ids = self._find_categories(cr, uid, record['categories'])
	   #Copy what someone else did, just apply the first category as primary randomly
	   #To satisfy unpredictable reporting requirement ;)
           if categ_ids:
               vals['categ_id'] = categ_ids[0]

           vals['categories'] = [(6, 0, categ_ids)]


        if record.get('websites'):
            vals['websites'] = self._find_websites(cr, uid, record['websites'])

        if record.get('super_attributes'):
            vals['super_attributes'] = self._find_super_attributes(cr, uid, record['super_attributes'])

        return vals


    def _find_categories(self, cr, uid, categories):
        cat_obj = self.pool.get('product.category')
        category_ids = cat_obj.search(cr, uid, [('external_id', 'in', categories)])
        return category_ids


    def _find_super_attributes(self, cr, uid, super_attributes):
        attribute_obj = self.pool.get('product.attribute')
        attribute_ids = attribute_obj.search(cr, uid, [('external_id', 'in', super_attributes)])
        return [(6, 0, attribute_ids)]


    def _find_websites(self, cr, uid, websites):
        website_obj = self.pool.get('mage.website')
        website_ids = website_obj.search(cr, uid, [('external_id', 'in', websites)])
        return [(6, 0, website_ids)]


    def _find_attribute_values(self, cr, uid, external_attribute_ids):
        attribute_obj = self.pool.get('product.attribute.value')
	external_ids = external_attribute_ids.split(',')
        attribute_ids = attribute_obj.search(cr, uid, [
                ('external_id', 'in', external_ids)
        ])

        return [(6, 0, attribute_ids)]


    def _find_attribute_value(self, cr, uid, external_attribute_id):
        attribute_obj = self.pool.get('product.attribute.value')

        attribute_ids = attribute_obj.search(cr, uid, [
                ('external_id', '=', external_attribute_id)
        ])

        if attribute_ids:
            return attribute_ids[0]

        return False


    def upsert_mage_record(self, cr, uid, vals, record_id=False):
        if record_id:
            self.write(cr, uid, record_id, vals)
            return record_id

        existing_id = self.get_mage_record(cr, uid, vals['external_id'])
        if not existing_id and vals.get('default_code'):
	    existing_id = self.sql_product_search(cr, uid, vals['default_code'])
#	    existing_id = self.search(cr, uid, [('default_code', '=', vals['default_code'])])
        if existing_id:
            self.write(cr, uid, existing_id, vals)
            return existing_id

        else:
            return self.create(cr, uid, vals)


    def sync_one_image(self, cr, uid, job, product_id, record, img_url):
	image_path = record.get('thumbnail')
	if not image_path:
	    image_path = record.get('small_image')

	if not image_path or image_path == 'no_selection':
	    return True

	get_url = img_url + image_path
	(filename, header) = urllib.urlretrieve(get_url)
	with open(filename, 'rb') as f:
	    img = base64.b64encode(f.read())
	    self.write(cr, uid, product_id, {'image': img, 'img_path': get_url})

	return True	
