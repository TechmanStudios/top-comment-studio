from .schemas import CommentInput, GuardrailReview


REJECT_TERMS = {
    "slur",
    "dox",
    "doxx",
    "kill yourself",
    "explicit sex",
    "gore",
}

REDIRECT_TERMS = {
    "destroy",
    "blow up",
    "bomb",
    "hack",
    "steal",
    "real city",
    "celebrity",
    "spongebob",
    "marvel",
    "disney",
}


def review_comment(comment_input: CommentInput) -> GuardrailReview:
    text = comment_input.selected_comment.strip()
    lowered = text.lower()

    if not text:
        return GuardrailReview(
            status="needs_human_review",
            risk_categories=["empty_comment"],
            reason="No audience signal was provided.",
            safe_interpretation="Ask Bryan to provide a usable audience comment or creator seed.",
        )

    rejected = sorted(term for term in REJECT_TERMS if term in lowered)
    if rejected:
        return GuardrailReview(
            status="rejected",
            risk_categories=["unsafe_or_abusive"],
            reason=f"The comment contains blocked terms or unsafe framing: {', '.join(rejected)}.",
            safe_interpretation="Choose the next strongest safe audience comment.",
        )

    redirected = sorted(term for term in REDIRECT_TERMS if term in lowered)
    if redirected:
        return GuardrailReview(
            status="approved_with_redirect",
            risk_categories=["redirect_required"],
            reason=f"The comment has a usable creative spark, but needs a safer fictional framing: {', '.join(redirected)}.",
            safe_interpretation=f"A fictional, YouTube-safe simulation inspired by the audience request: {text}",
        )

    return GuardrailReview(
        status="approved",
        risk_categories=[],
        reason="The comment is usable for a short-form audience-directed episode.",
        safe_interpretation=f"The next episode responds to the audience request: {text}",
    )
