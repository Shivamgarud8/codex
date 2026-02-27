from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class Project(BaseModel):
    title: str
    description: str
    tools: List[str] = Field(default_factory=list)
    link: Optional[str] = None


class Certification(BaseModel):
    name: str
    issuer: Optional[str] = None
    verification_link: Optional[str] = None


class CandidateProfile(BaseModel):
    full_name: str
    email: str
    phone: str
    city: str
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None
    medium: Optional[str] = None
    role_preference: Optional[str] = None
    skills_matrix: Dict[str, List[str]] = Field(default_factory=dict)
    projects: List[Project] = Field(default_factory=list)
    certifications: List[Certification] = Field(default_factory=list)


class ResumeGenerationRequest(BaseModel):
    job_description: str
    company: str
    city_override: Optional[str] = None
    candidate: CandidateProfile


class JDInsights(BaseModel):
    role: str
    primary_skills: List[str]
    secondary_skills: List[str]
    ats_keywords: List[str]
    tools_priority: List[str]


class ResumeOutput(BaseModel):
    filename: str
    insights: JDInsights
    selected_skills: Dict[str, List[str]]
    optimized_project_bullets: List[str]
    latex_sections: Dict[str, str]


class AnalyzeRequest(BaseModel):
    job_description: str


class AnalyzeResponse(BaseModel):
    insights: JDInsights
