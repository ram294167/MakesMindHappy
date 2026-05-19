"""
Career Recommendation Engine.
Rule-based scoring — structured so ML scoring can replace or supplement this later.
"""
from typing import Dict, List, Any


# Career profiles — matches based on answer patterns
CAREER_PROFILES = [
    {
        "title": "Psychologist / Counsellor",
        "emoji": "🧠",
        "interest_areas": ["humanities", "social", "helping"],
        "personality_types": ["empathetic", "introvert_helper", "reflective"],
        "aptitude_areas": ["verbal", "social"],
        "stream": "Arts / Science (Psychology)",
        "strengths": ["Empathy", "Listening", "Analytical thinking"],
        "base_score": 75,
    },
    {
        "title": "Doctor / Medical Professional",
        "emoji": "⚕️",
        "interest_areas": ["science", "helping", "biology"],
        "personality_types": ["analytical", "detail_oriented", "helper"],
        "aptitude_areas": ["science", "memory"],
        "stream": "Science (PCB)",
        "strengths": ["Attention to detail", "Science aptitude", "Empathy"],
        "base_score": 70,
    },
    {
        "title": "Software Engineer",
        "emoji": "💻",
        "interest_areas": ["technology", "logic", "building"],
        "personality_types": ["logical", "introvert", "builder"],
        "aptitude_areas": ["math", "logic", "patterns"],
        "stream": "Science (PCM)",
        "strengths": ["Logical thinking", "Problem solving", "Focus"],
        "base_score": 70,
    },
    {
        "title": "Business / Entrepreneur",
        "emoji": "🚀",
        "interest_areas": ["business", "leadership", "finance"],
        "personality_types": ["leader", "extrovert", "risk_taker"],
        "aptitude_areas": ["verbal", "logic", "social"],
        "stream": "Commerce",
        "strengths": ["Leadership", "Communication", "Decision making"],
        "base_score": 68,
    },
    {
        "title": "UX / Product Designer",
        "emoji": "🎨",
        "interest_areas": ["design", "technology", "creativity"],
        "personality_types": ["creative", "visual_thinker", "empathetic"],
        "aptitude_areas": ["visual", "creative", "pattern"],
        "stream": "Any stream + Design",
        "strengths": ["Creativity", "Visual thinking", "User empathy"],
        "base_score": 72,
    },
    {
        "title": "Teacher / Educator",
        "emoji": "📚",
        "interest_areas": ["teaching", "helping", "communication"],
        "personality_types": ["patient", "communicator", "helper"],
        "aptitude_areas": ["verbal", "social"],
        "stream": "Arts / Science / Commerce",
        "strengths": ["Patience", "Communication", "Subject knowledge"],
        "base_score": 70,
    },
    {
        "title": "Journalist / Writer",
        "emoji": "✍️",
        "interest_areas": ["writing", "communication", "social"],
        "personality_types": ["creative", "communicator", "curious"],
        "aptitude_areas": ["verbal", "creative"],
        "stream": "Arts / Humanities",
        "strengths": ["Writing", "Research", "Communication"],
        "base_score": 68,
    },
    {
        "title": "Chartered Accountant / Finance",
        "emoji": "💰",
        "interest_areas": ["finance", "numbers", "business"],
        "personality_types": ["analytical", "detail_oriented", "methodical"],
        "aptitude_areas": ["math", "logic", "detail"],
        "stream": "Commerce (PCM helpful)",
        "strengths": ["Analytical thinking", "Attention to detail", "Discipline"],
        "base_score": 68,
    },
    {
        "title": "Social Worker / NGO Professional",
        "emoji": "🤝",
        "interest_areas": ["helping", "social", "community"],
        "personality_types": ["empathetic", "driven", "communicator"],
        "aptitude_areas": ["verbal", "social"],
        "stream": "Arts / Social Work",
        "strengths": ["Compassion", "Communication", "Drive to help"],
        "base_score": 65,
    },
    {
        "title": "Architect / Civil Engineer",
        "emoji": "🏛️",
        "interest_areas": ["design", "building", "science"],
        "personality_types": ["creative", "methodical", "builder"],
        "aptitude_areas": ["visual", "math", "spatial"],
        "stream": "Science (PCM)",
        "strengths": ["Spatial thinking", "Creativity", "Maths"],
        "base_score": 70,
    },
]


