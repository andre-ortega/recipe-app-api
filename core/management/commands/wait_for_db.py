import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """ Django command to pause exectuion util database is available """
    def handle(self, *args, **options):
        self.stdout.write('Waiting for database..')
        db_conn = None
        while not db_conn:
            try:
                # try to set db_conn to that active connection
                db_conn = connections['default']
            except OperationalError:
                # notify user of waiting and wait
                self.stdout.write('Database unavailable, waiting 1 second')
                # Won't take time during tests because it is being mocked
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
