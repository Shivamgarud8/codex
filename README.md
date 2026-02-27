# Smart ATS Resume Generator (MVP)

FastAPI backend for a JD-to-resume engine that:
- analyzes Job Descriptions,
- prioritizes ATS keywords,
- selects role-relevant skills/projects,
- returns resume-ready LaTeX section content.

## Why this exists
This MVP is built for role-specific resume generation for DevOps/Cloud candidates, where a single generic resume often fails ATS filters.

## API endpoints
- `GET /health` — health check.
- `POST /analyze-jd` — heuristic JD analysis.
- `POST /generate-resume` — LLM-driven resume payload generation (with fallback logic).

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Environment variables
- `OPENAI_API_KEY` (required for `/generate-resume`)
- `OPENAI_MODEL` (optional, default: `gpt-4.1-mini`)

## Notes
- The prompt template is production-oriented JSON output so this can plug into a LaTeX rendering pipeline.
- If LLM output misses pieces, server fallback logic still returns structured output.
