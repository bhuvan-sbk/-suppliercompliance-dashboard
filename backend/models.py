from sqlalchemy import Column, Float, Integer, String, JSON, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base  

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    country = Column(String)
    contract_terms = Column(JSON)
    compliance_score = Column(Integer)
    last_audit = Column(Date)

class ComplianceRecord(Base):
    __tablename__ = "compliance_records"
    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    metric = Column(String)
    date_recorded = Column(Date)
    result = Column(Float)
    status = Column(String)