FROM python:3.10.12-slim

# Set the working directory in the container
WORKDIR /app


# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose the FastAPI port (optional, you can specify it when running the container)
EXPOSE 3000

# Set the Python path to your FastAPI app (you can use PYTHONPATH environment variable)
ENV PYTHONPATH=/app/app

# Run the FastAPI application using uvicorn
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
CMD ["flask", "run", "--host=0.0.0.0",  "--port=3000"]