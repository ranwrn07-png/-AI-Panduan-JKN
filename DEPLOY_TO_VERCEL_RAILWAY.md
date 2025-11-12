Panduan Deploy Permanen: Frontend ke Vercel, Backend ke Railway
===============================================================

Ringkasan singkat:
- Frontend (statis) akan dideploy ke Vercel (atau Netlify).
- Backend (FastAPI) akan dideploy ke Railway (atau Render/Fly).
- Domain `jknpintar.com` diarahkan via DNS (A/CNAME) ke provider hosting.

Langkah 1 — Siapkan repo GitHub
1. Commit semua perubahan pada repo lokal.
2. Push ke GitHub (buat repository baru jika perlu):

```powershell
git init
git add .
git commit -m "Prepare for deployment: meta api-base, Procfile, deploy docs"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

Langkah 2 — Deploy Backend ke Railway (cepat)
1. Buat akun di https://railway.app dan login.
2. Pilih "New Project" → "Deploy from GitHub".
3. Hubungkan repository Anda dan pilih folder `backend` (jika repo monorepo pilih path yang tepat) atau setup Dockerfile jika ada.
4. Railway akan mendeteksi `Procfile` dan menjalankan `uvicorn main:app --host 0.0.0.0 --port $PORT`.
5. Di pengaturan project Railway, masuk ke "Variables" dan tambahkan environment variables penting:
   - SECRET_KEY (isi random string)
   - ALGORITHM (HS256)
   - ACCESS_TOKEN_EXPIRE_MINUTES (60)
   - OPENAI_API_KEY (jika pakai)
   - SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS (untuk email)
   - BACKEND_BASE_URL (optional, contoh: https://api.jknpintar.com)
6. Deploy dan catat URL produksi Railway, misal: `https://jknpintar-backend.up.railway.app`.

Langkah 3 — Deploy Frontend ke Vercel
1. Buat akun di https://vercel.com dan login.
2. Pilih "New Project" → Import Git Repository (pilih repo Anda).
3. Untuk project statis, pastikan build command (jika ada) dan output directory sesuai. Jika frontend hanya static files (`index.html` dll), Vercel akan deploy langsung.
4. Penting: set environment variable `API_BASE` (atau edit `frontend/index.html` meta `api-base`) agar menunjuk ke backend Railway yang sudah deploy. Contoh isi meta di `index.html`:
   `<meta name="api-base" content="https://jknpintar-backend.up.railway.app/api">`
   Anda bisa mengedit `index.html` sebelum deploy atau men-set replacement di build step.
5. Deploy dan catat URL Vercel misal: `https://jknpintar.vercel.app`.

Langkah 4 — Hubungkan Domain `jknpintar.com`
1. Di panel domain registrar (tempat beli domain), buka pengaturan DNS.
2. Untuk Vercel: tambah CNAME record `www` → `cname.vercel-dns.com` (ikuti instruksi Vercel), dan A/ALIAS sesuai kebutuhan (Vercel menunjukkan record yang harus ditambahkan).
3. Di dashboard Vercel, buka Settings → Domains → Add domain `jknpintar.com`, lalu ikuti verifikasi DNS.
4. Setelah verifikasi, Vercel akan mengeluarkan sertifikat HTTPS otomatis.

Langkah 5 — Sesuaikan API_BASE dan CORS
1. Jika frontend di `https://jknpintar.com` dan backend di `https://api.jknpintar.com` (atau Railway generated URL), pastikan backend `CORS` mengizinkan origin frontend. Di `main.py`, konfigurasi CORS saat ini `allow_origins=["*"]` — lebih aman diganti menjadi domain frontend.
2. Atur `BACKEND_BASE_URL` di env dan pastikan `index.html` meta `api-base` menunjuk ke `https://<backend-domain>/api`.

Langkah 6 — Submit sitemap ke Google
1. Daftar dan verifikasi situs di Google Search Console.
2. Submit sitemap: `https://jknpintar.com/sitemap.xml`.
3. Minta indexing lewat Search Console.

Catatan keamanan & produksi
- Hapus atau disable `dev_code` fallback untuk endpoint `/api/send_verification` pada environment produksi.
- Pastikan `.env` tidak ter-commit.
- Tambahkan rate-limiting/protection (Cloudflare atau app-level) untuk endpoint verifikasi.

Jika Anda mau, saya bisa:
- Membantu menyiapkan PR ke repo Anda yang mengganti meta `api-base` sesuai backend final.
- Membuat GitHub Actions untuk auto-deploy (opsional).
- Atau melanjutkan proses deploy jika Anda beri akses (GitHub & domain provider) atau menjalankan instruksi sesuai panduan.
