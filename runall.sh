#!/bin/bash
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT
cd backend
python manage.py runserver 0.0.0.0:8000 &
cd ..
xdg-open localhost:8080
cd frontend
vue serve

