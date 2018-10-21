from django.core.management.base import BaseCommand

import world.load


class Command(BaseCommand):
    help = 'Loads world data into the database.'

    def handle(self, *args, **options):
        world.load.run()
