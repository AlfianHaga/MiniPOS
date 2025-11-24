import os
import shutil
from datetime import datetime
from django.conf import settings


class DailyBackupMiddleware:
    """Lazy daily SQLite backup.

    On first request each day, copy the primary SQLite database file into
    BASE_DIR/backup/db_backup_YYYYMMDD.sqlite3.
    Silent failures (production-grade system should log errors).
    Only triggers for SQLite backend.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.backup_dir = settings.BASE_DIR / "backup"

    def __call__(self, request):
        try:
            self._ensure_daily_backup()
        except Exception:
            # In development we ignore backup errors to avoid breaking requests
            pass
        return self.get_response(request)

    def _ensure_daily_backup(self):
        db_conf = settings.DATABASES.get("default", {})
        db_path = db_conf.get("NAME")
        if not db_path:
            return
        # Handle Path object
        if hasattr(db_path, "resolve"):
            db_path = db_path.resolve()
        else:
            db_path = settings.BASE_DIR / db_path
        if not str(db_path).endswith(".sqlite3"):
            return
        os.makedirs(self.backup_dir, exist_ok=True)
        today = datetime.now().strftime("%Y%m%d")
        backup_file = self.backup_dir / f"db_backup_{today}.sqlite3"
        if backup_file.exists():
            return  # already backed up today
        shutil.copy2(db_path, backup_file)
