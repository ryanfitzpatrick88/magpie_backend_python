# Build the Docker image
# docker build -t financial_budgeting_app .

# Run the Docker container with the new port mapping
# docker run -d -p 8000:8000 financial_budgeting_app

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload