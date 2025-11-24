# Deploy Mini POS ke PythonAnywhere

Panduan lengkap deploy aplikasi Django ke PythonAnywhere (100% gratis, tidak perlu kartu kredit).

## 🚀 Langkah-langkah Deploy

### 1. Buat Akun PythonAnywhere

1. Buka https://www.pythonanywhere.com
2. Klik **"Start running Python online in less than a minute!"**
3. Pilih **"Create a Beginner account"** (Free)
4. Isi form registrasi (email, username, password)
5. Verifikasi email

### 2. Upload Code ke PythonAnywhere

**A. Via GitHub (Recommended):**

1. Login ke PythonAnywhere
2. Klik tab **"Consoles"** → **"Bash"**
3. Clone repository:
```bash
git clone https://github.com/AlfianHaga/MiniPOS.git
cd MiniPOS
```

**B. Via Upload Manual:**

1. Zip folder `mini_pos` di komputer
2. Di PythonAnywhere, klik tab **"Files"**
3. Upload zip file
4. Extract via Bash console

### 3. Setup Virtual Environment

Di Bash console:

```bash
cd ~/MiniPOS
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Setup Database

```bash
python manage.py migrate
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: admin123
```

### 5. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 6. Configure Web App

1. Klik tab **"Web"**
2. Klik **"Add a new web app"**
3. Pilih **"Manual configuration"**
4. Pilih **"Python 3.11"**
5. Klik **"Next"**

### 7. Configure WSGI File

1. Di tab **"Web"**, scroll ke **"Code"** section
2. Klik link **"WSGI configuration file"** (misal: `/var/www/username_pythonanywhere_com_wsgi.py`)
3. **Hapus semua isi file**, ganti dengan:

```python
import os
import sys

# Path ke project
path = '/home/USERNAME/MiniPOS'  # Ganti USERNAME dengan username PythonAnywhere Anda
if path not in sys.path:
    sys.path.append(path)

# Path ke virtual environment
os.environ['DJANGO_SETTINGS_MODULE'] = 'mini_pos.settings'

# Activate virtual environment
activate_this = '/home/USERNAME/MiniPOS/venv/bin/activate_this.py'  # Ganti USERNAME
exec(open(activate_this).read(), {'__file__': activate_this})

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**⚠️ Penting:** Ganti `USERNAME` dengan username PythonAnywhere Anda (2 tempat)

4. Klik **"Save"**

### 8. Configure Virtual Environment Path

1. Kembali ke tab **"Web"**
2. Di section **"Virtualenv"**, klik **"Enter path to a virtualenv"**
3. Masukkan path: `/home/USERNAME/MiniPOS/venv` (ganti USERNAME)
4. Klik ✓

### 9. Configure Static Files

Di tab **"Web"**, scroll ke **"Static files"**, klik **"Enter URL"** dan **"Enter path"**:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/USERNAME/MiniPOS/staticfiles` |

(Ganti USERNAME)

### 10. Set Environment Variables (Opsional)

Di Bash console, edit `.bashrc`:

```bash
nano ~/.bashrc
```

Tambahkan di akhir file:

```bash
export SECRET_KEY='django-prod-secret-minipos-pythonanywhere-2024'
export DEBUG='False'
export ALLOWED_HOSTS='USERNAME.pythonanywhere.com'
```

Save (Ctrl+O, Enter, Ctrl+X)

Reload:
```bash
source ~/.bashrc
```

### 11. Reload Web App

1. Kembali ke tab **"Web"**
2. Scroll ke atas
3. Klik tombol **"Reload USERNAME.pythonanywhere.com"** (hijau besar)

### 12. Selesai! 🎉

Aplikasi akan tersedia di:
```
https://USERNAME.pythonanywhere.com
```

(Ganti USERNAME dengan username PythonAnywhere Anda)

---

## 📱 Install PWA dari URL PythonAnywhere

1. Buka URL di Chrome Android
2. Banner **"Install Mini POS"** akan muncul
3. Tap **"Install"**
4. Icon muncul di home screen!

---

## 🔄 Update Aplikasi

Setiap kali ada perubahan di GitHub:

```bash
cd ~/MiniPOS
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Lalu reload web app di tab **"Web"**.

---

## 🐛 Troubleshooting

### Error 500 / Aplikasi tidak jalan?

1. **Cek Error Log:**
   - Tab **"Web"** → **"Log files"** → **"Error log"**
   - Lihat error terakhir

2. **WSGI file salah?**
   - Pastikan path `/home/USERNAME/MiniPOS` benar
   - Pastikan virtual env path benar

3. **Static files tidak muncul?**
   - Pastikan static files mapping benar
   - Run `python manage.py collectstatic --noinput` lagi

4. **Database error?**
   - Run `python manage.py migrate` lagi

### Reload tidak work?

Gunakan Bash console:
```bash
touch /var/www/USERNAME_pythonanywhere_com_wsgi.py
```

---

## 💾 Backup Database

### Export:
```bash
cd ~/MiniPOS
python manage.py dumpdata > backup_$(date +%Y%m%d).json
```

### Import:
```bash
python manage.py loaddata backup_20241124.json
```

### Download ke komputer:

1. Tab **"Files"**
2. Navigate ke `MiniPOS/`
3. Klik file `backup_*.json`
4. Klik **"Download"**

---

## 📊 Monitoring

**Free Tier Limits:**
- ✅ Always online (tidak sleep)
- ✅ 512 MB storage
- ✅ 100k hits/day
- ✅ Python 3.11 support
- ✅ MySQL/PostgreSQL database

**Cukup untuk:**
- 100-200 users/day
- Database sampai 100 MB
- Testing & production kecil-menengah

---

## 🎯 Tips

1. **Domain Custom:**
   - Free tier tidak support custom domain
   - Harus upgrade ke Paid ($5/bulan)

2. **HTTPS:**
   - Sudah otomatis (`.pythonanywhere.com` sudah HTTPS)

3. **Scheduled Tasks:**
   - Free tier bisa 1 scheduled task
   - Bisa untuk backup otomatis

4. **Database:**
   - Free tier dapat MySQL database
   - Untuk production besar, consider PostgreSQL

---

## ✅ Checklist Deploy

- [ ] Akun PythonAnywhere dibuat
- [ ] Code di-clone dari GitHub
- [ ] Virtual environment dibuat
- [ ] Dependencies di-install
- [ ] Database migration done
- [ ] Superuser dibuat
- [ ] Static files collected
- [ ] Web app configured
- [ ] WSGI file edited (USERNAME diganti)
- [ ] Virtual env path set
- [ ] Static files mapping set
- [ ] Web app reloaded
- [ ] Aplikasi bisa diakses
- [ ] Login berhasil dengan admin/admin123

---

**Selamat! Aplikasi Mini POS sudah online dan bisa diakses dari mana saja!** 🚀

Untuk bantuan lebih lanjut, buka dokumentasi PythonAnywhere: https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/
