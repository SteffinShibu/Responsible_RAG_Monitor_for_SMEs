# Project Rules — Responsible RAG Monitor for SMEs

## Repository
- **Git remote:** `origin` → `https://github.com/SteffinShibu/Responsible_RAG_Monitor_for_SMEs.git`
- **Branch:** `main` (single developer, portfolio project)
- **Deployed:** https://steffinshibu-responsible-rag-monitor-fo-appstreamlit-app-bmjbbv.streamlit.app/

## Operation Ledger
This project has a permanent context handoff document at `V1_CONTEXT.md` in the project root. Before starting any work in a new session, read `V1_CONTEXT.md` to understand the current architecture, state, and implicit constraints.

## Git Rules
- **Never commit `.env`** — contains real API keys.
- **Never commit real API keys** in any file.
- `.env.example` must contain only placeholder values (`PASTE_YOUR_*_HERE`).
- `data/evaluation_results.csv` is gitignored — regenerate with `python scripts/run_evaluation.py`.
- `vectorstore/faiss_index/*.{faiss,json,pkl}` is gitignored — auto-built on Streamlit startup.
- Always run `git status` and `git diff --stat` before committing to verify no secrets staged.
- Commit messages should be descriptive (what changed and why, one line summary + bullet details).

## Code Style
- No comments in source code unless explaining a non-obvious design decision.
- Use descriptive function and variable names (self-documenting code).
- Python imports: standard library, third-party, local (grouped with blank lines).
- Type hints on all function signatures (`typing` module).
- Path resolution: always use `Path(__file__).resolve().parent` relative to the file, never hardcoded absolute paths.
- Config values go in `src/config.py` with `os.getenv("VAR", "default")` pattern.

## Streamlit Rules
- Always call `st.set_page_config()` first (page title, icon, layout).
- Use `from streamlit import st` (not `import streamlit as st` — actually `import streamlit as st` is fine, but be consistent).
- No API calls in the Evaluation Dashboard tab — it reads only CSV data.
- Use `st.spinner()` for long operations.
- Handle all empty/error states with `st.info()`, `st.warning()`, or `st.error()` followed by `st.stop()`.

## Testing
- No formal test framework set up yet (v1).
- Verify with: `python -m py_compile <file>` for syntax, `python -c "from <module> import <func>"` for imports.
- For full verification: run `streamlit run app/streamlit_app.py` locally.

## Deployment
- Streamlit Cloud secrets must match the keys in `src/config.py` exactly.
- The app uses `os.getenv()` — compatible with both `.env` and Streamlit secrets.
- FAISS index is NOT committed — auto-built via `ensure_index_built()` with spinner.
- Dashboard works without API keys for visualising existing results.
