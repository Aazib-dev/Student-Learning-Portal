package com.example.studentlearningportal

import android.app.DatePickerDialog
import android.content.Intent
import android.os.Bundle
import android.widget.EditText
import android.widget.Spinner
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.widget.AppCompatButton
import java.util.Calendar
import java.util.Locale

/**
 * Screen 1: Create Account
 *
 * Implements the student registration interface designed with RelativeLayout.
 * Handles user input, date picking via DatePickerDialog, form validations,
 * and navigation to LoginActivity with student details passed via Intent.
 */
class CreateAccountActivity : AppCompatActivity() {

    private lateinit var etFullName: EditText
    private lateinit var etStudentId: EditText
    private lateinit var etEmail: EditText
    private lateinit var etPassword: EditText
    private lateinit var etConfirmPassword: EditText
    private lateinit var spinnerDepartment: Spinner
    private lateinit var spinnerSemester: Spinner
    private lateinit var etDateOfAdmission: EditText
    private lateinit var btnCreateAccount: AppCompatButton
    private lateinit var tvAlreadyAccount: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_create_account)

        initializeViews()
        setupDatePicker()
        setupListeners()
    }

    /**
     * Bind view references from the RelativeLayout layout.
     */
    private fun initializeViews() {
        etFullName = findViewById(R.id.etFullName)
        etStudentId = findViewById(R.id.etStudentId)
        etEmail = findViewById(R.id.etEmail)
        etPassword = findViewById(R.id.etPassword)
        etConfirmPassword = findViewById(R.id.etConfirmPassword)
        spinnerDepartment = findViewById(R.id.spinnerDepartment)
        spinnerSemester = findViewById(R.id.spinnerSemester)
        etDateOfAdmission = findViewById(R.id.etDateOfAdmission)
        btnCreateAccount = findViewById(R.id.btnCreateAccount)
        tvAlreadyAccount = findViewById(R.id.tvAlreadyAccount)
    }

    /**
     * Displays a DatePickerDialog when the admission date field is clicked,
     * formatting the chosen date into dd/MM/yyyy.
     */
    private fun setupDatePicker() {
        val calendar = Calendar.getInstance()

        etDateOfAdmission.setOnClickListener {
            val year = calendar.get(Calendar.YEAR)
            val month = calendar.get(Calendar.MONTH)
            val day = calendar.get(Calendar.DAY_OF_MONTH)

            val datePickerDialog = DatePickerDialog(
                this,
                { _, selectedYear, selectedMonth, selectedDay ->
                    val formattedDate = String.format(
                        Locale.getDefault(),
                        "%02d/%02d/%04d",
                        selectedDay,
                        selectedMonth + 1,
                        selectedYear
                    )
                    etDateOfAdmission.setText(formattedDate)
                },
                year,
                month,
                day
            )
            datePickerDialog.show()
        }
    }

    /**
     * Attach click listeners for account creation and login navigation.
     */
    private fun setupListeners() {
        btnCreateAccount.setOnClickListener {
            handleCreateAccount()
        }

        tvAlreadyAccount.setOnClickListener {
            val intent = Intent(this, LoginActivity::class.java)
            startActivity(intent)
        }
    }

    /**
     * Validates all input fields according to assignment requirements:
     * 1. Empty fields -> "Please fill all fields"
     * 2. Department not selected -> "Please select department"
     * 3. Semester not selected -> "Please select semester"
     * 4. Password mismatch -> "Passwords do not match"
     * 5. Success -> "Account Created Successfully" and navigate to Login with Intent.
     */
    private fun handleCreateAccount() {
        val fullName = etFullName.text.toString().trim()
        val studentId = etStudentId.text.toString().trim()
        val email = etEmail.text.toString().trim()
        val password = etPassword.text.toString().trim()
        val confirmPassword = etConfirmPassword.text.toString().trim()
        val dateOfAdmission = etDateOfAdmission.text.toString().trim()

        val departmentPosition = spinnerDepartment.selectedItemPosition
        val semesterPosition = spinnerSemester.selectedItemPosition

        // Validation 1: Check if any required field is empty
        if (fullName.isEmpty() ||
            studentId.isEmpty() ||
            email.isEmpty() ||
            password.isEmpty() ||
            confirmPassword.isEmpty() ||
            dateOfAdmission.isEmpty()
        ) {
            Toast.makeText(this, getString(R.string.msg_empty_fields), Toast.LENGTH_SHORT).show()
            return
        }

        // Validation 2: Check if Department is selected (index 0 is "Select Department")
        if (departmentPosition == 0) {
            Toast.makeText(this, getString(R.string.msg_select_department), Toast.LENGTH_SHORT).show()
            return
        }

        // Validation 3: Check if Semester is selected (index 0 is "Select Semester")
        if (semesterPosition == 0) {
            Toast.makeText(this, getString(R.string.msg_select_semester), Toast.LENGTH_SHORT).show()
            return
        }

        // Validation 4: Check if Password and Confirm Password match
        if (password != confirmPassword) {
            Toast.makeText(this, getString(R.string.msg_passwords_mismatch), Toast.LENGTH_SHORT).show()
            return
        }

        // Validation 5: All checks passed
        Toast.makeText(this, getString(R.string.msg_account_created), Toast.LENGTH_SHORT).show()

        // Navigate to LoginActivity passing the student's full name via Intent
        val intent = Intent(this, LoginActivity::class.java).apply {
            putExtra(EXTRA_STUDENT_NAME, fullName)
        }
        startActivity(intent)
    }

    companion object {
        const val EXTRA_STUDENT_NAME = "extra_student_name"
    }
}
