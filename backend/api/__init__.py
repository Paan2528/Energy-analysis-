from fastapi import FastAPI
app = FastAPI()

# ภายในไฟล์ backend/api.py (หรือไฟล์ที่ประกาศตัวแปร app)


@app.get("/health")
def health_check():
    return {"status": "ok"}
