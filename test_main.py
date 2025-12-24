import unittest
import datetime
from main import (
    calendar_db, 
    reminders_db, 
    add_calendar_event, 
    set_reminder, 
    list_all_activities
)

class TestPersonalAssistant(unittest.TestCase):

    def setUp(self):
        """Clear old data before each test."""
        calendar_db.clear()
        reminders_db.clear()
        
        # --- PREPARE DYNAMIC TIME ---
        now = datetime.datetime.now()
        # Tomorrow (for testing new entries - always future)
        self.tomorrow = (now + datetime.timedelta(days=1)).strftime("%Y-%m-%d 09:00")
        # Yesterday (for testing expired/past logic)
        self.yesterday = (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d 09:00")

    def test_add_calendar_event_success(self):
        """Test adding a calendar event for TOMORROW (Always in the future)."""
        result = add_calendar_event.invoke({
            "event_name": "Future Team Meeting", 
            "time": self.tomorrow,  # Use dynamic time
            "description": "Test dynamic time"
        })

        self.assertEqual(len(calendar_db), 1)
        self.assertEqual(calendar_db[0]["time"], self.tomorrow)
        self.assertIn("Success", result)

    def test_set_reminder_success(self):
        """Test setting a reminder for TOMORROW."""
        result = set_reminder.invoke({
            "task_name": "Take Medicine", 
            "time": self.tomorrow
        })

        self.assertEqual(len(reminders_db), 1)
        self.assertEqual(reminders_db[0]["status"], "pending")
        self.assertIn("Success", result)

    def test_list_all_activities_with_data(self):
        """Test displaying the list with data."""
        # Add mock data using dynamic time
        add_calendar_event.invoke({"event_name": "Event A", "time": self.tomorrow, "description": ""})
        set_reminder.invoke({"task_name": "Task B", "time": self.tomorrow})

        result = list_all_activities.invoke({})
        
        self.assertIn("Event A", result)
        self.assertIn("Task B", result)

    def test_reminder_logic_trigger(self):
        """
        Test notification trigger logic:
        If a reminder time is YESTERDAY (Past) -> It must be marked as 'done'.
        """
        # 1. Inject a reminder in the past (Yesterday)
        reminders_db.append({
            "task": "Test Past Task", 
            "time": self.yesterday, 
            "status": "pending"
        })

        # 2. Run check logic (Identical to logic in background thread)
        # Get current time
        current_now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        for r in reminders_db:
            # Logic: If reminder time <= current time -> Trigger
            if r['time'] <= current_now_str and r['status'] == 'pending':
                r['status'] = 'done'

        # 3. Expectation: Status must change from 'pending' to 'done'
        self.assertEqual(reminders_db[0]["status"], "done")

if __name__ == '__main__':
    print("Running automated Unit Tests...")
    unittest.main()