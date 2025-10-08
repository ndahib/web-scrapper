from fpdf import FPDF


# Create a PDF document using FPDF
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Request for Absence Records - Years 2024 and 2025", ln=True, align="C")

        self.ln(5)

    def chapter_title(self, title):
        self.set_font("Arial", "B", 11)
        self.cell(0, 10, title, ln=True)
        self.ln(2)

    def chapter_body(self, body):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 8, body)
        self.ln()


pdf = PDF()
pdf.add_page()

# Header section
pdf.set_font("Arial", "", 11)
pdf.cell(0, 10, "To: Human Resources Department", ln=True)
pdf.cell(0, 10, "From: [Your Name / Team / Department]", ln=True)
pdf.cell(0, 10, "Date: [Insert Date]", ln=True)
pdf.cell(0, 10, "Subject: Request for Employee Absence Records (2024–2025)", ln=True)
pdf.ln(5)

# Introduction
intro = (
    "Dear HR Team,\n\n"
    "As part of our application development, we kindly ask you to provide the complete list "
    "of employee absences for the years 2024 and 2025.\n\n"
    "Please make sure the data includes the following details for each absence:"
)
pdf.chapter_body(intro)

# Absence Information
pdf.chapter_title("✅ Absence Information (for every absence):")
absence_info = (
    "1. Employee name or ID\n"
    "2. Who created the absence record (HR or manager name/ID)\n"
    "3. Absence type:\n"
    "   - Paid leave (Congé payé)\n"
    "   - Sick leave (Arrêt maladie)\n"
    "   - Personal reasons (Raisons personnelles)\n"
    "   - Parental leave (Congé parental)\n"
    "   - Other (Autre)\n"
    "4. Description or reason for the absence\n"
    "5. Duration:\n"
    "   - Full day (Jours)\n"
    "   - Half day (Demi-journée)\n"
    "     - If half day: specify Morning or Afternoon\n"
    "6. Start date of the absence\n"
    "7. End date of the absence\n"
    "8. Date the record was created"
)
pdf.chapter_body(absence_info)

# Attachments
pdf.chapter_title("📎 If available: Attached files")
attachments = "- Name of the file\n- Path or location (URL or folder)"
pdf.chapter_body(attachments)

# Absence Requests (Demandes)
pdf.chapter_title("📝 If the absence was requested in advance (Demande d’absence), please also include:")
requests = (
    "1. Name or ID of the employee who made the request\n"
    "2. Type of absence requested\n"
    "3. Reason for the request\n"
    "4. Duration and whether it was full day or half day\n"
    "5. Start and end dates of the request\n"
    "6. Status of the request (In progress, Approved, Rejected, Canceled, etc.)\n"
    "7. Date the request was submitted\n"
    "8. Names of people who approved or rejected the request\n"
    "9. Date of approval or rejection\n"
    "10. Reason for rejection (if applicable)"
)
pdf.chapter_body(requests)

# Format
pdf.chapter_title("📤 Format:")
format_text = (
    "Please provide the data in Excel or CSV format, and if needed, you can separate into 3 sheets or files:\n"
    "- Absences\n- Absence Requests (Demandes)\n- Attachments"
)
pdf.chapter_body(format_text)

# Closing
closing = "If anything is unclear, feel free to contact me directly.\n" "Thank you very much for your help!\n"
pdf.chapter_body(closing)

# Signature fields
pdf.chapter_body(
    "Sent by:\nName: _________________________\nTeam: _________________________\nEmail: _________________________\nDate: _________________________"
)

# Output the PDF
pdf.output("absence_request_form.pdf")
