from i18n.models import InternationalizablePage
from django.core.management.base import BaseCommand, CommandError

import django.apps
import json
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
        staticfiles = os.path.join(os.path.dirname(__file__), '../../static/source')
        os.makedirs(staticfiles)

        for model in django.apps.apps.get_models():
            # We care about models that:
            #   extend the InternationalizablePage models defined by this module
            #   are not proxy models (used by Django Admin for editing)
            is_internationalizable = issubclass(model, InternationalizablePage)
            is_not_proxy = not model._meta.proxy
            if (is_internationalizable and is_not_proxy):
                strings = model.gather_strings()
                outpath = os.path.abspath(os.path.join(staticfiles, model.__name__ + ".json"))
                with open(outpath, 'w') as outfile:
                    json.dump(strings, outfile, indent=4, sort_keys=True)