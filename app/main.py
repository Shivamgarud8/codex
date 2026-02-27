from __future__ import annotations

from fastapi import FastAPI

from app.llm import call_llm_resume, heuristic_insights, select_skills_from_profile
from app.models import AnalyzeRequest, AnalyzeResponse, ResumeGenerationRequest, ResumeOutput

app = FastAPI(title="Smart ATS Resume Generator", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/analyze-jd", response_model=AnalyzeResponse)
def analyze_jd(request: AnalyzeRequest) -> AnalyzeResponse:
    return AnalyzeResponse(insights=heuristic_insights(request.job_description))


@app.post("/generate-resume", response_model=ResumeOutput)
def generate_resume(request: ResumeGenerationRequest) -> ResumeOutput:
    llm_payload = call_llm_resume(request.job_description, request.candidate)
    insights = heuristic_insights(request.job_description)

    selected = llm_payload.get("selected_skills") or select_skills_from_profile(
        request.candidate, insights.ats_keywords
    )
    project_bullets = llm_payload.get("optimized_project_bullets") or [
        f"{p.title}: {p.description}" for p in request.candidate.projects[:4]
    ]
    latex_sections = llm_payload.get("latex_sections") or {
        "summary": f"{request.candidate.full_name} - {insights.role}",
        "skills": "\\n".join(f"{k}: {', '.join(v)}" for k, v in selected.items()),
        "projects": "\\n".join(project_bullets),
        "certifications": "\\n".join(c.name for c in request.candidate.certifications),
    }

    city = request.city_override or request.candidate.city
    filename = (
        f"{request.candidate.full_name}_{request.company}_{insights.role}_{city}"
        .replace(" ", "_")
        .replace("/", "-")
    )

    return ResumeOutput(
        filename=filename,
        insights=insights,
        selected_skills=selected,
        optimized_project_bullets=project_bullets,
        latex_sections=latex_sections,
    )