def score_answers(answers: Dict[str, str]) -> Dict[str, float]:
    """
    Convert raw answers to dimensional scores (0–100).
    Rule-based scoring — extensible for ML later.
    """
    scores = {
        "aptitude": 60.0,
        "personality": 60.0,
        "eq": 60.0,
        "interests": 60.0,
        "career_fit": 60.0,
        "learning": 60.0,
    }

    # Aptitude scoring
    apt_answers = [answers.get(f"apt{i}") for i in range(1, 4)]
    apt_boost = sum(1 for a in apt_answers if a in ("a", "c")) * 7
    scores["aptitude"] = min(95, 60 + apt_boost)

    # Personality scoring
    per_answers = [answers.get(f"per{i}") for i in range(1, 4)]
    per_boost = sum(1 for a in per_answers if a in ("a", "b")) * 8
    scores["personality"] = min(95, 60 + per_boost)

    # EQ scoring
    eq_answers = [answers.get(f"eq{i}") for i in range(1, 3)]
    eq_boost = sum(1 for a in eq_answers if a in ("a", "b")) * 12
    scores["eq"] = min(95, 60 + eq_boost)

    # Interest scoring
    int_answers = [answers.get(f"int{i}") for i in range(1, 4)]
    scores["interests"] = min(95, 65 + len([a for a in int_answers if a]) * 7)

    # Career fit
    cf_answers = [answers.get(f"cf{i}") for i in range(1, 4)]
    cf_boost = sum(1 for a in cf_answers if a in ("a", "b")) * 8
    scores["career_fit"] = min(95, 60 + cf_boost)

    # Learning style
    scores["learning"] = 75.0

    return scores


def determine_learning_style(answers: Dict[str, str]) -> str:
    ls1 = answers.get("ls1", "")
    ls2 = answers.get("ls2", "")
    styles = [ls1, ls2]
    counts = {
        "visual": styles.count("visual"),
        "auditory": styles.count("auditory"),
        "reading": styles.count("reading"),
        "kinesthetic": styles.count("kinesthetic"),
    }
    primary = max(counts, key=counts.get)  # type: ignore
    style_map = {
        "visual": "Visual Learner",
        "auditory": "Auditory Learner",
        "reading": "Reading/Writing Learner",
        "kinesthetic": "Kinesthetic/Hands-on Learner",
    }
    return style_map.get(primary, "Mixed Learning Style")


def recommend_careers(
    scores: Dict[str, float],
    answers: Dict[str, str]
) -> List[Dict[str, Any]]:
    """
    Map scores and answers to top career matches.
    Returns top 4 careers with match percentage and explanation.
    """
    # Determine answer-based interest signals
    interest_signals = []
    if answers.get("int1") == "a":
        interest_signals.extend(["writing", "creativity", "humanities"])
    elif answers.get("int1") == "b":
        interest_signals.extend(["social", "communication", "helping"])
    elif answers.get("int1") == "c":
        interest_signals.extend(["building", "technology", "logic"])
    elif answers.get("int1") == "d":
        interest_signals.extend(["outdoors", "physical", "exploration"])

    if answers.get("int2") == "a":
        interest_signals.extend(["science", "technology"])
    elif answers.get("int2") == "b":
        interest_signals.extend(["business", "finance", "commerce"])
    elif answers.get("int2") == "c":
        interest_signals.extend(["arts", "humanities", "writing"])
    elif answers.get("int2") == "d":
        interest_signals.extend(["social", "psychology", "helping"])

    if answers.get("cf1") == "a":
        interest_signals.extend(["building", "technology"])
    elif answers.get("cf1") == "b":
        interest_signals.extend(["helping", "medicine", "counselling", "teaching"])
    elif answers.get("cf1") == "c":
        interest_signals.extend(["creativity", "design", "arts"])
    elif answers.get("cf1") == "d":
        interest_signals.extend(["business", "leadership", "entrepreneurship"])

    # Score each career against signals
    career_scores = []
    for career in CAREER_PROFILES:
        overlap = len(set(career["interest_areas"]) & set(interest_signals))
        score = career["base_score"] + overlap * 8

        # Boost based on dimensional scores
        if scores["eq"] > 75 and "helping" in career.get("interest_areas", []):
            score += 5
        if scores["aptitude"] > 75 and "logic" in career.get("aptitude_areas", []):
            score += 5

        score = min(99, score)
        career_scores.append({
            "title": career["title"],
            "emoji": career["emoji"],
            "match": round(score),
            "stream": career["stream"],
            "strengths": career["strengths"],
            "why": f"Your profile shows strong alignment with this field based on your interests and personality.",
            "nextStep": "Discuss with the mentor to get a specific roadmap for this career.",
        })

    # Return top 4 sorted by match
    career_scores.sort(key=lambda x: x["match"], reverse=True)
    return career_scores[:4]


