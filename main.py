from fastapi import FastAPI

app = FastAPI(title="Firm Inteligence API")

@app.get("/health")
def health():
    return {"status":"ok"}


