from fastapi import FastAPI

app = FastAPI(title="fastapi-backend-lab")

@app.get("/health")
def health():
    return {"status": "ok"}