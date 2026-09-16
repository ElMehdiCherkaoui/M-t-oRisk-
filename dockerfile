From python:3.9-slim

workdir /app

copy requirements.txt .

run pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "streamlit", "run", "dashboard/app.py"]