from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from db import SessionLocal, init_db, User, Document
from auth import get_password_hash, verify_password, create_access_token, decode_token
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import random
from email_utils import send_verification_email
import json
import numpy as np

load_dotenv()

app = FastAPI(title="JKN Pintar - Mediator Service", description="AI Chat Assistant untuk Panduan Aplikasi JKN")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

class RegisterIn(BaseModel):
    email: str
    password: str
    verification_code: Optional[str] = None


class SendCodeIn(BaseModel):
    email: str


class VerifyCodeIn(BaseModel):
    email: str
    code: str

class LoginIn(BaseModel):
    email: str
    password: str

class LoginOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LinkJKNIn(BaseModel):
    jkn_id: str

class ChatIn(BaseModel):
    message: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(request: Request, db=Depends(get_db)):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing auth")
    token = auth.split(" ")[1]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.email == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@app.post("/api/register")
def register(payload: RegisterIn, db=Depends(get_db)):
    # Require a valid verification code before creating account
    if not payload.verification_code:
        raise HTTPException(status_code=400, detail="Verification code is required")
    # find a matching unused code
    now = datetime.utcnow()
    vc = db.query(__import__('db').VerificationCode).filter(
        __import__('db').VerificationCode.email == payload.email,
        __import__('db').VerificationCode.code == payload.verification_code,
        __import__('db').VerificationCode.used == False,
        __import__('db').VerificationCode.expires_at > now
    ).first()
    if not vc:
        raise HTTPException(status_code=400, detail="Invalid or expired verification code")
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=payload.email, hashed_password=get_password_hash(payload.password))
    db.add(user)
    # mark code used
    vc.used = True
    db.add(vc)
    db.commit()
    db.refresh(user)
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@app.post("/api/login")
def login(payload: LoginIn, db=Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


def _generate_code() -> str:
    return str(random.randint(100000, 999999))


@app.post("/api/send_verification")
def send_verification(payload: SendCodeIn, db=Depends(get_db)):
    # create code, store in DB with short expiry and attempt to send via SMTP
    code = _generate_code()
    expires = datetime.utcnow() + timedelta(minutes=10)
    VC = __import__('db').VerificationCode
    vc = VC(email=payload.email, code=code, expires_at=expires, used=False)
    db.add(vc)
    db.commit()
    # try to send email
    sent = send_verification_email(payload.email, code)
    if sent:
        return {"ok": True, "message": "Verification code sent to email"}
    else:
        # in development, return code so developer can complete flow without SMTP
        return {"ok": True, "message": "SMTP not configured or failed; returning code for dev/testing", "dev_code": code}


@app.post("/api/verify_code")
def verify_code(payload: VerifyCodeIn, db=Depends(get_db)):
    now = datetime.utcnow()
    VC = __import__('db').VerificationCode
    vc = db.query(VC).filter(VC.email == payload.email, VC.code == payload.code, VC.used == False, VC.expires_at > now).first()
    if not vc:
        raise HTTPException(status_code=400, detail="Invalid or expired code")
    vc.used = True
    db.add(vc)
    db.commit()
    return {"ok": True, "message": "Code verified"}


@app.post("/api/link-jkn")
def link_jkn(payload: LinkJKNIn, user=Depends(get_current_user), db=Depends(get_db)):
    user.jkn_id = payload.jkn_id
    db.add(user)
    db.commit()
    return {"ok": True, "message": "JKN account linked"}


@app.post("/api/chat")
async def chat(payload: ChatIn, user=Depends(get_current_user), db=Depends(get_db)):
    # Step 1: retrieve top documents (embedding-based if available)
    docs = db.query(Document).all()
    retrieved = []
    # if embeddings available and OPENAI configured, do embed compare
    OPENAI = os.getenv("OPENAI_API_KEY")
    USE_EMB = os.getenv("USE_OPENAI_EMBEDDINGS", "false").lower() == "true"
    query = payload.message
    if USE_EMB and OPENAI:
        try:
            import openai
            openai.api_key = OPENAI
            qemb = openai.Embedding.create(model="text-embedding-3-small", input=query)["data"][0]["embedding"]
            # compute cosine with stored
            sims = []
            for d in docs:
                if not d.embedding_json:
                    continue
                emb = json.loads(d.embedding_json)
                emb = np.array(emb, dtype=float)
                qv = np.array(qemb, dtype=float)
                sim = float(np.dot(emb, qv) / (np.linalg.norm(emb) * np.linalg.norm(qv) + 1e-10))
                sims.append((sim, d))
            sims.sort(key=lambda x: x[0], reverse=True)
            for sim, d in sims[:3]:
                retrieved.append({"title": d.title, "excerpt": d.content[:500], "score": sim})
        except Exception as e:
            # fallback to keyword search
            for d in docs:
                if query.lower() in d.content.lower():
                    retrieved.append({"title": d.title, "excerpt": d.content[:500]})
    else:
        # simple keyword search
        for d in docs:
            if query.lower() in d.content.lower():
                retrieved.append({"title": d.title, "excerpt": d.content[:500]})

    # Step 2: if user linked JKN, fetch claims (mock endpoint)
    user_info = {"linked_jkn": bool(user.jkn_id)}
    jkn_data = None
    if user.jkn_id:
        import requests
        try:
            base = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")
            resp = requests.get(f"{base}/mock/claims_for_user/{user.jkn_id}", timeout=3)
            if resp.ok:
                jkn_data = resp.json()
        except Exception:
            jkn_data = {"ok": False}

    # Step 3: assemble prompt and call OpenAI chat if available
    answer = ""
    sources = retrieved
    if OPENAI:
        try:
            import openai
            openai.api_key = OPENAI
            system = "Anda adalah asisten panduan Aplikasi JKN. Gunakan hanya informasi sumber yang diberikan. Jika diperlukan, gunakan data JKN yang terlinked."
            messages = [{"role": "system", "content": system}, {"role": "user", "content": payload.message}]
            # add retrievals as context
            for r in retrieved:
                messages.append({"role": "system", "content": f"Sumber: {r['title']}\n{r['excerpt']}"})
            if jkn_data:
                messages.append({"role": "system", "content": f"Data JKN untuk user: {json.dumps(jkn_data)}"})
            resp = openai.ChatCompletion.create(model="gpt-4o-mini", messages=messages, max_tokens=512)
            answer = resp["choices"][0]["message"]["content"]
        except Exception as e:
            answer = "(OpenAI error or not configured) Berikut hasil retrieval: \n" + "\n---\n".join([r["excerpt"] for r in retrieved])
    else:
        # fallback canned answer
        if retrieved:
            answer = "Saya menemukan informasi terkait: \n" + "\n---\n".join([f"{r['title']}: {r['excerpt'][:200]}..." for r in retrieved])
        else:
            answer = "Maaf, saya tidak menemukan jawaban di dokumen. Jika akun Anda terlink, saya bisa cek status klaim Anda." 
            if not user.jkn_id:
                answer += " Silakan link akun JKN Anda dulu."

    return {"answer": answer, "sources": sources, "jkn_data": jkn_data}


# Mount mock JKN router
from jkn_mock import router as mock_router
app.include_router(mock_router)

@app.get("/")
async def root():
    return {"ok": True, "message": "JKN Pintar backend running", "version": "1.0.0"}
