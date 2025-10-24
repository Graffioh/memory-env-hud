FROM public.ecr.aws/docker/library/python:3.11-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy source code first
COPY server/ ./server/
COPY environment/ ./environment/

# Install dependencies
RUN pip install --no-cache-dir ./server
RUN pip install --no-cache-dir ./environment

ENV ENV_SERVER_PORT=8005

# Start environment server in background, then run MCP server with hot-reload
CMD ["sh", "-c", "uvicorn environment.server:app --host 0.0.0.0 --port $ENV_SERVER_PORT --log-level warning --reload >&2 & sleep 0.5 && hud dev server.main --stdio"]
