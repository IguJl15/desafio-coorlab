#!/bin/bash

function check_return_code() {
  cmd_description="$1"
  result_code="$2"

  if [[ $result_code -ne 0 ]]; then
    echo "$cmd_description failed with code: $result_code"
    exit 1
  fi
}


echo "Iniciando as aplicaçoes frontend e backend"
echo ""

workdir=$(pwd)

backend_dir=$workdir/backend
frontend_dir=$workdir/frontend

fixture_flights=$workdir/data.json

# frontend
if ! cd "$frontend_dir"; then
  echo "Failed to change directory to '$frontend_dir' (return code $?)."
  echo "Please check if the directory exists and is accessible."
  exit 1
fi
mkdir -p logs

npm install
check_return_code "npm install", $?

npm run build-only

echo "Starting frontend..."

run_frontend_cmd="npm run preview -- --port 8080"
${run_frontend_cmd} &> "logs/frontend.log" & disown;

echo "Frontend should be started soon at http://localhost:8080"

# backend
if ! cd "$backend_dir"; then
  echo "Failed to change directory to '$frontend_dir' (return code $?)."
  echo "Please check if the directory exists and is accessible."
  exit 1
fi
mkdir -p logs

python3 -m venv .venv

source ".venv/bin/activate"
check_return_code "source", $?

pip install -r requirements.txt
check_return_code "pip install", $?

python3 manage.py migrate
check_return_code "migrate", $?

# run custom command to load fixtures, mocked, flights
python3 manage.py loadjsondata "$fixture_flights"
check_return_code "loadjsondata", $?

echo "Starting backend..."

run_backend_cmd="python3 manage.py runserver localhost:3000"
${run_backend_cmd} &> "logs/backend.log" & disown;

echo "Backend should be started soon at http://localhost:3000"

echo 'Both application should be starting. Check their respective log files at "logs" folder (inside each project)'