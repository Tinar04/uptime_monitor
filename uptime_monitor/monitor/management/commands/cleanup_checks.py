from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from monitor.models import Check
class Command(BaseCommand):
    def handle(self, *args, **options):
        cutoff = timezone.now() -timedelta(days=30)
        old_checks = Check.objects.filter(checked_at__lt=cutoff)
        old_checks_count = old_checks.count()
        old_checks.delete()
        self.stdout.write(f"deleted {old_checks_count} old checks")