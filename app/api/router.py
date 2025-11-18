from fastapi import APIRouter
from pydantic import BaseModel
from ..crypto import mint_ephemeral_secret, verify_secret

router = APIRouter(prefix="/v1")

class MintRequest(BaseModel):
    purpose: str
    ttl: int | None = None

class MintResponse(BaseModel):
    token: str
    expires: int

class VerifyRequest(BaseModel):
    token: str

class VerifyResponse(BaseModel):
    valid: bool
    data: dict | None = None
    error: str | None = None

@router.post("/mint", response_model=MintResponse)
async def mint(req: MintRequest):
    result = mint_ephemeral_secret(req.purpose, req.ttl)
    return MintResponse(**result)

@router.post("/verify", response_model=VerifyResponse)
async def verify(req: VerifyRequest):
    result = verify_secret(req.token)
    return VerifyResponse(valid=result.get("valid"), data=result.get("data"), error=result.get("error"))
