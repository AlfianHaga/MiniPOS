import random
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Fill missing Product.image_url fields with placeholder images (picsum)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force", action="store_true", help="Overwrite existing image_url values"
        )
        parser.add_argument(
            "--start-seed", type=int, default=1, help="Starting seed for picsum ids"
        )

    def handle(self, *args, **options):
        from pos.models import Product

        force = options["force"]
        seed = options["start_seed"]

        qs = Product.objects.all()
        updated = 0
        i = seed
        for p in qs:
            if p.image_url and not force:
                continue
            p.image_url = f"https://picsum.photos/seed/{i}/320/240"
            p.save(update_fields=["image_url"])
            updated += 1
            i += 1

        self.stdout.write(
            self.style.SUCCESS(f"Updated {updated} products with placeholder images.")
        )
