# Simple mock for JKN API — in production replace with real API connector
from fastapi import APIRouter

router = APIRouter()

# Mock data store
MOCK_CLAIMS = {
    "12345": {"claim_id": "12345", "status": "Approved", "date": "2025-10-01", "facility": "RS Contoh"},
    "67890": {"claim_id": "67890", "status": "Pending", "date": "2025-11-01", "facility": "Puskesmas Demo"}
}

@router.get("/mock/claim/{claim_id}")
async def get_claim(claim_id: str):
    item = MOCK_CLAIMS.get(claim_id)
    if item:
        return {"ok": True, "data": item}
    return {"ok": False, "error": "not_found"}

@router.get("/mock/claims_for_user/{jkn_id}")
async def get_claims_for_user(jkn_id: str):
    # return all claims that have claim_id ending with last 1 digit matching jkn_id for demo
    results = [v for k, v in MOCK_CLAIMS.items() if k.endswith(str(jkn_id)[-1:])]
    return {"ok": True, "data": results}
