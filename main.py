from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from executor import execute_python_code
from fastapi.middleware.cors import CORSMiddleware
import uuid

app = FastAPI()

# In-memory storage for code and results (temporary, resets on restart)
code_store = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    # Generate a unique ID and store the code + result
    code_id = str(uuid.uuid4())
    code_store[code_id] = {"code": request.code, "result": result}
    return {"id": code_id, "result": result}

@app.get("/code/{code_id}")
async def get_code(code_id: str):
    if code_id not in code_store:
        raise HTTPException(status_code=404, detail="Code not found")
    return code_store[code_id]

@app.get("/health")
async def health_check():
    return {"status": "healthy"}