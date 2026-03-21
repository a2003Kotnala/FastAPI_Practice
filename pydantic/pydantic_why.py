import asyncio
from pydantic import BaseModel, ValidationError, Field,AnyUrl,EmailStr,field_validator,model_validator,computed_field
from typing import Optional, List, Dict, Annotated

class Patient(BaseModel):
    name: str = Field(..., description="The name of the patient") 
    age: int = Field(..., description="The age of the patient", ge = 0)
    email: EmailStr
    linkedin_url: Annotated[Optional[AnyUrl],Field(None, description="The LinkedIn profile URL of the patient")]
    contact: Dict[str,str] = Field(..., description="Contact information of the patient")
    address: Optional[str] = Field(None, description="The address of the patient")


    @field_validator('age')
    @classmethod
    def validate_age(cls,value):
        if value < 0:
            raise ValueError("Age must be a non-negative integer")
        return value

    @model_validator(mode="before")
    @classmethod
    def validate_patient_info(cls, values):
        if "name" not in values or "age" not in values or "email" not in values or "contact" not in values:
            raise ValueError("Missing required fields: name, age, email, and contact are required")
        return values


    @computed_field
    @property
    def is_adult(self) -> bool:
        return self.age >= 18



def insert_patient(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(type(patient.name))    
    print(type(patient.age))
    print(patient.is_adult)
    print(patient.validate_age(patient.age))
    print(patient.is_adult)

    print("Inserted the data")

try:
    Patient_info = {"name" : "Ankit Kotnala", "age": "22", "email": "ankit.kotnala@example.com", "linkedin_url": "https://www.linkedin.com/in/ankit-kotnala/", "contact": {"phone": "123-456-7890"}, "address": "123 Main St, Anytown, USA"}
    patient = Patient(**Patient_info)
    insert_patient(patient)
except ValidationError as e:
    print("Validation error:", e)


    