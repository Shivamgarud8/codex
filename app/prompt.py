SYSTEM_PROMPT = """You are an ATS optimization expert and resume architect.
Return strict JSON only.
"""


def build_resume_prompt(job_description: str, candidate_payload: dict) -> str:
    return f"""
Analyze the uploaded Job Description and extract:
1. Job role
2. Primary and secondary skills
3. ATS keywords
4. Tools and technologies priority

Using the candidate's structured profile data (skills matrix, projects, certifications, links):
- Select only relevant skills
- Rewrite project descriptions to match the JD
- Prioritize ATS keywords naturally
- Exclude irrelevant technologies
- Optimize for a clean, ATS-friendly LaTeX resume

Output JSON with these keys exactly:
{{
  "insights": {{
    "role": "...",
    "primary_skills": ["..."],
    "secondary_skills": ["..."],
    "ats_keywords": ["..."],
    "tools_priority": ["..."]
  }},
  "selected_skills": {{"Category": ["..."]}},
  "optimized_project_bullets": ["..."],
  "latex_sections": {{
    "summary": "...",
    "skills": "...",
    "projects": "...",
    "certifications": "..."
  }}
}}

Job description:
{job_description}

Candidate profile JSON:
{candidate_payload}
""".strip()
