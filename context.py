from pydantic import BaseModel
from typing import Optional, List, Dict

class UserSessionContext(BaseModel):
    name: str = "Anonymous"
    uid: int = 0
    goal: Optional[dict] = None
    user_profile: Optional[str] = None
    diet_preferences: Optional[str] = None
    workout_plan: Optional[List[str]] = None
    meal_plan: Optional[List[str]] = None
    injury_notes: Optional[str] = None
    handoff_logs: List[str] = []
    progress_logs: List[Dict[str, str]] = []

