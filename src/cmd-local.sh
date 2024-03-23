#!/bin/bash
uvicorn app.main:app --app-dir=./ --reload --workers=1 --host=0.0.0.0 --port=8080  --use-colors --loop=uvloop