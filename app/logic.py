from __future__ import annotations

import re
from typing import Dict, List


def tokenize(text: str) -> List[str]:
    return [t.lower() for t in re.findall(r"[A-Za-z0-9+#.-]+", text)]


def heuristic_insights_dict(job_description: str) -> dict:
    tokens = tokenize(job_description)
    popular = [
        "aws",
        "azure",
        "gcp",
        "kubernetes",
        "docker",
        "jenkins",
        "terraform",
        "ansible",
        "linux",
        "python",
        "bash",
        "prometheus",
        "grafana",
        "cloudwatch",
        "ci/cd",
    ]
    found = [k for k in popular if any(k in t for t in tokens)]
    role = "DevOps Engineer"
    if "sre" in tokens:
        role = "Site Reliability Engineer"
    elif "cloud" in tokens and "engineer" in tokens:
        role = "Cloud Engineer"

    return {
        "role": role,
        "primary_skills": found[:6],
        "secondary_skills": found[6:10],
        "ats_keywords": sorted(set(found + ["automation", "scalability", "monitoring"])),
        "tools_priority": [k for k in found if k not in {"linux", "python", "bash"}],
    }


def select_skills_from_matrix(skills_matrix: Dict[str, List[str]], keywords: List[str]) -> Dict[str, List[str]]:
    lowered = [k.lower() for k in keywords]
    selected: Dict[str, List[str]] = {}
    for category, skills in skills_matrix.items():
        relevant = [s for s in skills if any(k in s.lower() for k in lowered)]
        if relevant:
            selected[category] = relevant
    return selected
