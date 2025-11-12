# JKN Pintar - Panduan Hosting Publik & SEO

Dokumen ini berisi panduan lengkap untuk deploy JKN Pintar sebagai website publik dengan domain custom dan optimasi SEO.

## 1. Registrasi Domain

Pilih registrar domain dan daftarkan domain untuk JKN Pintar:

**Opsi domain:**
- `jknpintar.com` (domain utama - ideal)
- `jkn-pintar.id` (domain Indonesia - juga bagus)
- `asistenjkn.com`
- Atau domain lain pilihan Anda

**Registrar populer:**
- Niagahoster.com (Indonesia, support lokal)
- Namecheap.com (internasional, murah)
- Godaddy.com (populer, support bagus)

Biaya: Rp 50k - 150k / tahun (tergantung registrar & ekstensi).

## 2. Hosting Platform (Rekomendasi)

Pilih salah satu platform managed untuk kemudahan:

### A) Railway.app (Recommended - simple & affordable)
- Free tier: cukup untuk MVP (monthly credit $5)
- Pro tier: mulai $5/bulan
- Setup cepat (push kode ke GitHub, auto-deploy)
- Support database, environment vars, custom domain

**Langkah:**
1. Sign up di railway.app
2. Hubungkan GitHub repo (push code ke repo)
3. Railway auto-detect `requirements.txt` dan deploy backend
4. Setup environment vars: `SECRET_KEY`, `OPENAI_API_KEY` (opsional)
5. Custom domain: di Railway dashboard, link ke domain Anda
6. Frontend bisa di-host terpisah di Netlify/Vercel

### B) Vercel.com (Frontend + Serverless API)
- Free tier: cukup baik
- Auto-deploy dari GitHub
- Edge network global (fast loading)
- Custom domain free (untuk .vercel.com atau domain Anda)

**Langkah:**
1. Push frontend folder ke GitHub
2. Sign up Vercel, import repo
3. Vercel auto-deploy
4. Config domain custom di Vercel dashboard
5. Backend bisa di Railway/Render

### C) Render.com (Backend + Frontend)
- Free tier: available
- Good for both backend & frontend
- Simple deployment

### D) VPS Tradisional (Jika ingin kontrol penuh)
- Lihat bagian "VPS Setup" di bawah

## 3. Setup Backend di Railway/Render

### Railway:
```yaml
# Ceritakan ke Railway:
# 1. Pastikan Anda punya Procfile atau Railway mendeteksi automatic:
# Procfile (di root project):
web: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

Atau biarkan Railway auto-detect dari `requirements.txt`.

Env vars di Railway dashboard:
```
SECRET_KEY=<generate-random-key>
OPENAI_API_KEY=<your-openai-key-if-needed>
USE_OPENAI_EMBEDDINGS=false
```

### Render:
- Connect GitHub repo
- Render auto-detect `requirements.txt`
- Set start command: `uvicorn backend.main:app --host 0.0.0.0`
- Add env vars same as above

## 4. Setup Frontend

### Vercel (recommended for frontend):
1. Create `vercel.json` in frontend folder:
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "index.html",
         "use": "@vercel/static"
       }
     ],
     "routes": [
       {
         "src": "/(.+)",
         "dest": "/index.html"
       }
     ]
   }
   ```
2. Push frontend folder to GitHub
3. Import to Vercel, auto-deploy
4. Link custom domain in Vercel dashboard

### Netlify:
1. Drag-drop `frontend` folder, or connect GitHub
2. Site settings → custom domain
3. Connect to your DNS

## 5. Connect Frontend to Backend API

Update `frontend/app.js` dengan backend URL production:

```javascript
// BEFORE (local):
const API_BASE = "http://localhost:8000/api";

// AFTER (production, ganti dengan domain Anda):
const API_BASE = "https://api.jknpintar.com/api";
// atau
const API_BASE = "https://jknpintar-backend.railway.app/api";
```

Pastikan backend di Railway/Render sudah expose public URL.

## 6. SSL Certificate

