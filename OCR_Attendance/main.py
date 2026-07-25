import cv2
import pytesseract
import csv
import os
import datetime

# Configuration 


TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

ROSTER_FILE = "roster.csv"
ATTENDANCE_FILE = "attendance.csv"

# OCR Engine Setup
if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
else:
    print(f"[WARNING] Tesseract not found at {TESSERACT_PATH}")


# Helper Functions 

def load_roster():
    """Loads student IDs and Names from CSV into a dictionary."""
    roster = {}
    if not os.path.exists(ROSTER_FILE):
        print(f"[ERROR] {ROSTER_FILE} missing. Please create it.")
        return {}

    try:
        with open(ROSTER_FILE, mode='r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                if len(row) >= 2:
                    roster[row[0].strip()] = row[1].strip()
    except Exception as e:
        print(f"[ERROR] Failed to load roster: {e}")
    return roster


def is_already_present(student_id):
    """Checks if the student ID is already in the attendance file."""
    if not os.path.exists(ATTENDANCE_FILE):
        return False
    
    try:
        with open(ATTENDANCE_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                # Check first column for ID match 
                if len(row) > 0 and row[0].strip() == student_id.strip():
                    return True
    except Exception:
        return False
    return False


def mark_attendance(student_id, name):
    """
    Saves the student to the attendance CSV file with Status.
    Prevents duplicates.
    """
    # 1. Check for duplicates first
    if is_already_present(student_id):
        print(f"[INFO] Student '{name}' ({student_id}) is already marked present.")
        return False

    # 2. Prepare data
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "Present"
    
    file_exists = os.path.exists(ATTENDANCE_FILE)
    
    try:
        # 3. Append to file (newlines are handled automatically by csv.writer)
        with open(ATTENDANCE_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            
            # Add Header if file is new
            if not file_exists:
                writer.writerow(["ID", "Name", "Time", "Status"])
            
            # Write student data
            writer.writerow([student_id, name, timestamp, status])
            
        print(f"[SUCCESS] Marked present: {name} ({student_id})")
        return True
    except Exception as e:
        print(f"[ERROR] Could not save attendance: {e}")
        return False


def get_student_from_image(image_path, roster):
    """Reads image, runs OCR, finds match."""
    if not os.path.exists(image_path):
        return None

    try:
        img = cv2.imread(image_path)
        if img is None: return None

        # Preprocessing
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # OCR
        text = pytesseract.image_to_string(thresh).strip()
        
        # Matching
        for s_id, s_name in roster.items():
            if s_id in text or s_name.lower() in text.lower():
                return s_id, s_name
    except Exception:
        pass

    return None


def manual_entry_loop(roster):
    """Teacher Override."""
    while True:
        sid = input("Enter Student ID (or 'b' to back): ").strip()
        if sid.lower() == 'b':
            return
        
        if sid in roster:
            mark_attendance(sid, roster[sid])
            return
        else:
            print("[INVALID] ID not found in roster. Try again.")


def process_batch_folder(folder_path, roster):
    """Process all images in a folder."""
    if not os.path.exists(folder_path):
        print("[ERROR] Folder not found.")
        return

    files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    print(f"\n[BATCH] Found {len(files)} images. Processing...")

    count_success = 0
    
    for filename in files:
        full_path = os.path.join(folder_path, filename)
        result = get_student_from_image(full_path, roster)
        
        if result:
            s_id, s_name = result
            # mark_attendance now handles duplicate checks inside it
            if mark_attendance(s_id, s_name):
                count_success += 1
        else:
            print(f"[FAIL] Could not identify student in: {filename}")

    print(f"\n[BATCH FINISHED] New records added: {count_success}")


# Main Application Loop

def main():
    print("--- OCR Attendance System (No Duplicates + Status) ---")
    roster = load_roster()
    print(f"[INFO] Loaded {len(roster)} students.\n")

    while True:
        print("\n1. Process Single Image")
        print("2. Process Batch Folder (All images in folder)")
        print("3. Manual ID Entry (Override)")
        print("4. Exit")
        choice = input("Select: ").strip()

        if choice == "1":
            path = input("Enter image path: ").strip().strip('"')
            result = get_student_from_image(path, roster)

            if result:
                s_id, s_name = result
                print(f"\n[MATCH FOUND] {s_name} ({s_id})")
                confirm = input("Confirm attendance? (y/n): ").lower()
                if confirm == 'y':
                    mark_attendance(s_id, s_name)
            else:
                print("\n[FAIL] OCR could not read the ID/Name.")
                ask = input("Do you want to enter ID manually? (y/n): ").lower()
                if ask == 'y':
                    manual_entry_loop(roster)

        elif choice == "2":
            folder_path = input("Enter folder path: ").strip().strip('"')
            process_batch_folder(folder_path, roster)

        elif choice == "3":
            manual_entry_loop(roster)

        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()





