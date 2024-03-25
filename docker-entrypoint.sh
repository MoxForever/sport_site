sleep 5
python -m aerich upgrade
python -m uvicorn main:app --port $APP_PORT --host 0.0.0.0