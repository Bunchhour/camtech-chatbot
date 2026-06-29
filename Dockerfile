# 1. Base Image: We start with a lightweight vesion of Linuz that already has python 3.12 installed
FROM python:3.12-slim

# 2. Working Directory: We create a folder inside the container called/app and move insid it
WORKDIR /app

# 3. Install our package manager 'uv' inside the container
RUN pip install uv

# 4. Caching layer:  We copy only our dependency files first
COPY pyproject.toml uv.lock ./

# 5. Install the dependiencies.
RUN uv sync --frozen --no-dev

# 6. Copy the rest of your actual python code into the container
COPY  . .

# 7. Expose the port so the outside world can talk to container
EXPOSE 8000

# 8. The command to start your API when the container turns on
CMD ["uv", "run", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]