import re

import anthropic
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """\
You are a senior incident responder responsible for triaging incoming alerts and tickets.
Given a description of an incident or alert, classify it into one of four severity levels
and explain your reasoning clearly.

Use these definitions:
- SEV1 — Critical: complete outage or data loss, all or most users affected, revenue/SLA impact immediate.
- SEV2 — Major: significant degradation or partial outage, large portion of users affected, workaround unavailable or unclear.
- SEV3 — Minor: limited degradation, small subset of users affected, workaround exists.
- SEV4 — Low: negligible impact, cosmetic or informational, no user-facing effect.

Respond in this exact format:

## Severity: SEV[1-4] — [Critical / Major / Minor / Low]

**Rationale:**
[2-4 sentences explaining why this severity was chosen, referencing specific details from the input.]

**Key factors:**
- [factor 1]
- [factor 2]
- [factor 3 if applicable]
"""


def classify(description: str):
    client = anthropic.Anthropic()
    with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": description}],
    ) as stream:
        for text in stream.text_stream:
            yield text


SEV_COLORS = {
    "SEV1": "🔴",
    "SEV2": "🟠",
    "SEV3": "🟡",
    "SEV4": "🟢",
}

EXAMPLES = [
    "Checkout service returning 503 for all users. Payment processing down. Started 4 minutes ago.",
    "Elevated latency on search API — p99 at 4s vs baseline of 400ms. ~15% of search requests affected.",
    "Typo in footer text on marketing homepage. No functional impact.",
    "Dashboard showing stale data for a small cohort of enterprise users. Workaround: refresh clears it.",
]

# ── UI ────────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="Severity Classifier", page_icon="🚨", layout="centered")
st.title("Severity Classifier")
st.caption("Paste an alert or incident description to get an instant SEV classification.")

with st.expander("Load an example"):
    for example in EXAMPLES:
        if st.button(example[:80] + "...", key=example):
            st.session_state["input_text"] = example

description = st.text_area(
    "Incident or alert description",
    height=180,
    placeholder="e.g. Auth service throwing 500s for SSO logins. Affects all enterprise customers. Started 6 minutes ago.",
    value=st.session_state.get("input_text", ""),
)

if st.button("Classify", type="primary"):
    if not description.strip():
        st.warning("Please enter a description first.")
    else:
        st.divider()
        output = st.empty()
        full = ""
        for chunk in classify(description):
            full += chunk
            output.markdown(full + "▌")
        output.markdown(full)

        # Badge
        match = re.search(r"##\s*Severity:\s*(SEV[1-4])", full)
        if match:
            sev = match.group(1)
            st.toast(f"{SEV_COLORS[sev]} {sev} classified", icon=None)

        st.session_state["last_result"] = full
        st.session_state.pop("input_text", None)
