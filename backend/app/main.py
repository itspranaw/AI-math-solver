# backend/app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sympy as sp
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI-Powered Math Solver API")

# Configure CORS
origins = [
    "http://localhost:3000",  # React's default port
    # Add other origins if necessary
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow requests from React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EquationRequest(BaseModel):
    equation: str

class EquationResponse(BaseModel):
    solution: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI-Powered Math Solver API"}

@app.post("/solve", response_model=EquationResponse)
def solve_equation(request: EquationRequest):
    equation = request.equation
    try:
        # If equation includes '=', split and rearrange
        if '=' in equation:
            lhs, rhs = equation.split('=')
            expr = sp.Eq(sp.sympify(lhs), sp.sympify(rhs))
            # Assuming solving for x
            solution = sp.solve(expr, sp.symbols('x'))
        else:
            # If no '=', assume expression equals zero
            expr = sp.sympify(equation)
            solution = sp.solve(expr)
        return EquationResponse(solution=str(solution))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
