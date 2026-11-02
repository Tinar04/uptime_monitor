from django.core.management.base import BaseCommand
from monitor.models import Site
from monitor.services import run_check
class Command(BaseCommand):
    def handle(self, *args, **options):
        active_sites = Site.objects.filter(is_active = True)
        checked = 0
        for site in active_sites:
            try:    
                run_check(site)
                checked+=1
            except Exception:
                self.stdout.write(f"Checked {checked} sites")

    






