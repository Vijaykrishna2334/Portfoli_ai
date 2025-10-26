# schema.py

from pydantic import BaseModel, Field
from typing import List

class WorkExperience(BaseModel):
    title: str = Field(description="The user's job title at this company.")
    company: str = Field(description="The name of the company.")
    years: str = Field(description="The start and end date/year range (e.g., '2020 - 2023').")
    summary: str = Field(description="A 2-3 sentence summary of responsibilities and achievements.")

class ResumeProfile(BaseModel):
    name: str = Field(description="The user's full name.")
    email: str = Field(description="The user's professional email address.")
    summary: str = Field(description="A concise, professional 3-sentence summary of the user's career goals and experience.")
    skills: List[str] = Field(description="A list of 8 to 12 key hard skills (e.g., Python, SQL, React).")
    experience: List[WorkExperience] = Field(description="A list of all work experiences.")

class OptimizationReport(BaseModel):
    match_score: int = Field(description="A confidence score from 0 to 100...")
    keyword_gaps: List[str] = Field(description="A list of 3-5 critical skills...")
    suggestions: List[str] = Field(description="A list of 3 actionable, specific suggestions...")

class InterviewSettings(BaseModel):
    role: str = Field(description="The target job role...")
    type: str = Field(description="The type of questions...")
    status: str = Field(default="ready", description="The current status...")
    history: List[str] = Field(default=[], description="List of all turns...")