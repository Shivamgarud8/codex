from __future__ import annotations

import json
import os
from typing import Dict, List

from app.logic import heuristic_insights_dict, select_skills_from_matrix
from app.models import CandidateProfile, JDInsights
from app.prompt import SYSTEM_PROMPT, build_resume_prompt


def heuristic_insights(job_description: str) -> JDInsights:
    return JDInsights(**heuristic_insights_dict(job_description))


def select_skills_from_profile(profile: CandidateProfile, keywords: List[str]) -> Dict[str, List[str]]:
    return select_skills_from_matrix(profile.skills_matrix, keywords)


def call_llm_resume(job_description: str, candidate: CandidateProfile) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")

    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    prompt = build_resume_prompt(job_description, candidate.model_dump())
    resp = client.chat.completions.create(
        model=model,
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    content = resp.choices[0].message.content or "{}"
    return json.loads(content)
