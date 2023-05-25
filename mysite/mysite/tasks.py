# # This will make sure the app is always imported when
# # Django starts so that shared_task will use this app.
from .celery import app as mysite

__all__ = ('mysite',)