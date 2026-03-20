# 1. Start with a lightweight Python image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file first
COPY requirements.txt .

# 4. Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code
COPY . .

# 6. Expose the port FastAPI runs on
EXPOSE 8000

# 7. Start the application using your specific filename
CMD ["uvicorn", "main(2):app", "--host", "0.0.0.0", "--port", "8000"]
