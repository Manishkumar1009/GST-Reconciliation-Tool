GST Reconciliation Tool (AI-Powered Desktop Application)
A complete automated solution to reconcile Purchase Register with GSTR-2A efficiently and accurately — built using Python, Pandas, PyQt5, and packaged as a Windows Desktop App (.exe).

⭐ Overview
This tool automates the entire GST reconciliation process:
Matches Purchase Register with GSTR-2A
Detects missing invoices
Identifies incorrect GSTIN entries
Calculates tax/value differences
Assigns risk levels (High / Medium / Low)
Generates a clean Excel output report
Offers a modern and user-friendly desktop UI
The software runs offline, requires no Python, and installs like a professional Windows application using an EXE installer.

🔥 Key Features
✅ Automated Data Matching
Line-by-line reconciliation
Detects missing or mismatched invoices
Highlights tax and value differences

✅ Risk-Based Classification
High Risk: Missing in GSTR-2A
Medium Risk: Tax/value difference beyond threshold
Low Risk: Fully matched invoices

✅ Excel Output Report
Clean formatted Excel file
Includes value diff, tax diff, risk class
Ready for audit and filing

✅ Modern Desktop UI
Browse → Process → Export workflow
Progress bar + status updates
Dark/light mode (optional)
Smooth animated loading GIF

✅ Installer (EXE)
Installable like any software
Creates shortcuts
Works on any Windows system
No technical setup needed

📥 Download the Installer
Click below to download the latest version:
👉 https://github.com/Manishkumar1009/GST-Reconciliation-Tool/releases/download/v1.0/GST_Reconciliation_Setup.exe

📂 Output Folder Structure
The tool automatically creates:
Documents/
  GST_Reconciliation/
    GST_Reconciliation_Output.xlsx

⚙️ Tech Stack
Python 3.14
Pandas
PyQt5
NSIS Installer
Excel (OpenPyXL / Pandas)

🛠️ Installation
Download the installer (GST_Reconciliation_Setup.exe)
Run the installer
Follow on-screen instructions
Launch GST Reconciliation Tool from Start Menu or Desktop shortcut

📝 How to Use
Load Purchase Register
Load GSTR-2A
Click Run Reconciliation
Click Open Output Folder
Review the generated Excel report

🧠 Logic Summary
Matching keys:
InvoiceNo
VendorGSTIN ↔ GSTIN_Supplier
Generated fields:
Value_Diff
Tax_Diff
Risk
Match_Flag

🔒 System Requirements
Windows 10 / 11
4GB RAM
200MB free space
Excel installed (optional, for viewing output)

👤 Author
Manish Kumar S S
Accountant | GST Automation | Python Developer
📧 Email: manishkumar.fin09@gmail.com
🔗 LinkedIn: https://www.linkedin.com/in/manish-kumar-b85972338?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BYljx%2Fm%2BzRWW5CZklelsRKg%3D%3D

⭐ Support
If you encounter issues or want to request features:
Open an Issue on GitHub

Or message me on LinkedIn
