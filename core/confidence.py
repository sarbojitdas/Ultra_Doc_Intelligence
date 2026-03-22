def compute_confidence(answer, docs):
    if not docs:
        return 0.0

    score = 0.5 + (0.1 * len(docs))

    if "don't know" in answer.lower():
        score -= 0.3

    return round(min(score, 1.0), 2)