# 📌 Prescription to Google Calendar
Transform prescriptions into structured calendar reminders effortlessly! This project automates the extraction of medicines, tests, and checkup schedules from prescriptions and syncs them with Google Calendar.

## 🚀 Features
1) OCR-Powered Extraction: Converts prescription images into text.
2) AI Processing: Identifies medicines, dosages, and schedules.
3) Google Calendar Integration: Automatically adds reminders.
4) Easy to Use: Just upload a prescription image and stay organized.

## 🔧 Setup & Installation
1. **Clone the repository**  
```sh
git clone https://github.com/shreshthkapai/prescription_to_google_calender.git
cd prescription_to_google_calender
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
2. **Create a virtual environment (optional but recommended)**
```sh
conda env create -f environment.yml
```
3. **Activate the environment**
```sh
   conda activate prescription_env
```
4. **Set up Google Calendar API**
   4.1 Follow the Google Calendar API Python Quickstart guide to enable the API and obtain the credentials.json file.
   4.2 Paste the JSON data in the credentials.json file in the google_auth_json_files directory located at the root of this repository.

##📌 To-Do / Future Enhancements
🔜 Add a simple web UI for user uploads
🔜 Support for multiple languages
🔜 Integration with other calendar apps

## 🤝 Contributing
Pull requests are welcome! Feel free to fork the repo, make changes, and submit a PR.
