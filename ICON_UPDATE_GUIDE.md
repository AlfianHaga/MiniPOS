# 🔄 Cara Memperbarui Icon & Cache PWA

Icon sudah diupload tapi tidak berubah? Ikuti langkah berikut:

## Cara 1: Automatic (Paling Mudah) ✨

1. **Buka halaman Clear Cache:**
   ```
   http://localhost:8000/clear-cache/
   ```

2. **Klik tombol "Clear Cache & Reload"**

3. **Tunggu proses selesai** (otomatis reload)

4. **Icon baru akan muncul!** 🎉

---

## Cara 2: Manual di Browser 🔧

### Chrome / Edge Desktop:

1. Tekan **F12** (Developer Tools)
2. Tab **Application**
3. Di sidebar kiri:
   - **Service Workers** → Klik "Unregister"
   - **Cache Storage** → Klik kanan → "Delete"
   - **Local Storage** → Klik kanan → "Clear"
4. Klik kanan di halaman → **Hard Reload** (Ctrl + Shift + R)

### Chrome Android:

1. Buka **Settings** → **Apps** → **Chrome**
2. Tap **Storage & cache**
3. Tap **Clear cache** dan **Clear storage**
4. Buka aplikasi lagi

### Jika sudah di-install sebagai PWA:

**Android:**
1. Long press icon Mini POS di home screen
2. Tap **"App info"**
3. Tap **"Storage"** → **"Clear cache"** dan **"Clear data"**
4. Atau uninstall dan install ulang

**Desktop:**
1. Buka Chrome → **chrome://apps**
2. Klik kanan "Mini POS" → **"Remove from Chrome"**
3. Buka website lagi → Install ulang

---

## Cara 3: Force Update Service Worker 🚀

Edit file `static/sw.js`:
```javascript
// Ubah version number
const CACHE_NAME = 'mini-pos-v3';  // dari v2 ke v3
```

Lalu reload halaman dengan **Ctrl + Shift + R**

---

## Troubleshooting 🔍

### Icon masih tidak berubah?

1. **Cek file ada:**
   ```
   static/icons/
   ├── icon-192x192.png  ← Penting untuk Android
   ├── icon-512x512.png  ← Penting untuk Android
   ├── favicon.svg       ← Tab browser
   └── apple-touch-icon.png  ← iOS
   ```

2. **Cek ukuran file:**
   - Icon tidak boleh terlalu kecil (minimal 10KB)
   - Format: PNG (recommended) atau SVG

3. **Restart server Django:**
   ```bash
   # Tekan Ctrl+C di terminal
   python manage.py runserver
   ```

4. **Test di Incognito/Private mode:**
   - Buka browser private
   - Akses http://localhost:8000
   - Icon baru harus muncul

---

## Quick Command 🎯

Untuk clear semua sekaligus, buka browser Console (F12) dan paste:

```javascript
// Clear everything
(async () => {
  // Unregister service workers
  const regs = await navigator.serviceWorker.getRegistrations();
  for (let reg of regs) await reg.unregister();
  
  // Delete all caches
  const keys = await caches.keys();
  for (let key of keys) await caches.delete(key);
  
  // Clear storage
  localStorage.clear();
  sessionStorage.clear();
  
  console.log('✅ Cache cleared! Reloading...');
  location.reload(true);
})();
```

---

## Verifikasi Icon Berhasil ✅

1. **Tab browser** → Icon baru di tab
2. **Bookmark** → Icon baru saat save bookmark
3. **PWA Install** → Icon baru di prompt install
4. **Home screen** → Icon baru setelah install (Android/iOS)

---

**Sudah coba semua cara tapi masih gagal?**

Kemungkinan file icon corrupt atau format salah. Upload ulang icon dengan:
- Format: PNG
- Ukuran: 512x512 px
- Background: Tidak transparan (atau solid color)
- File size: < 500KB

Atau generate ulang di: https://realfavicongenerator.net/
