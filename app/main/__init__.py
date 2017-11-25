from flask import Blueprint

<<<<<<< HEAD
main = Blueprint('main', __name__)

from . import views, errors
from ..models import Permission


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
=======
main=Blueprint('main',__name__)

from . import views,errors
from ..models import Permission
@main.app_context_processor
def inject_permissions():
	return dict(Permission=Permission)
>>>>>>> 17-app-1
