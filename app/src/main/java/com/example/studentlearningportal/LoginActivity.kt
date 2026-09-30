package com.example.studentlearningportal

import android.content.Intent
import android.os.Bundle
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.widget.AppCompatButton

/**
 * Screen 2: Login
 *
 * Implements the student login interface designed with LinearLayout.
 * Receives the registered student name via Intent to display a personalized
 * welcome message, validates credentials, and confirms successful login.
 */
class LoginActivity : AppCompatActivity() {

    private lateinit var tvWelcomeMessage: TextView
    private lateinit var etLoginStudentId: EditText
    private lateinit var etLoginPassword: EditText
    private lateinit var btnLogin: AppCompatButton
    private lateinit var tvBackToSignup: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        initializeViews()
        displayPersonalizedWelcome()
        setupListeners()
    }

    /**
     * Bind view references from the LinearLayout layout.
     */
    private fun initializeViews() {
        tvWelcomeMessage = findViewById(R.id.tvWelcomeMessage)
        etLoginStudentId = findViewById(R.id.etLoginStudentId)
        etLoginPassword = findViewById(R.id.etLoginPassword)
        btnLogin = findViewById(R.id.btnLogin)
        tvBackToSignup = findViewById(R.id.tvBackToSignup)
    }

    /**
     * Extracts student name passed via Intent from CreateAccountActivity
     * and displays "Welcome, <Student Name>!".
     */
    private fun displayPersonalizedWelcome() {
        val studentName = intent.getStringExtra(CreateAccountActivity.EXTRA_STUDENT_NAME)
        if (!studentName.isNullOrBlank()) {
            tvWelcomeMessage.text = getString(R.string.welcome_student_name, studentName)
        } else {
            tvWelcomeMessage.text = getString(R.string.welcome_default)
        }
    }

    /**
     * Sets up click listeners for the Login button and navigation back to Signup.
     */
    private fun setupListeners() {
        btnLogin.setOnClickListener {
            handleLogin()
        }

        tvBackToSignup.setOnClickListener {
            // Finish this activity or navigate back to registration
            val intent = Intent(this, CreateAccountActivity::class.java)
            intent.flags = Intent.FLAG_ACTIVITY_CLEAR_TOP or Intent.FLAG_ACTIVITY_SINGLE_TOP
            startActivity(intent)
            finish()
        }
    }

    /**
     * Validates student ID and password:
     * - If either is empty: displays "Please enter Student ID and Password"
     * - Otherwise: displays "Login Successful"
     */
    private fun handleLogin() {
        val studentId = etLoginStudentId.text.toString().trim()
        val password = etLoginPassword.text.toString().trim()

        if (studentId.isEmpty() || password.isEmpty()) {
            Toast.makeText(
                this,
                getString(R.string.msg_login_empty_fields),
                Toast.LENGTH_SHORT
            ).show()
        } else {
            Toast.makeText(
                this,
                getString(R.string.msg_login_success),
                Toast.LENGTH_SHORT
            ).show()
        }
    }
}
