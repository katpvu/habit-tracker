from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from app.models.habit_cycle import CycleTypes, CycleStatuses

# =============== REQUEST MODELS ===============

class HabitUpdate(BaseModel):
  name: Optional[str] = None
  # Add more here if Habit model grows and more fields are edittable.

class HabitAdd(BaseModel):
  habit_cycle_id: int
  name: str

class CycleCreate(BaseModel):
  name: str
  cycle_type: CycleTypes

class CycleUpdate(BaseModel):
  name: Optional[str] = None
  cycle_type: CycleTypes
  

# =============== RESPONSE MODELS ===============

class HabitResponse(BaseModel):
  model_config = ConfigDict(from_attributes=True)
  id: int
  habit_cycle_id: int
  name: str
  created_at: datetime
  updated_at: datetime

class CycleResponse(BaseModel):
  model_config = ConfigDict(from_attributes=True)
  id: int
  user_id: int
  name: str
  cycle_type: CycleTypes
  status: CycleStatuses
  created_at: datetime
  updated_at: datetime
  started_at: Optional[datetime]
  completed_at: Optional[datetime]
  habits: List[HabitResponse]

class CycleListResponse(BaseModel):
  model_config = ConfigDict(from_attributes=True)
  id: int
  user_id: int
  name: str
  cycle_type: CycleTypes
  status: CycleStatuses
  created_at: datetime
  started_at: Optional[datetime]
  completed_at: Optional[datetime]