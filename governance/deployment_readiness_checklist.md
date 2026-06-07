# Deployment Readiness Checklist

## Pre-Deployment

- [ ] FAISS index is built with the latest document set
- [ ] Evaluation has been run on the golden dataset
- [ ] No critical low-quality cases (score < 0.4) without documented review
- [ ] API keys are configured via environment variables or Streamlit secrets
- [ ] `.env` is in `.gitignore` — no secrets in version control
- [ ] `requirements.txt` includes all dependencies
- [ ] Streamlit app starts without errors

## Streamlit Cloud Deployment

To deploy on Streamlit Community Cloud:

1. Push the repository to GitHub
2. Go to https://share.streamlit.io
3. Select the repository and branch
4. Set the main file path to `app/streamlit_app.py`
5. Add secrets in Streamlit Cloud dashboard:
   - `GROQ_API_KEY`
   - `MISTRAL_API_KEY` (or `GEMINI_API_KEY` depending on evaluator)
   - `EVALUATOR_PROVIDER`
   - `EVALUATOR_MODEL_NAME`
6. Deploy

No `.env` file is needed on Streamlit Cloud — the app reads `st.secrets` via `python-dotenv`'s fallback or the Streamlit secrets manager.

## Post-Deployment

- [ ] Verify the app loads and shows the Ask Assistant tab
- [ ] Verify the Evaluation Dashboard tab loads with demo data
- [ ] Test with a sample query
- [ ] Confirm SPC chart renders
- [ ] Check that missing API key errors are user-friendly
- [ ] Verify CSV download works

## Production Considerations (V2)

- [ ] Replace synthetic documents with real (anonymised) SME policies
- [ ] Add human evaluation layer to validate LLM-as-judge scores
- [ ] Implement live telemetry and time-series SPC monitoring
- [ ] Add authentication and access control
- [ ] Conduct privacy impact assessment
- [ ] Establish incident response procedure
- [ ] Define model update and re-deployment process
