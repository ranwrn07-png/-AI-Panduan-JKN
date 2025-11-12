# Testing Web Chat - Panduan Lokal

Selamat! Backend dan frontend chat sudah berjalan lokal. Berikut adalah panduan untuk test fitur-fitur utama:

## Status Server
- Backend (API): http://localhost:8000
- Frontend (Chat UI): http://localhost:8080
- Database: `backend/jkn_ai.db` (SQLite)

## Test Skenario

### 1. Daftar Akun Baru
1) Buka http://localhost:8080 di browser.
2) Di bagian kiri, isi form "Daftar":
   - Email: contoh@test.com
   - Password: password123
3) Klik "Daftar & Masuk".
4) Harapan: User berhasil terdaftar dan JWT token diterima. Form berubah ke "Link Akun JKN" dan "Mulai Chat".

### 2. Login
1) Jika belum login, isi form "Login":
   - Email: contoh@test.com
   - Password: password123
2) Klik "Login".
3) Harapan: Token diterima, UI berubah.

### 3. Link Akun JKN (Mock)
1) Setelah login, di form "Link Akun JKN (mock)", isi:
   - JKN ID: 12345
2) Klik "Link Akun".
3) Harapan: Pesan "Linked!" muncul. Akun JKN sudah terlinked.

### 4. Chat dengan AI
1) Di bagian "Mulai Chat", isi textarea dengan pertanyaan, contoh:
   - "Bagaimana cara registrasi di JKN?"
   - "Apa itu rujukan?"
   - "Status klaimku?"
2) Klik "Kirim".
3) Harapan:
   - Jika pertanyaan cocok dokumen panduan yang ada (`docs/panduan_penggunaan.txt`), AI akan retrieve excerpt dan menjawab.
   - Jika akun sudah terlink JKN, AI akan coba query mock endpoint `/mock/claims_for_user/{jkn_id}` dan sertakan data klaim dalam jawaban.
   - Jawaban muncul di chat box sebelah kanan.

## Catatan untuk Testing

- **Dokumen Panduan**: Saat ini hanya ada 1 file dummy `docs/panduan_penggunaan.txt`. Untuk result yang lebih baik, tambahkan lebih banyak file `.txt` di folder `docs/` dan jalankan:
  ```powershell
  cd backend
  .\.venv\Scripts\Activate.ps1
  python ingest.py
  ```

- **OpenAI Integration** (opsional): Jika ingin gunakan OpenAI untuk LLM responses:
  1. Buat file `backend/.env` dengan isi:
     ```
     SECRET_KEY=your-secret-key
     OPENAI_API_KEY=sk-...
     USE_OPENAI_EMBEDDINGS=true
     ```
  2. Jalankan `python ingest.py` di backend folder untuk mengindeks dokumen dengan embeddings.
  3. Restart backend server (Ctrl+C di terminal, jalankan ulang `uvicorn main:app --reload`).
  4. Chat akan menggunakan OpenAI ChatCompletion API untuk menjawab dengan lebih natural.

- **Database Reset**: Jika ingin reset data user & dokumen, hapus file `backend/jkn_ai.db` dan jalankan `python db.py` lagi.

- **Mock JKN API**: Endpoint `/mock/claims_for_user/{jkn_id}` hanya mengembalikan data dummy:
  - JKN ID 12345 → claim status "Approved"
  - JKN ID 67890 → claim status "Pending"
  - Untuk production, ganti dengan API JKN resmi.

## Akses untuk Development

Jika server perlu dikonfigurasi atau ada issue:

### Backend logs
- Terminal di mana backend berjalan menunjukkan uvicorn logs dan error dari FastAPI.

### Frontend DevTools
- Buka DevTools (F12) → Console untuk melihat error dari JavaScript (app.js).
- Cek Network tab untuk memastikan request ke backend (http://localhost:8000/api/...) berhasil.

### Database Query (direct)
- Gunakan SQLite client atau command line:
  ```powershell
  cd backend
  sqlite3 jkn_ai.db
  SELECT * FROM users;  -- lihat user yang terdaftar
  SELECT * FROM documents;  -- lihat dokumen terindeks
  ```

## Next Steps

Setelah testing lokal berhasil:
1. Tambahkan lebih banyak dokumen panduan JKN ke folder `docs/`.
2. Integrasikan dengan API resmi JKN (ganti `jkn_mock.py` dengan connector sebenarnya).
3. Aktifkan OpenAI untuk RAG yang lebih baik.
4. Deploy ke hosting (VPS, Docker, atau platform managed seperti Railway/Render).
5. Integrasikan WebView ke aplikasi mobile JKN.

Jika ada pertanyaan atau error, lihat DEPLOY.md atau hubungi support development.
