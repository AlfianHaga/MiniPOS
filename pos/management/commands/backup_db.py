import os
import shutil
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Create a timestamped backup of the SQLite database in backup/ directory"

    def add_arguments(self, parser):
        parser.add_argument(
            "--overwrite",
            action="store_true",
            help="Overwrite existing backup for today if present",
        )

    def handle(self, *args, **options):
        db_conf = settings.DATABASES.get("default", {})
        db_path = db_conf.get("NAME")
        if not db_path:
            self.stderr.write("Database path not found in settings.")
            return
        # Handle Path object or string
        if hasattr(db_path, "resolve"):
            db_path = db_path.resolve()
        else:
            db_path = settings.BASE_DIR / db_path
        if not str(db_path).endswith(".sqlite3"):
            self.stderr.write("This command currently supports only SQLite databases.")
            return
        backup_dir = settings.BASE_DIR / "backup"
        os.makedirs(backup_dir, exist_ok=True)
        today = datetime.now().strftime("%Y%m%d")
        backup_file = backup_dir / f"db_backup_{today}.sqlite3"
        if backup_file.exists() and not options.get("overwrite"):
            self.stdout.write(f"Backup for today already exists: {backup_file.name}")
            return
        shutil.copy2(db_path, backup_file)
        self.stdout.write(f"Database backed up to {backup_file}")
