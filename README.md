# 🎓 OCR-Based Automated Attendance System

An automated, smart attendance management solution developed as the final capstone project for the **Access Control & Authentication Systems Program** presented by Google Developer Groups (GDG) Aden, Women Techmakers (WTM), and Technovation.

This system leverages Computer Vision and Optical Character Recognition (OCR) to automate student identification from document images or ID cards, seamlessly verifying rosters, logging timestamps, and actively preventing duplicate entries.

---

## 🌟 Key Features

* **Advanced Image Preprocessing:** Utilizes OpenCV for grayscale conversion and Otsu's Binarization thresholding to clean and optimize image contrast before text extraction.
* **Accurate Text Extraction:** Powered by Google's Tesseract OCR engine (`pytesseract`) to detect and extract student IDs and names from raw images.
* **Automated Roster Matching:** Dynamically loads student records from an external `roster.csv` database to validate extracted text against registered IDs and names.
* **Zero-Duplication Guarantee:** Built-in validation checks (`is_already_present`) inspect existing records to ensure a student cannot be marked present more than once per session.
* **Detailed Time-Logged CSV Export:** Automatically generates and updates an `attendance.csv` file with exact timestamps (`YYYY-MM-DD HH:MM:SS`) and attendance status (`Present`).
* **Flexible CLI Operation Modes:**
  * **Single Image Processing:** Scan an individual document/ID image with user confirmation.
  * **Batch Folder Processing:** Automatically iterate through an entire directory of images (`.png`, `.jpg`, `.jpeg`) to log multiple students in seconds.
  * **Manual Override Entry:** Built-in instructor fallback to manually input student IDs if an image is unreadable or physically damaged.

---

## 🛠️ Tech Stack & Libraries

* **Language:** Python 3.x
* **Computer Vision:** OpenCV (`opencv-python`)
* **OCR Engine:** Tesseract OCR (`pytesseract`)
* **Data Handling:** Native Python `csv`, `os`, and `datetime` modules

---

## ⚙️ Installation & Setup

### 1. Prerequisites
You must have Python installed along with the required libraries:
```bash 
pip install opencv-python pytesseract
```
2. Install Tesseract OCR Engine
Windows: Download and install Tesseract from the official Windows binaries.

Note: The default installation path configured in the script is C:\Program Files\Tesseract-OCR\tesseract.exe. If you install it elsewhere, update the TESSERACT_PATH variable in the script.

Linux (Debian/Ubuntu):

```bash
sudo apt update
sudo apt install tesseract-ocr
macOS:
```
```bash
brew install tesseract
```
🚀 Usage Instructions
1. Prepare Your Roster
Create a file named roster.csv in the project root directory with the following structure:

Code snippet
ID,Name
1001,Ahmed Mohamed
1002,Sarah Ali
1003,John Doe
2. Run the Application
Execute the main script from your terminal:

```Bash
python main.py
```
3. Select an Operation Mode
Upon launching, the interactive CLI will prompt you with the following menu:

Plaintext
--- OCR Attendance System (No Duplicates + Status) ---
[INFO] Loaded 3 students.

1. Process Single Image
2. Process Batch Folder (All images in folder)
3. Manual ID Entry (Override)
4. Exit
Option 1: Enter the relative or absolute path to a single ID image (e.g., images/id_1001.jpg).

Option 2: Enter the folder path containing multiple student ID images (e.g., batch_attendance/) for rapid automated logging.

Option 3: Manually type a student ID to mark attendance without image verification.

📂 Project Structure
Plaintext
├── main.py              # Core CLI application, OpenCV preprocessing & OCR pipeline
├── roster.csv           # Registered student database (ID, Name)
├── attendance.csv       # Automatically generated output log (ID, Name, Time, Status)
└── README.md            # Project documentation
🏆 Acknowledgments & Program Details
This project was built and presented as part of the Access Control & Authentication Systems Track.

Speaker & Mentor: Nuha Jadu

Program Judge: Mazen Othman

Supporting Communities:

Women Techmakers (WTM)

Technovation

Google Developer Groups (GDG) Aden
