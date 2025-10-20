FROM python:3.9
WORKDIR /app
COPY backend/ /app/backend/
COPY frontend/ /app/frontend/
RUN pip install -r backend/requirements.txt
EXPOSE 5000
CMD ["python", "backend/app.py"]
