import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sent_analysis.settings')
django.setup()

# Now import your task function
# Replace 'dashboard.tasks' with the actual path to your tasks.py file
from sent_app.tasks import stream_and_save_comments

if __name__ == '__main__':
    print("Attempting to run the task directly...")
    try:
        # Call the function directly, not as a Celery task
        stream_and_save_comments.delay()
        print("Task completed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")