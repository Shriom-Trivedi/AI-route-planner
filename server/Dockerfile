# Dockerfile

FROM route-planner-base:latest

# If building locally, uncomment below and remove the above line:
# FROM llm-base:latest

WORKDIR /app

COPY . .

EXPOSE 8000

CMD ["python", "run.py"]
