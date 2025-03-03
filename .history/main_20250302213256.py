from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from executor import execute_python_code
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code: str

@app.post("/execute")
async def execute_code(request: CodeRequest):
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="No code provided")
    
    result = execute_python_code(request.code)
    return result

@app.get("/health")
async def health_check():
    return {"status": "healthy"}