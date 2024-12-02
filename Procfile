# Run all development server processes via the honcho process manager
# Start the dev environment via `honcho start` at the command line
# Stop via sending the `Control+C` to send interrupt signal

proxy: caddy run
backend: uvicorn --port=4402 --reload backend.main:app --reload-exclude es_files*
frontend: cd frontend && npm run dev
