# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py .
COPY pr_list_view.py .
COPY pr_detail_view.py .
COPY pr_files_view.py .
COPY repo_filter_screen.py .
COPY comment_screen.py .

# Set environment variables (will be overridden by user)
ENV GITHUB_TOKEN=""
ENV GITHUB_ORG=""

# Run the application
CMD ["python", "main.py"]
