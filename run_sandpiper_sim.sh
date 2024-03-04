#!/bin/bash

cd "$(dirname "$0")"
source venv/bin/activate
nohup streamlit run pipelinesim.py --server.address=127.0.0.1 --server.port=8501 --server.enableCORS=false --server.enableXsrfProtection=false --server.enableWebsocketCompression=false
