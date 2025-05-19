FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libgdal-dev \
        libgeos-dev \
        libproj-dev \
        && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY concordance_script.py .
COPY pd_analysis.py .
COPY data/*.geojson .

CMD ["bash"]