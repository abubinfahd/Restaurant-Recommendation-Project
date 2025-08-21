# Use a slim Python base image
FROM python:3.10-slim

# System deps for building common ML/DS wheels (numpy, pandas, scikit-learn, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc \
 && rm -rf /var/lib/apt/lists/*

# Workdir
WORKDIR /app

# Install Python deps first (better caching)
COPY requirements.txt . 

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install Python dependencies with a longer timeout and alternate package index (optional)
RUN pip install --no-cache-dir -i https://pypi.org/simple -r requirements.txt --timeout=120

# Copy the whole project
COPY . .

# Useful envs
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1

# Expose both app ports (Flask 5000, Streamlit 8501)
EXPOSE 5000 8501

# Default command (overridden by docker-compose)
CMD ["python", "-V"]
