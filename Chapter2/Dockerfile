# Use lightweight Python image
FROM python:3.13-slim

# Set working directory inside container
WORKDIR /app


# Copy application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r reqs.txt

# Expose Flask port
EXPOSE 5000

# Run the Flask app
CMD [ "python", "main.py"]