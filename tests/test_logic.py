from app.logic import heuristic_insights_dict, select_skills_from_matrix


def test_heuristic_insights_detects_core_terms():
    jd = "Need DevOps engineer with AWS, Kubernetes, Docker, Terraform and Jenkins experience"
    insights = heuristic_insights_dict(jd)
    assert insights["role"] == "DevOps Engineer"
    assert "aws" in insights["primary_skills"]
    assert "kubernetes" in insights["primary_skills"]


def test_select_skills_from_profile_matches_keywords():
    skills_matrix = {
        "Cloud": ["AWS", "Azure"],
        "DevOps": ["Kubernetes", "Docker", "Jenkins"],
        "Programming": ["Python"],
    }
    selected = select_skills_from_matrix(skills_matrix, ["aws", "docker"])
    assert selected == {"Cloud": ["AWS"], "DevOps": ["Docker"]}
