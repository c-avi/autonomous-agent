from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
import os

# === Configuration ===
CHROME_DRIVER_PATH = "E:/autonomous-agent/chromedriver.exe"
LOG_PATH = "logs/history.txt"


# === Helper Functions ===

def create_browser():
    print("🤖 Starting Agent...\n")
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def perform_task(driver, task):
    driver.get("https://www.google.com/")
    time.sleep(2)
    search = driver.find_element(By.NAME, "q")
    search.send_keys(task)
    search.send_keys(Keys.RETURN)
    time.sleep(3)
    log_action(f"✅ Searched for: {task} on Google")

def log_action(message):
    os.makedirs("logs", exist_ok=True)
    entry = f"{time.ctime()} — {message}"
    if message.strip():
        with open(LOG_PATH, "a", encoding="utf-8") as log_file:
            log_file.write(entry + "\n")

def view_history():
    print("\n📜 Task History:\n")
    if not os.path.exists(LOG_PATH):
        print("No task history yet.")
        return []

    with open(LOG_PATH, "r", encoding="utf-8") as log_file:
        lines = log_file.readlines()
        for i, line in enumerate(lines, 1):
            print(f"{i}. {line.strip()}")
        return lines


# === Main Menu ===

while True:
    print("\n===== 🤖 Autonomous Agent Menu =====")
    print("1. Run a new task")
    print("2. Retry failed tasks (demo)")
    print("3. View task history and retry")
    print("0. Exit")
    choice = input("Choose option: ")

    if choice == "1":
        task = input("📝 Enter your task (like 'Search for laptops on Amazon'): ")
        driver = create_browser()
        perform_task(driver, task)
        input("🛑 Press Enter to close the browser...")

    elif choice == "2":
        print("⚠️ Retry logic not implemented yet. Coming soon.")

    elif choice == "3":
        history = view_history()
        if history:
            num = input("\n🔁 Enter task number to retry (or press Enter to go back): ")
            if num.isdigit() and 1 <= int(num) <= len(history):
                task_line = history[int(num)-1]
                task = task_line.split("—")[-1].replace("✅ Searched for: ", "").replace("on Google", "").strip()
                driver = create_browser()
                perform_task(driver, task)
                input("🛑 Press Enter to close the browser...")
            else:
                print("❌ Invalid input or cancelled.")
        else:
            print("📭 No history available to retry.")

    elif choice == "0":
        print("👋 Exiting...")
        break

    else:
        print("❌ Invalid option. Please try again.")
