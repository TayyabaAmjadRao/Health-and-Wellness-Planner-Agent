from pydantic import BaseModel, validator
from typing import Optional, List

class GoalInput(BaseModel):
    quantity: float
    metric: str  # e.g., "kg", "lbs", "cm"
    duration: str  # e.g., "2 months"
    goal_type: str  # e.g., "lose", "gain", "maintain"
    
    @validator('metric')
    def validate_metric(cls, v):
        valid_metrics = ['kg', 'lbs', 'cm', 'inches']
        if v not in valid_metrics:
            raise ValueError(f"Metric must be one of {valid_metrics}")
        return v

class DietaryInput(BaseModel):
    preference: str
    restrictions: Optional[List[str]] = None
    allergies: Optional[List[str]] = None