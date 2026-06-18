from typing import Iterable, Tuple, Dict, List

RISK_WEIGHTS = {
    "SMS": 30,
    "Contacts": 20,
    "Location": 20,
    "Microphone": 15,
    "Camera": 10,
    "Phone": 15,
    "Storage": 5,
    "Identity": 10,
    "Device ID & call information": 20,
}

DEFAULT_RISK_WEIGHT = 2

RISK_LEVEL_THRESHOLDS = {
    "Low": 30,
    "Medium": 60,
    "High": 100,
}


def calculate_risk(permission_types: Iterable[str]) -> Tuple[int, str, Dict[str, int], str, List[str]]:
    """Calculate the risk score and return:

    - score (0-100)
    - level (Low/Medium/High)
    - breakdown: mapping of permission type -> weight used
    - explanation: short human-readable summary
    - recommendations: list of security recommendations
    """

    unique_types = set(permission_types)
    breakdown: Dict[str, int] = {}
    for t in unique_types:
        breakdown[t] = RISK_WEIGHTS.get(t, DEFAULT_RISK_WEIGHT)

    score = sum(breakdown.values())
    score = min(score, RISK_LEVEL_THRESHOLDS["High"])

    level = _get_risk_level(score)

    explanation = _generate_explanation(score, level, breakdown)
    recommendations = _generate_recommendations(breakdown)

    return score, level, breakdown, explanation, recommendations


def _get_risk_level(score: int) -> str:
    """Return a human-readable risk level for the given score."""

    if score < RISK_LEVEL_THRESHOLDS["Low"]:
        return "Low"
    if score < RISK_LEVEL_THRESHOLDS["Medium"]:
        return "Medium"
    return "High"


def _generate_explanation(score: int, level: str, breakdown: Dict[str, int]) -> str:
    """Create a concise explanation for the calculated score."""

    if not breakdown:
        return "No permissions were detected; risk is minimal."

    # List top contributors (by weight)
    sorted_items = sorted(breakdown.items(), key=lambda x: x[1], reverse=True)
    top = sorted_items[:3]
    top_desc = ", ".join(f"{t} ({w})" for t, w in top)

    return f"Score {score} ({level}): top contributors — {top_desc}."


def _generate_recommendations(breakdown: Dict[str, int]) -> List[str]:
    """Return prioritized security recommendations based on permission types."""

    recs: List[str] = []
    types = set(breakdown.keys())

    if any(t in types for t in ("SMS", "Phone")):
        recs.append("Avoid granting SMS or direct-call permissions unless the app explicitly needs them for core functionality.")

    if any(t in types for t in ("Location",)):
        recs.append("Limit location access: prefer 'While Using' rather than background/location always-on permissions.")

    if any(t in types for t in ("Contacts", "Identity")):
        recs.append("Review why the app needs contact or identity access; restrict where possible and avoid syncing contacts automatically.")

    if any(t in types for t in ("Camera", "Microphone")):
        recs.append("Only allow camera/microphone during active use; disable background capture permissions.")

    if any(t in types for t in ("Device ID & call information",)):
        recs.append("Device identifiers increase tracking risk — avoid apps that read device IDs unless necessary.")

    if any(t in types for t in ("Storage", "Photos/Media/Files")) and "Storage" in breakdown:
        recs.append("Restrict file storage access; use scoped storage or grant only explicit files when required.")

    # Generic recommendation
    if not recs:
        recs.append("No immediate security recommendations; permissions appear minimal.")

    # Keep recommendations concise and de-duplicated
    seen = set()
    final: List[str] = []
    for r in recs:
        if r not in seen:
            final.append(r)
            seen.add(r)

    return final