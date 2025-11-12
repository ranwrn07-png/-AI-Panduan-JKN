Panduan Deploy & Integrasi WebView (Bahasa Indonesia)

File ini berisi instruksi lengkap untuk men-deploy prototype web chat dan contoh cara menambahkan tombol/WebView di aplikasi JKN.

1) Prasyarat
- Docker & Docker Compose (opsional, untuk deploy cepat)
- Server/VPS atau platform hosting static (Netlify, Vercel) jika ingin hosting frontend
- (Opsional) OpenAI API key bila ingin mengaktifkan integrasi LLM


2) Deploy cepat menggunakan Docker Compose (staging)
- Pastikan Anda berada di folder root proyek (folder yang berisi `docker-compose.yml`).

Perintah menjalankan (PowerShell):

```powershell
# di folder root proyek
docker-compose up --build -d
```

Service yang dijalankan:
- Backend (FastAPI) pada port 8000
- Frontend static (nginx) pada port 8080

Catatan: atur environment di `docker-compose.yml` untuk `SECRET_KEY`, `OPENAI_API_KEY`, `USE_OPENAI_EMBEDDINGS`.


3) Hosting frontend saja (opsi cepat)
- Jika hanya ingin men-deploy frontend static, gunakan Netlify atau Vercel:
  - Upload folder `frontend/` ke repo GitHub, lalu deploy di Netlify/Vercel sebagai static site.
  - Backend tetap dijalankan di server terpisah atau platform managed.


4) Mengamankan komunikasi antara aplikasi JKN & chat service
- Gunakan HTTPS di frontend dan backend
- Untuk menghindari login ulang: tim aplikasi JKN dapat membuat endpoint yang menghasilkan one-time token (HMAC) untuk user, kemudian memanggil `https://chat.example.com/?token=...`. Backend chat harus memverifikasi token yang masuk dan menukar dengan session JWT.


5) Contoh WebView minimal (Android & iOS)
- Android (Kotlin)
```kotlin
// Activity
webView.settings.javaScriptEnabled = true
// Jika backend memerlukan header Authorization, pertimbangkan metode server-to-server untuk membuat token singkat
webView.loadUrl("https://chat.example.com")
```

- iOS (Swift)
```swift
let webView = WKWebView(frame: view.bounds)
view.addSubview(webView)
let url = URL(string: "https://chat.example.com")!
webView.load(URLRequest(url: url))
```

6) Contoh flow one-time token (high-level)
- Aplikasi JKN membuat request ke server JKN: POST /generate-chat-token { user_id }
- Server JKN menghasilkan token singkat (HMAC dengan expiry, mis. 120 detik) dan mengembalikan URL: `https://chat.example.com/?token=...`
- Aplikasi JKN membuka WebView ke URL tersebut. Backend chat memverifikasi token, menukar dengan JWT sesi, dan user dianggap terautentikasi.


7) Monitoring & Logs
- Aktifkan logs di backend (uvicorn/fastapi logging).
- Simpan access logs dan event audit untuk panggilan data JKN.


8) Checklist security sebelum produksi
- Pastikan persetujuan pengguna (consent) saat akses data klaim
- Redaksi PII sebelum mengirim ke LLM
- Rotasi API keys & amankan secrets
- Review kebijakan hukum dengan pihak JKN


9) Jika Anda ingin saya jalankan deploy lokal sekarang
- Saya bisa menjalankan `docker-compose up --build -d` pada terminal (butuh izin Anda untuk menjalankan). Bila Anda ingin saya jalankan, balas: "Jalankan sekarang".


Jika butuh saya buat contoh script server-side (contoh generate one-time token) atau bantu deploy ke layanan tertentu (contoh DigitalOcean, Railway, Render), beri tahu hosting yang Anda pilih dan saya akan bantu menyiapkan langkahnya.
