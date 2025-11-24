# Mini POS - Deploy ke Railway.app

Panduan lengkap deploy aplikasi Django Mini POS ke Railway.app (gratis).

## 🚀 Persiapan

File yang sudah disiapkan:
- ✅ `requirements.txt` - Dependencies Python
- ✅ `Procfile` - Perintah start server
- ✅ `runtime.txt` - Versi Python
- ✅ `settings.py` - Konfigurasi production-ready

## 📋 Langkah Deploy

### 1. Buat Akun Railway

1. Buka https://railway.app/
2. Klik **"Start a New Project"**
3. Login dengan GitHub (gratis)

### 2. Install Railway CLI (Opsional)

```bash
# Windows (PowerShell)
iwr https://railway.app/install.ps1 | iex

# Atau langsung via web dashboard
```

### 3. Deploy via GitHub (Recommended)

**A. Push ke GitHub:**

```bash
# Inisialisasi git (jika belum)
git init
git add .
git commit -m "Initial commit - Mini POS"

# Buat repository baru di GitHub
# Lalu push:
git remote add origin https://github.com/username/mini-pos.git
git branch -M main
git push -u origin main
```

**B. Connect ke Railway:**

1. Di Railway dashboard → **"New Project"**
2. Pilih **"Deploy from GitHub repo"**
3. Pilih repository `mini-pos`
4. Railway akan auto-detect Django dan deploy!

### 4. Tambahkan Database PostgreSQL

1. Di Railway project → Klik **"New"** → **"Database"** → **"PostgreSQL"**
2. Database otomatis ter-connect ke app
3. Environment variable `DATABASE_URL` otomatis tersedia

### 5. Set Environment Variables

Di Railway project → **Settings** → **Variables**, tambahkan:

```env
SECRET_KEY=your-super-secret-key-change-this-12345
DEBUG=False
ALLOWED_HOSTS=*.railway.app
```

**Generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Run Migrations

Di Railway → **Deployments** → Pilih latest deployment → **"View Logs"**

Atau via CLI:
```bash
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

### 7. Collect Static Files

Railway akan otomatis run:
```bash
python manage.py collectstatic --noinput
```

Jika perlu manual, run via Railway console.

## ✅ Deploy Selesai!

Aplikasi akan tersedia di:
```
https://mini-pos-production.up.railway.app
```

URL akan diberikan setelah deploy selesai.

## 🔐 Buat Superuser

```bash
# Via Railway CLI
railway run python manage.py createsuperuser

# Atau via Railway dashboard → Service → "Shell"
python manage.py createsuperuser
```

## 📱 Install PWA di Android

1. Buka URL Railway di Chrome Android
2. Banner "Install Mini POS" akan muncul
3. Tap **"Install"**
4. Icon muncul di home screen! 🎉

## 🔧 Update Aplikasi

Setiap kali push ke GitHub, Railway otomatis deploy ulang:

```bash
git add .
git commit -m "Update fitur X"
git push
```

Railway akan auto-deploy dalam ~2 menit.

## 💾 Backup Database

### Automatic via Railway:

1. Railway → Project → Database → **"Backups"**
2. Enable automatic backups

### Manual Export:

```bash
# Export database
railway run python manage.py dumpdata > backup.json

# Import database
railway run python manage.py loaddata backup.json
```

## 🌐 Custom Domain (Opsional)

1. Railway → Project → **"Settings"** → **"Domains"**
2. Tambahkan custom domain (misal: `pos.tokoku.com`)
3. Update DNS di domain registrar
4. Update `ALLOWED_HOSTS` di Railway variables

## 💰 Biaya

**Railway Free Tier:**
- ✅ $5 credit per bulan (gratis)
- ✅ Cukup untuk 500+ jam/bulan
- ✅ PostgreSQL gratis
- ✅ Auto-sleep setelah 30 menit idle (otomatis wake up saat diakses)

**Untuk produksi serius:** Upgrade ke Hobby ($5/bulan) - no sleep.

## 🐛 Troubleshooting

### Deploy gagal?

Cek logs di Railway dashboard → **"Deployments"** → **"View Logs"**

### Static files tidak muncul?

```bash
railway run python manage.py collectstatic --noinput
```

### Database migration error?

```bash
railway run python manage.py migrate --run-syncdb
```

### App tidak bisa diakses?

Cek `ALLOWED_HOSTS` di environment variables sudah include `*.railway.app`

## 📊 Monitoring

Railway dashboard menampilkan:
- CPU usage
- Memory usage
- Request metrics
- Deployment history
- Logs real-time

## 🚀 Alternatif Deploy Lainnya

### 1. **Render** (Gratis)
- https://render.com
- PostgreSQL gratis
- Auto-deploy dari GitHub
- Free tier: Sleep setelah 15 menit idle

### 2. **PythonAnywhere** (Gratis 500MB)
- https://www.pythonanywhere.com
- Upload manual via web interface
- MySQL gratis
- Always on (tidak sleep)

### 3. **Heroku** (Tidak gratis lagi)
- Sekarang berbayar minimum $5/bulan

### 4. **Vercel** (Untuk frontend)
- Gratis unlimited
- Tapi butuh serverless setup

## 📖 Rekomendasi

Untuk Mini POS: **Railway.app** adalah pilihan terbaik karena:
- ✅ Setup paling mudah
- ✅ PostgreSQL gratis
- ✅ Auto-deploy dari GitHub
- ✅ $5 credit gratis per bulan
- ✅ Support Django out of the box

---

## 🎯 Quick Deploy Command

Jika sudah ada Railway CLI:

```bash
# Login
railway login

# Link project
railway link

# Deploy
railway up

# Run migrations
railway run python manage.py migrate

# Create superuser
railway run python manage.py createsuperuser
```

Selesai! Aplikasi online dalam 5 menit! 🚀

---

**Butuh bantuan?** Railway punya Discord community yang sangat helpful.
