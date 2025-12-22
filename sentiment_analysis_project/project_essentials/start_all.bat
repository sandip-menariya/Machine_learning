@echo off
start cmd /k redis-server
timeout /t 5
start cmd /k celery -A sent_analysis worker --loglevel=info -P eventlet
timeout /t 5
start cmd /k python manage.py runserver
@REM @echo off
@REM ECHO Starting Redis...
@REM start "Redis" cmd /k redis-server

@REM timeout /t 5
@REM ECHO Starting Django Server...
@REM start "Django" cmd /k python manage.py runserver

@REM timeout /t 5
@REM ECHO Starting Celery Worker...
@REM start "CeleryWorker" cmd /k celery -A sent_analysis worker --loglevel=info -P eventlet

@REM timeout /t 5
@REM ECHO Starting Celery Beat Scheduler...
@REM start "CeleryBeat" cmd /k celery -A sent_analysis beat --loglevel=info -P eventlet