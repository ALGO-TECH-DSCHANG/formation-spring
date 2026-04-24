#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUN_DIR="$ROOT_DIR/.run"
PID_DIR="$RUN_DIR/pids"
LOG_DIR="$RUN_DIR/logs"
INFRA_FILE="$ROOT_DIR/docker-compose.infra.yml"

SERVICES=(
  "discovery-service:discovery-service:8761:no:no"
  "member-service:member-service:8081:yes:no"
  "event-service:event-service:8082:yes:no"
  "booking-service:booking-service:8083:yes:yes"
  "notification-service:notification-service:8084:yes:yes"
  "api-gateway:api-gateway:8080:no:no"
)

usage() {
  cat <<'EOF'
Usage:
  ./run-all.sh build        Build all services (skip tests)
  ./run-all.sh start        Start all services in background
  ./run-all.sh stop         Stop all services started by this script
  ./run-all.sh restart      Stop then start all services
  ./run-all.sh status       Show service status
  ./run-all.sh logs [name]  Tail logs for all services or one service
  ./run-all.sh infra-up     Start MySQL + RabbitMQ with docker compose
  ./run-all.sh infra-down   Stop MySQL + RabbitMQ
EOF
}

ensure_dirs() {
  mkdir -p "$PID_DIR" "$LOG_DIR"
}

port_is_open() {
  local port="$1"
  timeout 1 bash -c "</dev/tcp/127.0.0.1/$port" >/dev/null 2>&1
}

check_java() {
  local version raw major
  raw="$(java -version 2>&1 | head -n1)"
  version="$(java -version 2>&1 | awk -F '"' '/version/ {print $2}')"
  major="${version%%.*}"

  if [[ "$major" -lt 25 ]]; then
    echo "Java 25+ is required. Current: $raw"
    exit 1
  fi
}

build_one() {
  local name="$1"
  local dir="$2"
  echo "[build] $name"
  (cd "$ROOT_DIR/$dir" && mvn clean package -DskipTests)
}

build_all() {
  check_java
  for svc in "${SERVICES[@]}"; do
    IFS=':' read -r name dir _ _ _ <<<"$svc"
    build_one "$name" "$dir"
  done
}

start_one() {
  local name="$1"
  local dir="$2"
  local port="$3"
  local needs_db="$4"
  local needs_rabbit="$5"
  local pid_file="$PID_DIR/$name.pid"
  local log_file="$LOG_DIR/$name.log"
  local jar_file

  jar_file="$(ls "$ROOT_DIR/$dir"/target/"$name"-*.jar 2>/dev/null | grep -v '\.original$' | head -n1 || true)"
  if [[ -z "$jar_file" ]]; then
    echo "[start] Missing jar for $name, building first"
    build_one "$name" "$dir"
    jar_file="$(ls "$ROOT_DIR/$dir"/target/"$name"-*.jar 2>/dev/null | grep -v '\.original$' | head -n1 || true)"
  fi

  if [[ -f "$pid_file" ]] && kill -0 "$(cat "$pid_file")" 2>/dev/null; then
    echo "[start] $name already running (pid $(cat "$pid_file"))"
    return
  fi

  if [[ "$needs_db" == "yes" ]] && ! port_is_open 3308; then
    echo "[warn] MySQL port 3308 is closed. $name may fail to start."
  fi
  if [[ "$needs_rabbit" == "yes" ]] && ! port_is_open 5672; then
    echo "[warn] RabbitMQ port 5672 is closed. $name may fail to start."
  fi

  echo "[start] $name on port $port"
  nohup java -jar "$jar_file" >"$log_file" 2>&1 &
  echo $! >"$pid_file"
}

start_all() {
  check_java
  ensure_dirs
  for svc in "${SERVICES[@]}"; do
    IFS=':' read -r name dir port needs_db needs_rabbit <<<"$svc"
    start_one "$name" "$dir" "$port" "$needs_db" "$needs_rabbit"
    sleep 2
  done
  echo "[done] Stack started. Use './run-all.sh status' or './run-all.sh logs'."
}

stop_one() {
  local name="$1"
  local pid_file="$PID_DIR/$name.pid"
  if [[ -f "$pid_file" ]]; then
    local pid
    pid="$(cat "$pid_file")"
    if kill -0 "$pid" 2>/dev/null; then
      echo "[stop] $name (pid $pid)"
      kill "$pid"
      sleep 1
      if kill -0 "$pid" 2>/dev/null; then
        kill -9 "$pid" 2>/dev/null || true
      fi
    fi
    rm -f "$pid_file"
  else
    echo "[stop] $name not started by script"
  fi
}

stop_all() {
  for ((i=${#SERVICES[@]}-1; i>=0; i--)); do
    IFS=':' read -r name _ _ _ _ <<<"${SERVICES[$i]}"
    stop_one "$name"
  done
}

status_all() {
  for svc in "${SERVICES[@]}"; do
    IFS=':' read -r name _ port _ _ <<<"$svc"
    local pid_file="$PID_DIR/$name.pid"
    if [[ -f "$pid_file" ]] && kill -0 "$(cat "$pid_file")" 2>/dev/null; then
      echo "$name: RUNNING (pid $(cat "$pid_file"), port $port)"
    else
      echo "$name: STOPPED (port $port)"
    fi
  done
}

logs_cmd() {
  ensure_dirs
  if [[ $# -gt 0 ]]; then
    tail -n 200 -f "$LOG_DIR/$1.log"
  else
    tail -n 60 -f "$LOG_DIR"/*.log
  fi
}

infra_up() {
  if [[ ! -f "$INFRA_FILE" ]]; then
    echo "Missing $INFRA_FILE"
    exit 1
  fi
  docker compose -f "$INFRA_FILE" up -d
}

infra_down() {
  if [[ ! -f "$INFRA_FILE" ]]; then
    echo "Missing $INFRA_FILE"
    exit 1
  fi
  docker compose -f "$INFRA_FILE" down
}

main() {
  local cmd="${1:-}"
  case "$cmd" in
    build) build_all ;;
    start) start_all ;;
    stop) stop_all ;;
    restart) stop_all; start_all ;;
    status) status_all ;;
    logs) shift; logs_cmd "$@" ;;
    infra-up) infra_up ;;
    infra-down) infra_down ;;
    *) usage; exit 1 ;;
  esac
}

main "$@"
