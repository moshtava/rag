FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set environment variables
#ENV HF_TOKEN="hf_SGRQSDKiDflsYrqlilxlERqjQffnjNdmmmcmcxZFG"
#ENV API_KEY="WdsZlKvXsjMPP71kCFOByouIVwn8573ry5ty56tt56tF"

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]