from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date
from typing import Optional
import google.generativeai as genai
import os
from dotenv import load_dotenv
from models import Base, Supplier, ComplianceRecord
from database import engine, SessionLocal
import logging
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# Set Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Gemini API key is missing! Please set GEMINI_API_KEY in the .env file.")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Create FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow requests from your React frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models for request bodies
class SupplierCreate(BaseModel):
    name: str
    country: str
    contract_terms: Optional[dict] = None
    compliance_score: Optional[int] = None
    last_audit: Optional[date] = None

class ComplianceData(BaseModel):
    supplier_id: int
    metric: str
    result: float
    date_recorded: date

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Supplier Compliance Monitor & Insights Dashboard!"}

# Endpoint to add a new supplier
@app.post("/suppliers")
def add_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    db_supplier = Supplier(**supplier.dict())
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

# Endpoint to get all suppliers
@app.get("/suppliers")
def get_suppliers(db: Session = Depends(get_db)):
    suppliers = db.query(Supplier).all()
    return suppliers

# Endpoint to get a single supplier by ID
@app.get("/suppliers/{supplier_id}")
def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

# Function to analyze compliance data using Gemini
async def analyze_compliance_data(metric: str, result: float):
    try:
        analysis_prompt = f"""
        Analyze this supplier compliance data:
        Metric: {metric}
        Result: {result}
        
        Provide insights and recommendations in the following JSON format:
        {{
            "status": "analyzed",
            "risk_level": "low/medium/high",
            "insights": ["insight 1", "insight 2"],
            "recommendations": ["recommendation 1", "recommendation 2"]
        }}
        """
        
        response = model.generate_content(analysis_prompt)
        return response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")

# Endpoint to upload and analyze compliance data
@app.post("/suppliers/check-compliance")
async def check_compliance(compliance_data: ComplianceData, db: Session = Depends(get_db)):
    try:
        # Check if supplier exists
        supplier = db.query(Supplier).filter(Supplier.id == compliance_data.supplier_id).first()
        if not supplier:
            raise HTTPException(status_code=404, detail="Supplier not found")

        # Save compliance record to the database
        compliance_record = ComplianceRecord(
            supplier_id=compliance_data.supplier_id,
            metric=compliance_data.metric,
            result=compliance_data.result,
            date_recorded=compliance_data.date_recorded,
            status="Pending Analysis"
        )
        db.add(compliance_record)
        db.commit()
        db.refresh(compliance_record)

        # Analyze compliance data using Gemini
        insights = await analyze_compliance_data(compliance_data.metric, compliance_data.result)

        # Update compliance record with insights
        compliance_record.status = "Analyzed"
        compliance_record.insights = insights
        db.commit()

        return {"message": "Compliance data analyzed", "insights": insights}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to fetch insights for a supplier
@app.get("/suppliers/insights/{supplier_id}")
async def get_insights(supplier_id: int, db: Session = Depends(get_db)):
    try:
        # Fetch supplier and compliance records
        supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
        if not supplier:
            raise HTTPException(status_code=404, detail="Supplier not found")

        compliance_records = db.query(ComplianceRecord).filter(ComplianceRecord.supplier_id == supplier_id).all()
        if not compliance_records:
            return {"supplier_id": supplier_id, "insights": "No compliance records found for this supplier."}

        # Prepare data for Gemini analysis
        compliance_data = [
            f"Metric: {record.metric}, Result: {record.result}, Date: {record.date_recorded}"
            for record in compliance_records
        ]
        compliance_summary = "\n".join(compliance_data)

        # Generate insights using Gemini
        insights_prompt = f"""
        Analyze this supplier's compliance history and provide insights in JSON format:
        
        Supplier: {supplier.name}
        Country: {supplier.country}
        Compliance History:
        {compliance_summary}
        
        Provide analysis in the following JSON format:
        {{
            "overall_assessment": "brief overall assessment",
            "key_insights": ["insight 1", "insight 2"],
            "recommendations": ["recommendation 1", "recommendation 2"],
            "risk_factors": ["risk 1", "risk 2"],
            "suggested_actions": ["action 1", "action 2"]
        }}
        """

        response = model.generate_content(insights_prompt)
        insights = response.text

        return {
            "supplier_id": supplier_id,
            "supplier_name": supplier.name,
            "insights": insights
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))