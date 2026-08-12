import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from home.google_business import import_reviews_payload, mark_sync_error, sync_google_business_reviews


class Command(BaseCommand):
    help = 'Synchronize Google Business Profile reviews into the local Enigma Dent database.'

    def add_arguments(self, parser):
        parser.add_argument('--from-json', dest='from_json', help='Import a saved Google reviews JSON response for local testing.')

    def handle(self, *args, **options):
        try:
            if options.get('from_json'):
                path = Path(options['from_json'])
                if not path.exists():
                    raise CommandError(f'File not found: {path}')
                payload = json.loads(path.read_text(encoding='utf-8'))
                result = import_reviews_payload(payload)
            else:
                result = sync_google_business_reviews()
        except Exception as exc:
            mark_sync_error(exc)
            raise CommandError(str(exc)) from exc
        self.stdout.write(self.style.SUCCESS(
            f"Google reviews synced: +{result['created']} new, {result['updated']} updated, total={result['total']}"
        ))
