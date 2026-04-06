from agents.pro_agent import pro_reason
from agents.con_agent import con_reason
from agents.evidence_agent import evaluate_evidence
from agents.moderator_agent import moderate

async def run_debate(query: str):
    pro = await pro_reason(query)
    con = await con_reason(query)
    evidence = await evaluate_evidence(pro, con)
    final = await moderate(pro, con, evidence)

    return {
        "pro": pro,
        "con": con,
        "evidence": evidence,
        "final": final
    }
