# Severity Classifier

AI-powered triage tool that classifies incident descriptions into SEV1–SEV4 with rationale.

## Severity Levels

| Level | Name | Description |
|-------|------|-------------|
| SEV1 | Critical | Complete outage, all users affected, immediate revenue/SLA impact |
| SEV2 | Major | Significant degradation, large portion of users affected |
| SEV3 | Minor | Limited degradation, small subset of users, workaround exists |
| SEV4 | Low | Negligible impact, cosmetic or informational |

## Setup

```bash
pip install anthropic streamlit python-dotenv
```

Copy `.env.example` to `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=your_key_here
```

## Usage

### Local

```bash
streamlit run app.py
```

### Docker

```bash
docker build -t severity-classifier .
docker run -p 8501:8501 -e ANTHROPIC_API_KEY=your_key_here severity-classifier
```

Open [http://localhost:8501](http://localhost:8501), paste an alert or incident description, and click **Classify**.
