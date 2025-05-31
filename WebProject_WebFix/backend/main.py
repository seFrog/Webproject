# 1. 패키지 설치
!pip install fastapi pyngrok uvicorn nest-asyncio kiwipiepy requests -q

!pip install fastapi sqlmodel transformers torch pyngrok uvicorn -q

# 2. 임포트 및 초기화
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Session, create_engine, select
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
from datetime import datetime
import nest_asyncio
from pyngrok import ngrok
import uvicorn
from contextlib import asynccontextmanager
from sqlalchemy import inspect

# 3. 데이터베이스 모델 정의
class CorrectionBase(SQLModel):
    original: str = Field(index=True)
    corrected: str

class Correction(CorrectionBase, table=True):
    __table_args__ = {'extend_existing': True}
    id: int | None = Field(default=None, primary_key=True)

class FeedbackBase(SQLModel):
    original: str
    system: str
    user: str
    timestamp: str

class Feedback(FeedbackBase, table=True):
    __table_args__ = {'extend_existing': True}
    id: int | None = Field(default=None, primary_key=True)

# 4. 데이터베이스 엔진 설정
sqlite_url = "sqlite:///database.db"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def get_session():
    with Session(engine) as session:
        yield session

# 5. AI 모델 초기화 
MODEL_NAME = "j5ng/et5-typos-corrector"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, legacy=False)  # ✅ legacy=False 추가
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

# 6. FastAPI 앱 설정 
@asynccontextmanager
async def lifespan(app: FastAPI):
    inspector = inspect(engine)
    if not inspector.has_table("correction"):
        SQLModel.metadata.create_all(engine)
    if not inspector.has_table("feedback"):
        SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 7. API 엔드포인트 (변경 없음)
class CorrectionRequest(BaseModel):
    text: str

@app.post("/correct")
async def correct_text(
    request: CorrectionRequest,
    session: Session = Depends(get_session)
):
    existing = session.exec(
        select(Correction)
        .where(Correction.original == request.text)
    ).first()

    if existing:
        return {
            "original": existing.original,
            "corrected": existing.corrected,
            "source": "database"
        }

    inputs = tokenizer(
        request.text,
        return_tensors="pt",
        padding=True,
        max_length=128,
        truncation=True
    ).to(device)
    
    outputs = model.generate(
        inputs.input_ids,
        attention_mask=inputs.attention_mask,
        max_length=128,
        num_beams=7,
        early_stopping=True
    )
    
    corrected_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    correction = Correction(
        original=request.text,
        corrected=corrected_text
    )
    session.add(correction)
    session.commit()
    session.refresh(correction)

    return {
        "original": request.text,
        "corrected": corrected_text,
        "source": "AI model"
    }

@app.post("/api/feedback")
async def submit_feedback(
    request: Request,
    session: Session = Depends(get_session)
):
    data = await request.json()
    
    feedback = Feedback(
        original=data.get("original"),
        system=data.get("system"),
        user=data.get("user"),
        timestamp=datetime.now().isoformat()
    )
    session.add(feedback)
    
    existing = session.exec(
        select(Correction)
        .where(Correction.original == data.get("original"))
    ).first()

    if existing:
        existing.corrected = data.get("user")
    else:
        session.add(Correction(
            original=data.get("original"),
            corrected=data.get("user")
        ))
    
    session.commit()
    return {"status": "success"}

# 8. 서버 실행
NGROK_AUTH_TOKEN = "dlrjqhstkfkaqkqh"  # 본인 토큰으로 변경하세요
ngrok.set_auth_token(NGROK_AUTH_TOKEN)
tunnel = ngrok.connect(8000)
print(f"🌟 공개 접속 URL: {tunnel.public_url}")

nest_asyncio.apply()
uvicorn.run(app, host="0.0.0.0", port=8000)
