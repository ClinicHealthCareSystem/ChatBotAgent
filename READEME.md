## First time

1.  python -m venv .venv
2.  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
3.  .\.venv\Scripts\activate
4.  pip install -r requirements.txt
5.  uvicorn app.main:app --reload

## Running

1.  [powershell] Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
2.  [powershell] .\.venv\Scripts\activate
3.  [powershell] uvicorn app.main:app --reload
