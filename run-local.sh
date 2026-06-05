#!/bin/bash
set -e

IMAGE="novai-local"
PORT="${1:-8000}"
ENV_FILE="backend/.env"

# ── Kill anything holding the port ───────────────────────────────────────────
PIDS=$(lsof -i :"$PORT" -sTCP:LISTEN -t 2>/dev/null || true)
if [ -n "$PIDS" ]; then
  for PID in $PIDS; do
    CMD=$(ps -p "$PID" -o comm= 2>/dev/null || echo "inconnu")
    echo "🔫  Kill '$CMD' (PID $PID) sur le port $PORT..."
    kill -9 "$PID" 2>/dev/null || true
  done
  sleep 0.5
fi

# ── Load API key ──────────────────────────────────────────────────────────────
if [ ! -f "$ENV_FILE" ]; then
  echo "❌  $ENV_FILE introuvable. Crée-le avec ANTHROPIC_API_KEY=sk-ant-..."
  exit 1
fi

API_KEY=$(grep -E "^ANTHROPIC_API_KEY=" "$ENV_FILE" | cut -d= -f2-)

if [ -z "$API_KEY" ] || [ "$API_KEY" = "sk-ant-REMPLACE_MOI" ]; then
  echo "❌  Clé API non configurée. Édite $ENV_FILE avec ta vraie clé."
  exit 1
fi

# ── Build ─────────────────────────────────────────────────────────────────────
echo "🔨  Build de l'image Docker '$IMAGE'..."
docker build -t "$IMAGE" .

# ── Run ───────────────────────────────────────────────────────────────────────
echo ""
echo "🚀  Démarrage du conteneur sur http://localhost:$PORT"
echo "    Ctrl+C pour arrêter"
echo ""

docker run --rm \
  -p "$PORT:$PORT" \
  -e ANTHROPIC_API_KEY="$API_KEY" \
  -e PORT="$PORT" \
  "$IMAGE"
