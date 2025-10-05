from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas
from ..deps import get_current_user
from ..ai.embeddings import embed_texts
import numpy as np
import re

router = APIRouter(prefix="/matcher", tags=["matcher"])

CORE_SKILL_REGEX = r"\b([A-Za-z][A-Za-z\+\#\.]*)\b"

def _extract_keywords(text: str) -> set:
    # Very light heuristic: tokens >1 char, drop common stopwords
    stop = {"and","or","with","the","a","an","to","for","of","in","on","at","by","be","is","are","as","we"}
    words = {w.lower() for w in re.findall(CORE_SKILL_REGEX, text)}
    return {w for w in words if len(w) > 1 and w not in stop}

@router.post("/score/{app_id}", response_model=schemas.MatchOut)
async def score_resume(app_id: int, payload: schemas.MatchRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    app = db.query(models.Application).filter(models.Application.id == app_id, models.Application.user_id == user.id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    resume_text = payload.resume_text.strip()
    jd_text = payload.jd_text.strip()
    if len(resume_text) < 20 or len(jd_text) < 20:
        raise HTTPException(status_code=400, detail="Provide sufficient text for resume and JD")

    vecs = await embed_texts([resume_text, jd_text])
    a, b = np.array(vecs[0]), np.array(vecs[1])
    # Cosine similarity on already normalized vectors (from provider) -> dot product in [-1,1]
    cosine = float(np.clip(a @ b, -1.0, 1.0))
    score = round((cosine + 1) * 50, 2) # map [-1,1] → [0,100]

    r_keys = _extract_keywords(resume_text)
    j_keys = _extract_keywords(jd_text)
    present = sorted(list(r_keys & j_keys))
    missing = sorted(list(j_keys - r_keys))

    match = models.Match(application_id=app.id, score=score,
    skills_present=",".join(present),
    skills_missing=",".join(missing))
    # store snapshots for traceability
    app.resume_text = resume_text
    app.jd_text = jd_text

    db.add(match)
    db.commit()
    db.refresh(match)

    return {
    "id": match.id,
    "score": match.score,
    "skills_present": present,
    "skills_missing": missing,
    "created_at": match.created_at,
    }