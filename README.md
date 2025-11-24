# Mini POS - Sistem Point of Sale

Aplikasi Point of Sale (POS) berbasis web menggunakan Django untuk manajemen toko, inventory, dan penjualan.

## ✨ Fitur Lengkap

- 🔐 **Autentikasi** - Login system dengan role management
- 📦 **Manajemen Produk** - CRUD produk dengan kategori
- 👥 **Manajemen Customer & Supplier** - Database pelanggan dan supplier
- 🚚 **Purchase Order** - Kelola PO dan update stock otomatis
- 🛒 **Transaksi Penjualan** - Sistem order dengan diskon per item
- 📊 **Laporan** - Export PDF & Excel dengan filter periode
- 📈 **Analytics** - Grafik penjualan dengan Chart.js
- 💾 **Backup Database** - Auto daily backup + manual download
- 📥 **Import Excel** - Bulk import produk dari Excel
- 📱 **PWA Ready** - Install sebagai aplikasi Android/iOS
- 🎨 **Responsive** - Optimal di mobile, tablet, dan desktop
- 🇮🇩 **Bahasa Indonesia** - Interface dalam Bahasa Indonesia

## 🚀 Quick Start (Local Development)

### 1. Install Dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Setup Database

```powershell
python manage.py migrate
```

### 3. Buat Superuser

```powershell
python manage.py createsuperuser
```

**Atau gunakan default:**
- Username: `admin`
- Password: `admin123`

```powershell
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123'); print('Superuser created!')"
```

### 4. Seed Data Demo (Opsional)

```powershell
python manage.py seed_data
```

### 5. Jalankan Server

```powershell
python manage.py runserver
```

Buka browser: **http://localhost:8000**

## 🌍 Deploy Online (Production)

### Deploy ke Railway.app (Gratis & Mudah)

1. **Push ke GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/username/mini-pos.git
   git push -u origin main
   ```

2. **Deploy di Railway:**
   - Buka https://railway.app
   - Login dengan GitHub
   - New Project → Deploy from GitHub repo
   - Pilih repository `mini-pos`
   - Tambahkan PostgreSQL database
   - Set environment variables:
     ```
     SECRET_KEY=your-secret-key-here
     DEBUG=False
     ALLOWED_HOSTS=*.railway.app
     ```

3. **Run Migrations:**
   ```bash
   railway run python manage.py migrate
   railway run python manage.py createsuperuser
   ```

4. **Selesai!** Aplikasi online di: `https://mini-pos-production.up.railway.app`

**Panduan lengkap:** Lihat file `DEPLOY_GUIDE.md`

## 📱 Install sebagai Aplikasi Android/iOS

1. Buka aplikasi di Chrome (Android) atau Safari (iOS)
2. Klik banner **"Install Mini POS"** 
3. Atau menu browser → **"Add to Home screen"**
4. Icon aplikasi muncul di home screen! 🎉

**Panduan lengkap:** Lihat file `PWA_GUIDE.md`

## 📖 Halaman & Fitur

### Dashboard
- `/` - Overview metrics & grafik penjualan 7 hari
- `/low-stock/` - Produk dengan stok menipis

### Manajemen
- `/categories/` - CRUD Kategori produk
- `/products/` - CRUD Produk
- `/products/import/` - Import produk dari Excel
- `/customers/` - CRUD Pelanggan
- `/suppliers/` - CRUD Supplier

### Transaksi
- `/purchase-orders/` - Purchase Order & penerimaan barang
- `/orders/` - Daftar pesanan
- `/orders/create/` - Buat pesanan baru (dengan diskon)
- `/orders/<id>/receipt/` - Download struk PDF (thermal 58mm)

### Laporan & Analytics
- `/reports/` - Laporan penjualan (daily/weekly/monthly)
- `/reports/export/pdf/` - Export laporan PDF
- `/reports/export/excel/` - Export laporan Excel
- `/analytics/` - Grafik penjualan (kategori, produk, jam)

