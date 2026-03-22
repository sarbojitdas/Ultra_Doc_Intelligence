def apply_guardrails(answer, docs):
    if not docs:
        return "I don't know based on the document.", 0.0

    if len(answer.strip()) < 5:
        return "I don't know based on the document.", 0.2

    return answer, 0.9