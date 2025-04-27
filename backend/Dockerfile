FROM python:3.12

WORKDIR /app

# Install dependencies
RUN pip install fastapi uvicorn[standard] motor redis.asyncio python-dotenv pydantic pydantic-settings google-generativeai better-profanity

# Copy the backend code
COPY backend/ .

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
