# JKN Pintar - Asisten AI untuk Panduan Aplikasi JKN (Bahasa Indonesia)

Ini adalah prototype web chat AI untuk panduan penggunaan Aplikasi JKN. **JKN Pintar** adalah layanan terpisah (mediator) yang bisa di-deploy sebagai web app dan di-embed ke aplikasi JKN lewat WebView atau deep link. Platform ini responsive, bisa diakses dari PC, smartphone (Android/iOS), dan tablet.

Komponen:
- backend: FastAPI (auth, chat endpoint, JKN mock, ingest)
- frontend: minimal HTML/CSS/JS chat UI

Cara menjalankan (Windows PowerShell):

1) Masuk ke folder backend dan buat virtualenv:

```powershell
cd "c:\Users\LENOVO\OneDrive\Documents\AI Panduan Penggunaan Aplikasi JKN\AI-Panduan-JKN\backend"
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) Copy `.env.example` ke `.env` dan isi `SECRET_KEY` dan (opsional) `OPENAI_API_KEY` jika ingin memanfaatkan embedding/OpenAI.

3) (Opsional) letakkan dokumen panduan sebagai TXT di folder `docs` (buat folder `..\\docs` di root project dan masukkan .txt files), lalu jalankan:

```powershell
python ingest.py
```

4) Jalankan backend:

```powershell
uvicorn main:app --reload
```

5) Buka frontend:
- buka file `frontend/index.html` di browser (atau serve static files via simple http server)

Catatan:
- Untuk integrasi production, gantikan `jkn_mock` dengan connector resmi Aplikasi JKN.
- Pastikan environment variabel dan kebijakan privasi/consent terpenuhi sebelum mengirim data pengguna ke LLM.

Next steps:
- Ganti mock JKN dengan API official
- Tambah vector DB (pgvector) bila skala dokumen besar
- Tambah UI/UX polish dan unit tests
