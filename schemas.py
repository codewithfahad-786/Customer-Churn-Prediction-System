from pydantic import BaseModel

class CustomerData(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MonthlyCharges: float
    TotalCharges: float