### Sistem
- `/backups/` - Backup & download database
- `/login/` - Halaman login
- `/logout/` - Logout
- `/clear-cache/` - Clear PWA cache & service worker

### API Endpoints (Protected)
- `GET /api/products/` - List produk (JSON)
- `POST /api/orders/create/` - Buat order via API

## 🛠️ Tech Stack

- **Backend:** Django 4.2, Django REST Framework
- **Database:** SQLite (dev), PostgreSQL (production)
- **Frontend:** Bootstrap 5, Chart.js, Select2
- **PDF Generation:** ReportLab
- **Excel:** openpyxl (read & write)
- **Authentication:** Django built-in auth
- **Static Files:** WhiteNoise (production)
- **Web Server:** Gunicorn (production)
- **PWA:** Service Worker, Web Manifest

## 📁 Struktur Project

```
mini_pos/
├── pos/                    # Main app
│   ├── models.py          # Category, Product, Customer, Order, etc.
│   ├── views.py           # All business logic
│   ├── forms.py           # Django forms
│   ├── utils.py           # PDF & Excel generators
│   ├── middleware.py      # Daily backup middleware
│   └── management/        # Custom commands
├── templates/             # HTML templates
│   ├── base.html         # Base template with PWA
│   ├── pos/              # App templates
│   └── clear_cache.html  # PWA cache clear page
├── static/               # Static files
│   ├── css/             # Stylesheets
│   ├── icons/           # PWA icons
│   ├── manifest.json    # PWA manifest
│   └── sw.js            # Service worker
├── backup/              # Auto backup location
├── requirements.txt     # Python dependencies
├── Procfile            # Railway/Heroku config
├── runtime.txt         # Python version
├── .gitignore          # Git ignore rules
├── DEPLOY_GUIDE.md     # Deployment guide
├── PWA_GUIDE.md        # PWA installation guide
└── README.md           # This file
```

## 🔒 Security

- CSRF protection enabled
- Login required for all pages (except login)
- API endpoints protected with API key
- SQL injection protected (Django ORM)
- XSS protection enabled

## 💾 Backup System

- **Auto Backup:** Daily automatic backup (first request per day)
- **Manual Backup:** `python manage.py backup_db`
- **Download:** Via `/backups/` page
- **Location:** `backup/db_backup_YYYYMMDD.sqlite3`

## 📊 Reports & Analytics

### Thermal Receipt (58mm)
- Logo toko
- Informasi pesanan
- Detail item dengan diskon
- Total & payment info
- Thermal printer friendly

### PDF Report (A4)
- Header dengan periode
- Summary metrics
- Detail transaksi table
- Footer dengan timestamp

### Excel Export
- Multiple sheets
- Formatted headers
- Auto-width columns
- Summary totals

## 🎨 Customization

### Ubah Logo & Icon
1. Upload icon baru ke `static/icons/`
2. Buka `/clear-cache/` dan klik tombol
3. Refresh browser

### Ubah Warna Theme
Edit `static/css/styles.css`:
```css
:root {
    --accent: #2563eb;  /* Warna utama */
    --bg: #0f1724;      /* Background */
}
```

## 🐛 Troubleshooting

### Icon PWA tidak update?
Buka `/clear-cache/` dan klik tombol "Clear Cache & Reload"

### Static files tidak muncul di production?
```bash
python manage.py collectstatic --noinput
```

### Database migration error?
```bash
python manage.py migrate --run-syncdb
```

## 📝 License

MIT License - Free to use and modify

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📞 Support

Untuk pertanyaan atau bantuan:
- Baca dokumentasi lengkap di folder `/docs`
- Check `DEPLOY_GUIDE.md` untuk deployment
- Check `PWA_GUIDE.md` untuk PWA setup

---

**Dibuat dengan ❤️ menggunakan Django & Python**

Versi: 1.0.0 | Last Update: November 2025
