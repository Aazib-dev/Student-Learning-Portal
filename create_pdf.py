import os
import pymupdf
from PIL import Image as PILImage
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
)
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_OUTPUT = os.path.join(BASE_DIR, "Aazib_Akram_Student_Learning_Portal_Assignment.pdf")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
TEMP_IMG_DIR = os.path.join(BASE_DIR, ".pdf_img_cache")
os.makedirs(TEMP_IMG_DIR, exist_ok=True)

GITHUB_REPO_URL = "https://github.com/Aazib-dev/Student-Learning-Portal"

def optimize_image(filename, max_width=500, quality=85):
    src = os.path.join(SCREENSHOTS_DIR, filename)
    dst = os.path.join(TEMP_IMG_DIR, filename.replace(".png", ".jpg"))
    if not os.path.exists(src):
        return None
    with PILImage.open(src) as img:
        img = img.convert("RGB")
        w, h = img.size
        if w > max_width:
            new_h = int(h * (max_width / float(w)))
            img = img.resize((max_width, new_h), PILImage.Resampling.LANCZOS)
        img.save(dst, "JPEG", quality=quality, optimize=True)
    return dst

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (Pages 2+)
        if self._pageNumber > 1:
            self.drawString(54, 750, "Student Learning Portal — Mobile Application Development Assignment")
            self.drawRightString(558, 750, "Aazib Akram")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.75)
            self.line(54, 744, 558, 744)

        # Footer (All pages)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(54, 42, 558, 42)
        
        repo_text = "GitHub: github.com/Aazib-dev/Student-Learning-Portal"
        self.drawString(54, 30, repo_text)
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 30, page_str)
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_OUTPUT,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=50
    )
    
    styles = getSampleStyleSheet()
    
    c_primary = colors.HexColor("#1E3A8A")
    c_secondary = colors.HexColor("#2563EB")
    c_body = colors.HexColor("#334155")
    c_accent_bg = colors.HexColor("#EFF6FF")
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=c_primary,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=c_secondary,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13.5,
        leading=17,
        textColor=c_primary,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=c_secondary,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=c_body,
        spaceAfter=5
    )

    th_style = ParagraphStyle(
        'TH_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12.5,
        textColor=colors.white
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=c_primary,
        alignment=1,
        spaceBefore=3,
        spaceAfter=4
    )

    link_box_style = ParagraphStyle(
        'LinkBoxText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=c_primary,
        alignment=1
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#0F172A")
    )

    elements = []

    # ================= PAGE 1 =================
    elements.append(Paragraph("Student Learning Portal", title_style))
    elements.append(Paragraph("Android Mobile Application Development (Kotlin) — Assignment Submission", subtitle_style))
    
    info_data = [
        [
            Paragraph("<b>Student Name:</b>", body_style),
            Paragraph("Aazib Akram", body_style),
            Paragraph("<b>Degree Program:</b>", body_style),
            Paragraph("BS Computer Science", body_style)
        ],
        [
            Paragraph("<b>Technology:</b>", body_style),
            Paragraph("Kotlin / Android SDK 36", body_style),
            Paragraph("<b>Architecture:</b>", body_style),
            Paragraph("RelativeLayout & LinearLayout", body_style)
        ]
    ]
    info_table = Table(info_data, colWidths=[90, 160, 100, 154])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 8))

    github_box_content = [
        [
            Paragraph(
                f"🔗 <b>Public GitHub Repository (Source Code & APK):</b><br/>"
                f"<a href='{GITHUB_REPO_URL}'><b><u>{GITHUB_REPO_URL}</u></b></a><br/>"
                f"<font size='8' color='#64748B'><i>(Click the link above to view repository, source files, and live commits)</i></font>",
                link_box_style
            )
        ]
    ]
    github_table = Table(github_box_content, colWidths=[504])
    github_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_accent_bg),
        ('BOX', (0,0), (-1,-1), 1.5, c_secondary),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    elements.append(github_table)
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("1. Executive Summary & Features", h1_style))
    elements.append(Paragraph(
        "This project implements the complete assignment requirements for the <b>Student Learning Portal</b>. "
        "The project consists of two dedicated Activities built in <b>Kotlin</b> using traditional native Android XML views, "
        "strictly conforming to the designated layout managers (<b>RelativeLayout</b> for registration, <b>LinearLayout</b> for login), "
        "inter-activity data passing via <b>Intents</b>, and comprehensive form validations.",
        body_style
    ))

    req_data = [
        [Paragraph("<b>Component / Requirement</b>", th_style), Paragraph("<b>Specification</b>", th_style), Paragraph("<b>Implementation Status</b>", th_style)],
        [Paragraph("Screen 1 Layout", body_style), Paragraph("Must use <b>RelativeLayout</b>", body_style), Paragraph("<b>[Completed]</b> activity_create_account.xml", body_style)],
        [Paragraph("App Title & Logo", body_style), Paragraph("Portal title and custom emblem image", body_style), Paragraph("<b>[Completed]</b> Custom Vector Logo + TextView", body_style)],
        [Paragraph("User Input Fields", body_style), Paragraph("Name, Student ID, Email, Password, Confirm Password", body_style), Paragraph("<b>[Completed]</b> 5 Form EditTexts with styled backgrounds", body_style)],
        [Paragraph("Department Dropdown", body_style), Paragraph("Select Dept, CS, SE, IT, AI", body_style), Paragraph("<b>[Completed]</b> Spinner with XML string-array", body_style)],
        [Paragraph("Semester Dropdown", body_style), Paragraph("Select Semester, 1st to 8th", body_style), Paragraph("<b>[Completed]</b> Spinner with XML string-array", body_style)],
        [Paragraph("Admission Date", body_style), Paragraph("Interactive calendar selection", body_style), Paragraph("<b>[Completed]</b> DatePickerDialog integration (dd/MM/yyyy)", body_style)],
        [Paragraph("Signup Validations", body_style), Paragraph("All empty, dept, sem, passwords match", body_style), Paragraph("<b>[Completed]</b> 5 Sequential Toast validation rules", body_style)],
        [Paragraph("Screen 2 Layout", body_style), Paragraph("Must use <b>LinearLayout</b>", body_style), Paragraph("<b>[Completed]</b> activity_login.xml", body_style)],
        [Paragraph("Intent Data Transfer", body_style), Paragraph("Receive student name on Login screen", body_style), Paragraph("<b>[Completed]</b> Displays: <i>'Welcome, Muhammad Ali!'</i>", body_style)],
        [Paragraph("Login Validation", body_style), Paragraph("Empty checks vs successful login", body_style), Paragraph("<b>[Completed]</b> 'Please enter...' & 'Login Successful'", body_style)],
    ]
    req_table = Table(req_data, colWidths=[130, 200, 174])
    req_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    elements.append(req_table)

    # ================= PAGE 2 =================
    elements.append(PageBreak())
    elements.append(Paragraph("2. Screen 1 — Create Account (RelativeLayout Architecture)", h1_style))
    elements.append(Paragraph(
        "Screen 1 is designed using <b>RelativeLayout</b> as the root and main container layout. All child views are explicitly positioned "
        "relative to each other using attributes like <code>android:layout_below</code> and <code>android:layout_centerHorizontal</code>. "
        "Tapping the Date of Admission field opens a native <b>DatePickerDialog</b>.",
        body_style
    ))

    s1_main = optimize_image("screen1_create_account.png")
    s1_picker = optimize_image("screen1_datepicker.png")
    s1_filled = optimize_image("screen1_date_filled.png")

    img_w, img_h = 150, 320
    row1_cells = [
        [Image(s1_main, width=img_w, height=img_h), Image(s1_picker, width=img_w, height=img_h), Image(s1_filled, width=img_w, height=img_h)],
        [Paragraph("Fig 1: RelativeLayout Signup Screen", caption_style), Paragraph("Fig 2: Calendar DatePickerDialog", caption_style), Paragraph("Fig 3: Date Populated (25/09/2026)", caption_style)]
    ]
    t_row1 = Table(row1_cells, colWidths=[168, 168, 168])
    t_row1.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
    ]))
    elements.append(t_row1)
    elements.append(Spacer(1, 6))

    elements.append(Paragraph("<b>DatePickerDialog Implementation Highlights:</b>", h2_style))
    elements.append(Paragraph(
        "A <code>Calendar.getInstance()</code> object captures current year, month, and day. "
        "When the user selects a date, a callback formats the result as <code>dd/MM/yyyy</code> and populates the <code>EditText</code>:",
        body_style
    ))
    dp_code = (
        "etDateOfAdmission.setOnClickListener {\n"
        "    DatePickerDialog(this, { _, year, month, day ->\n"
        "        etDateOfAdmission.setText(String.format(Locale.getDefault(), \"%02d/%02d/%04d\", day, month + 1, year))\n"
        "    }, calendar.get(Calendar.YEAR), calendar.get(Calendar.MONTH), calendar.get(Calendar.DAY_OF_MONTH)).show()\n"
        "}"
    )
    t_dp = Table([[Paragraph(dp_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)]], colWidths=[504])
    t_dp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(t_dp)

    # ================= PAGE 3 =================
    elements.append(PageBreak())
    elements.append(Paragraph("3. Screen 1 Dropdowns & Signup Form Validations", h1_style))
    elements.append(Paragraph(
        "The assignment requires robust validation on the signup form with explicit Toast messages. "
        "Below are screenshots demonstrating the Department and Semester dropdowns, followed by the empty fields check.",
        body_style
    ))

    s1_dept_dd = optimize_image("screen1_dept_dropdown.png")
    s1_sem_dd = optimize_image("screen1_sem_dropdown.png")
    s1_val_empty = optimize_image("screen1_validation_empty.png")

    row2_cells = [
        [Image(s1_dept_dd, width=img_w, height=img_h), Image(s1_sem_dd, width=img_w, height=img_h), Image(s1_val_empty, width=img_w, height=img_h)],
        [Paragraph("Fig 4: Department Dropdown List", caption_style), Paragraph("Fig 5: Semester Dropdown List", caption_style), Paragraph("Fig 6: 'Please fill all fields'", caption_style)]
    ]
    t_row2 = Table(row2_cells, colWidths=[168, 168, 168])
    t_row2.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
    ]))
    elements.append(t_row2)
    elements.append(Spacer(1, 6))

    elements.append(Paragraph("<b>Spinner Dropdown Configuration:</b>", h2_style))
    elements.append(Paragraph(
        "Both Spinners use XML string-array resources (<code>departments_array</code> and <code>semesters_array</code>) "
        "defined in <code>strings.xml</code>, ensuring zero hardcoding and clean separation of concerns. "
        "Position 0 acts as the prompt item ('Select Department' / 'Select Semester').",
        body_style
    ))

    # ================= PAGE 4 =================
    elements.append(PageBreak())
    elements.append(Paragraph("4. Specific Validation Cases & Account Creation Success", h1_style))
    elements.append(Paragraph(
        "Screen 1 sequentially validates every input constraint. If Department or Semester are not chosen (position 0), "
        "or if passwords do not match, dedicated warning Toasts appear. When valid, a success Toast appears and the Intent navigates to Screen 2.",
        body_style
    ))

    s1_val_dept = optimize_image("screen1_validation_dept.png")
    s1_val_sem = optimize_image("screen1_validation_sem.png")
    s1_val_pwd = optimize_image("screen1_validation_pwd.png")
    s1_val_success = optimize_image("screen1_success_toast.png")

    v_w, v_h = 118, 255
    row3_cells = [
        [Image(s1_val_dept, width=v_w, height=v_h), Image(s1_val_sem, width=v_w, height=v_h), Image(s1_val_pwd, width=v_w, height=v_h), Image(s1_val_success, width=v_w, height=v_h)],
        [Paragraph("Fig 7: 'Please select department'", caption_style), Paragraph("Fig 8: 'Please select semester'", caption_style), Paragraph("Fig 9: 'Passwords do not match'", caption_style), Paragraph("Fig 10: 'Account Created Successfully'", caption_style)]
    ]
    t_row3 = Table(row3_cells, colWidths=[126, 126, 126, 126])
    t_row3.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
    ]))
    elements.append(t_row3)
    elements.append(Spacer(1, 8))

    elements.append(Paragraph("<b>Kotlin Validation Logic in CreateAccountActivity.kt:</b>", h2_style))
    snippet_text = (
        "// 1. Check empty text fields\n"
        "if (fullName.isEmpty() || studentId.isEmpty() || email.isEmpty() || password.isEmpty() || ...)\n"
        "    Toast.makeText(this, \"Please fill all fields\", Toast.LENGTH_SHORT).show()\n"
        "// 2. Department selected (position > 0)\n"
        "else if (departmentPosition == 0)\n"
        "    Toast.makeText(this, \"Please select department\", Toast.LENGTH_SHORT).show()\n"
        "// 3. Semester selected (position > 0)\n"
        "else if (semesterPosition == 0)\n"
        "    Toast.makeText(this, \"Please select semester\", Toast.LENGTH_SHORT).show()\n"
        "// 4. Passwords match\n"
        "else if (password != confirmPassword)\n"
        "    Toast.makeText(this, \"Passwords do not match\", Toast.LENGTH_SHORT).show()\n"
        "// 5. Success -> Intent to LoginActivity with student name\n"
        "else {\n"
        "    Toast.makeText(this, \"Account Created Successfully\", Toast.LENGTH_SHORT).show()\n"
        "    val intent = Intent(this, LoginActivity::class.java).apply { putExtra(EXTRA_STUDENT_NAME, fullName) }\n"
        "    startActivity(intent)\n"
        "}"
    )
    snippet_table = Table([[Paragraph(snippet_text.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)]], colWidths=[504])
    snippet_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(snippet_table)

    # ================= PAGE 5 =================
    elements.append(PageBreak())
    elements.append(Paragraph("5. Screen 2 — Login (LinearLayout & Intent Integration)", h1_style))
    elements.append(Paragraph(
        "Screen 2 is created entirely using <b>LinearLayout</b> with <code>android:orientation=\"vertical\"</code>. "
        "Upon successful registration, it receives the student's name from Screen 1 using <code>Intent.getStringExtra()</code> "
        "and dynamically updates the welcome header to: <b>Welcome, Muhammad Ali!</b>",
        body_style
    ))

    s2_main = optimize_image("screen2_login.png")
    s2_val_empty = optimize_image("screen2_validation_empty.png")
    s2_val_success = optimize_image("screen2_success_toast.png")

    s2_img_w, s2_img_h = 145, 305
    row4_cells = [
        [Image(s2_main, width=s2_img_w, height=s2_img_h), Image(s2_val_empty, width=s2_img_w, height=s2_img_h), Image(s2_val_success, width=s2_img_w, height=s2_img_h)],
        [Paragraph("Fig 11: 'Welcome, Muhammad Ali!'", caption_style), Paragraph("Fig 12: 'Please enter Student ID and Password'", caption_style), Paragraph("Fig 13: 'Login Successful'", caption_style)]
    ]
    t_row4 = Table(row4_cells, colWidths=[168, 168, 168])
    t_row4.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
    ]))
    elements.append(t_row4)
    elements.append(Spacer(1, 6))

    elements.append(Paragraph("<b>Intent Handling & Login Validation in LoginActivity.kt:</b>", h2_style))
    s2_snippet = (
        "// Extract student name from registration Intent\n"
        "val studentName = intent.getStringExtra(CreateAccountActivity.EXTRA_STUDENT_NAME)\n"
        "tvWelcomeMessage.text = if (!studentName.isNullOrBlank()) \"Welcome, $studentName!\" else \"Welcome!\"\n\n"
        "// Login Button Validation\n"
        "btnLogin.setOnClickListener {\n"
        "    val studentId = etLoginStudentId.text.toString().trim()\n"
        "    val password = etLoginPassword.text.toString().trim()\n"
        "    if (studentId.isEmpty() || password.isEmpty())\n"
        "        Toast.makeText(this, \"Please enter Student ID and Password\", Toast.LENGTH_SHORT).show()\n"
        "    else\n"
        "        Toast.makeText(this, \"Login Successful\", Toast.LENGTH_SHORT).show()\n"
        "}"
    )
    s2_table = Table([[Paragraph(s2_snippet.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)]], colWidths=[504])
    s2_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(s2_table)
    elements.append(Spacer(1, 6))

    elements.append(Paragraph(
        f"<b>Submission Verification Link:</b> All code and the compiled APK are live at "
        f"<a href='{GITHUB_REPO_URL}'><b><u>{GITHUB_REPO_URL}</u></b></a>. "
        f"The APK file <code>Student_Learning_Portal.apk</code> is available at the repository root.",
        body_style
    ))

    doc.build(elements, canvasmaker=NumberedCanvas)
    size_bytes = os.path.getsize(PDF_OUTPUT)
    print("PDF build complete:", PDF_OUTPUT)
    print(f"PDF file size: {size_bytes} bytes ({size_bytes / 1024:.1f} KB / {size_bytes / (1024*1024):.2f} MB)")

    # Also copy to a shorter name for convenience
    short_output = os.path.join(BASE_DIR, "Student_Learning_Portal_Assignment.pdf")
    with open(PDF_OUTPUT, "rb") as f_in, open(short_output, "wb") as f_out:
        f_out.write(f_in.read())

if __name__ == "__main__":
    build_pdf()
