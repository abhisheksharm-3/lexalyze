from typing import Dict, List

from server.app.main import LegalClause, LegalEntities


def _compare_entities(entities1: LegalEntities, entities2: LegalEntities) -> Dict:
    """Compare entities between two documents"""
    return {
        "unique_to_first": {
            "parties": list(set(entities1.parties) - set(entities2.parties)),
            "judges": list(set(entities1.judges) - set(entities2.judges)),
            "lawyers": list(set(entities1.lawyers) - set(entities2.lawyers)),
            "courts": list(set(entities1.courts) - set(entities2.courts)),
            "organizations": list(set(entities1.organizations) - set(entities2.organizations))
        },
        "unique_to_second": {
            "parties": list(set(entities2.parties) - set(entities1.parties)),
            "judges": list(set(entities2.judges) - set(entities1.judges)),
            "lawyers": list(set(entities2.lawyers) - set(entities1.lawyers)),
            "courts": list(set(entities2.courts) - set(entities1.courts)),
            "organizations": list(set(entities2.organizations) - set(entities1.organizations))
        },
        "modified": {
            "parties": list(set(entities1.parties) & set(entities2.parties)),
            "judges": list(set(entities1.judges) & set(entities2.judges)),
            "lawyers": list(set(entities1.lawyers) & set(entities2.lawyers)),
            "courts": list(set(entities1.courts) & set(entities2.courts)),
            "organizations": list(set(entities1.organizations) & set(entities2.organizations))
        }
    }

def _compare_obligations(obligations1: List[Dict[str, str]], obligations2: List[Dict[str, str]]) -> Dict:
    """Compare obligations between two documents"""
    return {
        "unique_to_first": [o for o in obligations1 if o not in obligations2],
        "unique_to_second": [o for o in obligations2 if o not in obligations1],
        "modified": [
            {"from": o1, "to": o2}
            for o1 in obligations1
            for o2 in obligations2
            if o1["text"] != o2["text"] and o1["type"] == o2["type"]
        ]
    }

def _compare_deadlines(deadlines1: List[Dict[str, str]], deadlines2: List[Dict[str, str]]) -> Dict:
    """Compare deadlines between two documents"""
    return {
        "unique_to_first": [d for d in deadlines1 if d not in deadlines2],
        "unique_to_second": [d for d in deadlines2 if d not in deadlines1],
        "modified": [
            {"from": d1, "to": d2}
            for d1 in deadlines1
            for d2 in deadlines2
            if d1["text"] != d2["text"] and d1["date"] != d2["date"]
        ]
    }

def _compare_monetary_values(values1: List[Dict[str, str]], values2: List[Dict[str, str]]) -> Dict:
    """Compare monetary values between two documents"""
    return {
        "unique_to_first": [v for v in values1 if v not in values2],
        "unique_to_second": [v for v in values2 if v not in values1],
        "modified": [
            {"from": v1, "to": v2}
            for v1 in values1
            for v2 in values2
            if v1["value"] != v2["value"]
        ]
    }
def _compare_clauses(clauses1: List[LegalClause], clauses2: List[LegalClause]) -> Dict:
    """Compare clauses between two documents"""
    return {
        "unique_to_first": [c.dict() for c in clauses1 if not any(
            c.text == c2.text for c2 in clauses2
        )],
        "unique_to_second": [c.dict() for c in clauses2 if not any(
            c.text == c1.text for c1 in clauses1
        )],
        "modified": [
            {"from": c1.dict(), "to": c2.dict()}
            for c1 in clauses1
            for c2 in clauses2
            if c1.clause_type == c2.clause_type and c1.text != c2.text
        ]
    }