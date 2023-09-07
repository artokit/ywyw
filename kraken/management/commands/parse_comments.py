from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'not help'

    def handle(self, *args, **options):
        executor.Executor(dp).start_polling()