import discord
import json
import os

# report file mangement
class ReportFile():
    def __init__(self, path):
        self.path = path
        self.data = {}
    
    def load(self): # Overwrites memory with the file
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding = "utf-8") as f:
                    self.data = json.load(f)
            except Exception as e:
                print(f"Error loading reports: {e}")
        else:
            print("Reports file does not exist, using default blank format")
            self.data = {"count": 0, "id": 0, "pending": [], "reports": []}

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent = 4, ensure_ascii = False)
        self.load()
    
    def add_report(self, report: dict):
        self.data["reports"].append(report)

# add more tools later
