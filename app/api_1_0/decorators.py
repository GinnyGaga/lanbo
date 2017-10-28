from functools import wraps
from flask import g
from .errors import forbidden

def permission_required(permisson):
	def decorator(f):
		@wraps(f)
		def decorated_function(*args,**kwargs):
			if not g.curent_user.can(permisson):
				return forbidden('Insufficient permissions')
			return f(*args,**kwargs)
		return decorated_function
	return decorator
