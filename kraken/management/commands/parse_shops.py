from django.core.management import BaseCommand
from ywyw.kraken.df import parse_shop

class Command(BaseCommand):
    help = 'not help'

    def handle(self, *args, **options):
        executor.Executor(dp).start_polling()