# Polygon Stock Data API

An exploratory FastAPI endpoint that requests Polygon aggregate stock data and inserts results into a MySQL database.

## Overview

`main.py` mounts the router in `services/stock.py`. The active route is `GET /fetch-and-insert-multiple-data`; inspect its parameters in `/docs` before calling it. The implementation uses fixed historical dates and is an experiment, not a general-purpose or live market-data service.

## Tech stack

Python, FastAPI, requests, mysql-connector-python, Uvicorn, Polygon API, and MySQL.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export POLYGON_IO_API_KEY="your-own-key"
uvicorn main:app --reload
```

On Windows activate with `.venv\Scripts\activate` and set the variable with `$env:POLYGON_IO_API_KEY="your-own-key"` in PowerShell. Supply your own MySQL database and schema expected by `services/stock.py`; the current database settings are still coded in that file and are not yet portable.

## Configuration and security

`POLYGON_IO_API_KEY` is required by the active module and the optional `test.py` script. Copy the variable name from `.env.example`; do not commit a real value. A key was previously present in committed source and may remain in git history. Rotate it if it was real. Changing the latest files does not clean history.

## Limitations

The API uses fixed date ranges, and the current code has limited validation and error handling. It has not been verified against a live Polygon account or MySQL schema.
