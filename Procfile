# Run all development server processes via the honcho process manager
# Start the dev environment via `honcho start` at the command line
# Stop via sending the `Control+C` to send interrupt signal

proxy: caddy run
backend: fastapi dev backend/main.py
frontend: cd frontend && npm run dev