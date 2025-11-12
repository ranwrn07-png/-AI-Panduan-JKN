# JKN Pintar - Panduan Deployment ke Web Publik

## 🎯 Apa yang Sudah Selesai

✅ **Rebranding**: Semua referensi berubah dari "AI Panduan JKN" → "JKN Pintar"
✅ **UI Responsive**: Mobile (< 480px), Tablet (480-1024px), Desktop (> 1024px)  
✅ **SEO Ready**: Meta tags, manifest.json, robots.txt, sitemap.xml
✅ **Backend API**: FastAPI, JWT auth, mock JKN connector
✅ **Frontend**: Modern UI dengan gradient, touch-friendly buttons
✅ **Dokumentasi**: Panduan hosting, testing, deployment

## 🚀 Langkah Deploy ke Web Publik (jknpintar.com atau custom domain)

### Pilihan A: SETUP CEPAT (Railway + Vercel) - RECOMMENDED

#### Step 1: Registrasi Domain (10 menit)
1. Kunjungi: niagahoster.com atau namecheap.com
2. Search domain: `jknpintar.com` (atau pilihan Anda)
3. Beli domain (Rp 50k-150k / tahun, usually around Rp 120k)
4. Catat NS (nameserver) atau DNS settings

#### Step 2: Setup Backend di Railway (20 menit)

1. Buka: https://railway.app
2. Sign up dengan GitHub
3. New Project → GitHub Repo → select `AI-Panduan-JKN` folder
4. Railway auto-detect Python project
5. Tunggu build (5-10 menit)
6. Di Railway dashboard, copy URL backend (contoh: `jknpintar-backend.railway.app`)
7. Domain tab → tambahkan custom domain `api.jknpintar.com`
   - Atau biarkan Railway auto-assign, catat URLnya

#### Step 3: Setup Frontend di Vercel (15 menit)

1. Buka: https://vercel.com
2. Sign up dengan GitHub
3. Import project → select repo → select `frontend` folder
4. Vercel auto-deploy
5. Domain tab → tambahkan custom domain `jknpintar.com`
6. Vercel akan generate CNAME records untuk DNS

#### Step 4: Update API_BASE di Frontend (5 menit)

Edit file: `frontend/app.js` baris 1

```javascript
// GANTI INI:
const API_BASE = "http://localhost:8000/api";

// MENJADI INI:
const API_BASE = "https://api.jknpintar.com/api";
// atau (jika Railway auto-assigned):
const API_BASE = "https://jknpintar-backend.railway.app/api";
```

Save & push ke GitHub:
```bash
git add frontend/app.js
git commit -m "Update API_BASE untuk production"
git push origin main
```

Vercel auto-redeploy.

#### Step 5: Update Domain DNS (5-30 menit, tunggu propagasi)

Registrar domain (Niagahoster/Namecheap) → Dashboard → DNS

**Untuk Railway backend:**
```
Name: api
Type: CNAME
Value: <railway-url>
TTL: 3600
```

**Untuk Vercel frontend:**
```
Name: @
Type: CNAME
Value: cname.vercel-dns.com
TTL: 3600
```

(Vercel akan memberikan exact CNAME di dashboard)

**Alternative: NS Records**
- Jika menggunakan Railway/Vercel NS, update NS registrar ke yang diberikan platform.

#### Step 6: Setup HTTPS & SSL (automatic)

Railway & Vercel memberikan SSL free (Let's Encrypt).
Tunggu ~5 menit setelah DNS propagate.

#### Step 7: Test

```
https://jknpintar.com
https://api.jknpintar.com (endpoint backend)
```

Buka di browser dan test:
- Register akun
- Login
- Link JKN ID
- Chat dengan AI

---

### Pilihan B: SETUP dengan VPS (Jika ingin kontrol penuh)

Gunakan DigitalOcean / Linode / Vultr:

1. Rent Droplet (ubuntu-20.04, 1GB RAM, ~$5/bulan)
2. SSH ke server
3. Clone repo
4. Install Docker
5. Setup Let's Encrypt SSL (certbot)
6. Run docker-compose:
   ```bash
   docker-compose up --build -d
   ```
7. Update DNS ke VPS IP
8. Akses https://jknpintar.com

(Lihat PUBLIC_HOSTING.md untuk detail)

---

## 📋 Env Variables yang Harus di-Set di Production

Di Railway/Vercel/VPS, set ini di environment:

```
SECRET_KEY=<generate-random-32-char-string>
OPENAI_API_KEY=<optional-jika-pakai-openai>
USE_OPENAI_EMBEDDINGS=false
```

Generate SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_hex(16))"
# Output: xxxxxxxxxxxxxxxx (copy ke SECRET_KEY)
```

---

## ✅ Pre-Launch Checklist

- [ ] Domain registered (jknpintar.com)
- [ ] Railway backend running & URL copied
- [ ] Vercel frontend running & custom domain added
- [ ] API_BASE updated in frontend/app.js
- [ ] GitHub push completed
- [ ] DNS records created (CNAME)
- [ ] DNS propagated (test dengan nslookup atau online tool)
- [ ] SSL certificate active (https working)
- [ ] Test dari mobile browser
- [ ] Test dari desktop browser
- [ ] Test dari tablet
- [ ] Register @ Google Search Console
- [ ] Submit sitemap.xml to Google

---

## 🎉 SELESAI!

Setelah langkah di atas, JKN Pintar sudah live di `jknpintar.com` dan dapat diakses dari:
- ✅ PC (Windows, Mac, Linux)
- ✅ Android (via Chrome)
- ✅ iPhone (via Safari)
- ✅ Tablet (via browser apapun)

---

## 💡 Troubleshooting

**Frontend tidak bisa call backend API?**
- Cek CORS di `backend/main.py`, pastikan domain frontend di-allow
- Cek API_BASE di `frontend/app.js`
- Buka DevTools → Console, lihat error

**Domain tidak resolve?**
- Tunggu DNS propagation (5 menit - 24 jam)
- Test: `nslookup jknpintar.com`

**HTTPS tidak bekerja?**
- Railway/Vercel auto-generate cert, tunggu 5 menit setelah DNS

**Database error?**
- Railway/Vercel menggunakan SQLite lokal (jkn_ai.db)
- Untuk production besar, upgrade ke PostgreSQL

---

## 📚 Dokumentasi Lanjutan

- **PUBLIC_HOSTING.md** — Panduan teknis lengkap
- **DEPLOY.md** — Deployment detail
- **README.md** — Project overview
- **TESTING.md** — Local testing guide

---

## 🎬 QUICK START (No Reading Version)

```bash
# 1. Register domain (niagahoster.com)
# 2. Push code to GitHub
# 3. Railway: Sign up → Import GitHub repo → Done
# 4. Vercel: Sign up → Import GitHub repo (frontend folder) → Done
# 5. Update frontend/app.js API_BASE
# 6. Update registrar DNS ke Railway & Vercel CNAME
# 7. Wait DNS propagate
# 8. Test jknpintar.com
# Done! 🎉
```

**Estimasi waktu total: 2-3 jam (including DNS wait)**  
**Estimasi biaya: Rp 120k/tahun (domain) + free hosting**

---

Jika ada pertanyaan saat deployment, check PUBLIC_HOSTING.md atau contact support platform yang Anda gunakan (Railway/Vercel).

Good luck! 🚀
