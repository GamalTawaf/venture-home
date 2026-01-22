FROM python:3.14.2-slim-bookworm

# Prevents Python from writing pyc files to disk.
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr.
ENV PYTHONUNBUFFERED=1
# Create the application directory and set it as the working directory.
RUN mkdir -p /app
WORKDIR /app
# copy app folder
COPY . /app/

# Install system packages required to build some Python packages (Postgres).
# Keep image small by not installing recommended packages and cleaning apt lists.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# expose port for the application
EXPOSE 8000

# Run Django's development server.
CMD ["./startup.sh"]