def recommend_stream(
    scores: Dict[str, float],
    answers: Dict[str, str]
) -> Dict[str, str]:
    """Return stream recommendation based on scores."""
    int2 = answers.get("int2", "")
    aptitude = scores.get("aptitude", 60)

    if int2 == "a" and aptitude > 70:
        primary = "Science (PCM)"
        secondary = "Science (PCB)"
        avoid = "Commerce — unless you want business + tech"
    elif int2 == "b":
        primary = "Commerce"
        secondary = "Arts / BBA"
        avoid = "Pure Science — unless you enjoy maths/science subjects"
    elif int2 == "c":
        primary = "Arts / Humanities"
        secondary = "Commerce"
        avoid = "Pure Science (PCM) — unless you have strong aptitude"
    elif int2 == "d":
        primary = "Arts / Humanities"
        secondary = "Science (PCB)"
        avoid = "PCM — unless maths is a strong suit"
    else:
        primary = "Arts / Humanities"
        secondary = "Commerce"
        avoid = "Make this decision after the full mentoring session"

    return {
        "primary": primary,
        "secondary": secondary,
        "avoid": avoid,
        "reason": "Based on your interest areas and aptitude profile from the assessment.",
    }


def identify_strengths(
    scores: Dict[str, float],
    answers: Dict[str, str]
) -> List[str]:
    """Return top 4–5 strengths based on scores."""
    strengths = []
    if scores.get("eq", 0) > 75:
        strengths.append("High emotional intelligence — you understand people well")
    if scores.get("personality", 0) > 75:
        strengths.append("Strong personality clarity — you know how you operate")
    if scores.get("aptitude", 0) > 75:
        strengths.append("Good reasoning and problem-solving aptitude")
    if answers.get("per1") == "a":
        strengths.append("Natural leadership tendencies in group situations")
    if answers.get("int1") in ("a", "b"):
        strengths.append("Strong communication and verbal skills")
    if answers.get("cf1") == "b":
        strengths.append("Strong drive to help others — a valuable career asset")
    if not strengths:
        strengths = ["Thoughtful and self-aware", "Open to guidance and growth"]
    return strengths[:5]


def identify_skill_gaps(
    scores: Dict[str, float],
    answers: Dict[str, str]
) -> List[str]:
    """Return areas to develop."""
    gaps = []
    if scores.get("aptitude", 0) < 70:
        gaps.append("Analytical / numerical reasoning needs consistent practice")
    if scores.get("eq", 0) < 65:
        gaps.append("Emotional regulation and self-awareness can be developed")
    if answers.get("per2") == "d":
        gaps.append("Working on managing stress and staying action-oriented when overwhelmed")
    gaps.append("Building structured study habits will significantly help")
    return gaps[:3]


def build_action_plan(
    scores: Dict[str, float],
    answers: Dict[str, str],
    top_careers: List[Dict]
) -> List[str]:
    """Generate a basic action plan."""
    top_career = top_careers[0]["title"] if top_careers else "your top career match"
    return [
        f"Have a conversation with your family about your inclination toward {top_career}",
        "Book a 1-on-1 mentoring session to go through your full report in detail",
        "Research the educational path required for your top 2 career matches",
        "Focus on the subjects that align with your chosen stream starting this week",
        "Start a small hobby or activity that builds skills in your interest area",
    ]


def generate_result(assessment_id: int, answers: Dict[str, str]):
    """Main function: takes answers, returns full result dict."""
    scores = score_answers(answers)
    learning_style = determine_learning_style(answers)
    top_careers = recommend_careers(scores, answers)
    stream = recommend_stream(scores, answers)
    strengths = identify_strengths(scores, answers)
    skill_gaps = identify_skill_gaps(scores, answers)
    action_plan = build_action_plan(scores, answers, top_careers)

    overall = round(
        (scores["aptitude"] * 0.2 + scores["personality"] * 0.2 +
         scores["eq"] * 0.2 + scores["interests"] * 0.2 +
         scores["career_fit"] * 0.2)
    )

    return {
        "assessment_id": assessment_id,
        "overall_score": overall,
        "aptitude_score": scores["aptitude"],
        "personality_score": scores["personality"],
        "eq_score": scores["eq"],
        "learning_style": learning_style,
        "interest_score": scores["interests"],
        "career_fit_score": scores["career_fit"],
        "top_careers": top_careers,
        "stream_recommendation": stream,
        "strengths": strengths,
        "skill_gaps": skill_gaps,
        "action_plan": action_plan,
        "mentor_notes": None,
    }
