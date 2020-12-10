from django.apps import AppConfig
# from django.db.models.signals import post_save
#
# from .models import Parent
# from .signals import create_boxes


class SolverConfig(AppConfig):
    name = 'solver'

    def ready(self):
        from . import signals
        # create_boxes.connect(self, self.get_model('BoxValue'), self.get_model('Parent'))
