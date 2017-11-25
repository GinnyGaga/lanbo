from functools import wraps
from flask import g
from .errors import forbidden

<<<<<<< HEAD

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user.can(permission):
                return forbidden('Insufficient permissions')
            return f(*args, **kwargs)
        return decorated_function
    return decorator
=======
def permission_required(permission):
	def decorator(f):
		@wraps(f)
		def decorated_function(*args,**kwargs):
			if not g.current_user.can(permission):
				return forbidden('Insufficient permissions')
			return f(*args,**kwargs)
		return decorated_function
	return decorator
>>>>>>> 17-app-1
