from main import *
class tags(db.Model):
	__tablename__ = 'tags'
	id = db.Column(db.Integer,primary_key=True)
	tag_name = db.Column(db.Text)
class tagmap(db.Model):
	__tablename__ = 'tagmap'
	id = db.Column(db.Integer,primary_key=True)
	tag_id = db.Column(db.Integer)
	api_id = db.Column(db.Integer)
class api_providers(db.Model):
	__tablename__ = 'api_providers'
	id = db.Column(db.Integer,primary_key=True)
	date = db.Column(db.Text)
	api_provider_name = db.Column(db.Text)
	email = db.Column(db.Text)
	owner_key = db.Column(db.Text)
class api_endpoints(db.Model):
	__tablename__ = 'api_endpoints'
	id = db.Column(db.Integer,primary_key=True)
	date = db.Column(db.Text)
	api_name = db.Column(db.Text)
	api_url = db.Column(db.Text)
	owner_key = db.Column(db.Text)
	category = db.Column(db.Text)
	api_provider_id = db.Column(db.Integer, db.ForeignKey('api_providers.id'))
	api_provider = db.relationship("api_providers", backref=db.backref('api_endpoints', order_by=id))
class api_authent_info(db.Model):
	__tablename__ = 'api_authent_info'
	id = db.Column(db.Integer,primary_key=True)
	date = db.Column(db.Text)
	info_json = db.Column(db.Text)
	api_endpoint_id = db.Column(db.Integer, db.ForeignKey('api_endpoints.id'))
	api_endpoint = db.relationship("api_endpoints", backref=db.backref('api_authent_info', order_by=id))
class api_authent_terms(db.Model):
	__tablename__ = 'api_authent_terms'
	id = db.Column(db.Integer,primary_key=True)
	date = db.Column(db.Text)
	owner_key = db.Column(db.Text)
	authent_json = db.Column(db.Text)
	api_endpoint_id = db.Column(db.Integer, db.ForeignKey('api_endpoints.id'))
	api_endpoint = db.relationship("api_endpoints", backref=db.backref('api_authent_terms', order_by=id))