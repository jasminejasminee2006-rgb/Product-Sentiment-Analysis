PRODUCT SENTIMENT ANALYZER AND REVIEW DASHBOARD
================================================

HOW TO RUN IN VS CODE (Windows)

1. Extract this ZIP file.
2. Open VS Code.
3. Select File > Open Folder and choose the extracted ProductSentimentAnalyzer folder.
4. Open Terminal > New Terminal.
5. Create a virtual environment:

   python -m venv venv

6. Activate it in PowerShell:

   .\venv\Scripts\Activate.ps1

   If PowerShell blocks activation, run this command in that terminal:
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   Then activate again.

7. Install dependencies:

   python -m pip install -r requirements.txt

8. Start the application:

   python app.py

9. Open this address in Chrome:
   http://127.0.0.1:5000

IMPORTANT
---------
This ZIP contains a working starter prototype. It analyzes built-in sample
reviews so you can test the Flask application, sentiment classification,
SQLite storage, and dashboard. It does NOT yet collect live Amazon or
Flipkart reviews. Live scraping is a separate next development stage and
must respect each website's terms and access restrictions.

To stop the server, click the terminal and press Ctrl+C.