- Railway/Render/Vercel: **automatic HTTPS** (free)
- Jika VPS: gunakan Let's Encrypt (certbot) - **free**

## 7. Domain DNS Setup

Setelah mendaftar domain di registrar, config DNS pointing ke hosting:

### Jika Railway/Render:
- Registrar → DNS settings
- Add CNAME record:
  ```
  Host: @ (atau www)
  Type: CNAME
  Value: <railway-app-url> atau <render-url>
  ```

### Jika Vercel:
- Vercel dashboard auto-generate NS records
- Update di registrar domain

Tunggu propagasi DNS (5 menit - 24 jam).

## 8. SEO Optimization

### Metadata (sudah ditambahkan di `frontend/index.html`):
```html
<meta name="description" content="JKN Pintar - Asisten AI untuk panduan Aplikasi JKN" />
<meta name="keywords" content="JKN, BPJS, Kesehatan, AI Chat" />
<meta property="og:title" content="JKN Pintar - Asisten AI" />
```

### Tambahkan robots.txt:
Buat `frontend/robots.txt`:
```
User-agent: *
Allow: /
Sitemap: https://jknpintar.com/sitemap.xml
```

### Tambahkan sitemap.xml:
Buat `frontend/sitemap.xml`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://jknpintar.com</loc>
    <priority>1.0</priority>
  </url>
</urlset>
```

### Google Search Console:
1. Daftar di https://search.google.com/search-console
2. Verify ownership (upload sitemap.xml via GSC)
3. Monitor indexing status

### Meta Tags Tambahan (di `<head>`):
```html
<meta name="google-site-verification" content="..." />
<meta name="theme-color" content="#0b63d6">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<link rel="manifest" href="/manifest.json">
```

## 9. Progressive Web App (PWA) - Opsional

Buat `frontend/manifest.json`:
```json
{
  "name": "JKN Pintar",
  "short_name": "JKN Pintar",
  "description": "Asisten AI untuk panduan Aplikasi JKN",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#0b63d6",
  "icons": [
    {
      "src": "/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

Buat `frontend/service-worker.js` untuk offline support (optional).

## 10. CORS Configuration (Important)

Backend harus allow frontend domain. Update `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://jknpintar.com", "https://www.jknpintar.com", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 11. Environment Variables (Production)

Jangan expose API keys di frontend. Backend harus handle:
- `SECRET_KEY`: random 32+ chars
- `OPENAI_API_KEY`: (opsional) dari OpenAI
- `DATABASE_URL`: (jika Postgres) connection string

## 12. Monitoring & Logs

- Railway/Render: Dashboard logs built-in
- Setup error tracking: Sentry.io (free tier available)

## 13. Checklist Deploy Production

- [ ] Domain registered & DNS configured
- [ ] SSL certificate active
- [ ] Backend environment vars set
- [ ] Frontend API_BASE updated to production URL
- [ ] CORS origins configured
- [ ] Robots.txt & sitemap.xml added
- [ ] Google Search Console verified
- [ ] Database backed up
- [ ] Rate limiting & security headers added
- [ ] Tested dari mobile/desktop/tablet

## 14. Quick Start Commands

```bash
# Clone repo
git clone <repo-url>
cd jkn-pintar

# Push ke GitHub (jika belum)
git add .
git commit -m "JKN Pintar - update branding & responsive"
git push origin main

# Railway deploy:
# - Connect GitHub repo di railway.app
# - Set env vars
# - Auto-deploy

# Vercel deploy (frontend):
# - Connect GitHub repo di vercel.com
# - Select frontend folder
# - Auto-deploy
```

## Support & Questions

- Railway docs: https://docs.railway.app
- Vercel docs: https://vercel.com/docs
- Next step: contact hosting support atau dev team

---

**Estimasi biaya (per bulan):**
- Railway backend: $0-5 (free tier generous)
- Vercel frontend: $0 (free tier)
- Domain: ~Rp 10k/bulan (tahunan Rp 120k)
- **Total: ~Rp 10-60k/bulan (tergantung traffic)**

Jika traffic tinggi, scale up di Railway/Vercel (bayar sesuai usage).
