import streamlit as st
import pandas as pd
import re
import time
from streamlit_option_menu import option_menu

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CPC Club Contest Spring 2026",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- SESSION STATE MANAGEMENT ---
# We use session state to simulate a database for this example.
if 'users' not in st.session_state:
    st.session_state['users'] = {}  # {email: {'password': pw, 'name': name, 'id': id, 'payment_status': 'Pending', 'trx_id': '', 'bio': '', 'pfp': None}}
if 'logged_in_user' not in st.session_state:
    st.session_state['logged_in_user'] = None
if 'registrations' not in st.session_state:
    st.session_state['registrations'] = []

# --- CONSTANTS ---
ADMIN_PASSWORD = "891011"
BKASH_NUMBER = "01346561010"

# --- HELPER FUNCTIONS ---
def validate_email(email):
    return email.endswith("@diu.edu.bd")

def validate_student_id(student_id):
    # Format: xxx-xx-xxx (e.g., 221-15-123)
    pattern = r"^\d{3}-\d{2}-\d{3,4}$"
    return re.match(pattern, student_id)

def login_user(email, password):
    if email in st.session_state['users']:
        if st.session_state['users'][email]['password'] == password:
            st.session_state['logged_in_user'] = email
            return True
    return False

def register_user(email, password, name):
    if email in st.session_state['users']:
        return False
    st.session_state['users'][email] = {
        'password': password,
        'name': name,
        'id': None,
        'payment_status': 'Not Registered',
        'trx_id': None,
        'bio': 'Coding enthusiast ready to win!',
        'pfp': None
    }
    return True

# --- MAIN APP LOGIC ---

# 1. SIDEBAR NAVIGATION (Hidden logic for Admin)
with st.sidebar:
    st.title("Navigation")
    # Secret Admin Access: Using a checkbox to simulate 'double tap' or hidden toggle
    admin_access = st.checkbox("Admin Mode (Restricted)", value=False)
    
    if st.session_state['logged_in_user']:
        st.write(f"Logged in as: **{st.session_state['users'][st.session_state['logged_in_user']]['name']}**")
        if st.button("Logout"):
            st.session_state['logged_in_user'] = None
            st.rerun()

# 2. ADMIN PANEL
if admin_access:
    st.title("🔒 Admin Panel")
    password_input = st.text_input("Enter Admin Password", type="password")
    
    if password_input == ADMIN_PASSWORD:
        st.success("Access Granted")
        st.subheader("Registered Participants Data")
        
        # Convert session state data to DataFrame for display
        data = []
        for email, info in st.session_state['users'].items():
            if info['payment_status'] != 'Not Registered':
                data.append({
                    "Name": info['name'],
                    "Student ID": info['id'],
                    "Email": email,
                    "Transaction ID": info['trx_id'],
                    "Status": info['payment_status']
                })
        
        if data:
            df = pd.DataFrame(data)
            edited_df = st.data_editor(df, num_rows="dynamic", key="admin_editor")
            
            # Button to approve payments (Simulated logic)
            st.info("To approve a user, manually note their ID. (In a real DB, you'd click a button row-wise)")
            
            participant_to_approve = st.selectbox("Select Participant to Approve", [d['Email'] for d in data if d['Status'] == 'Pending'])
            if st.button("Approve Payment"):
                st.session_state['users'][participant_to_approve]['payment_status'] = "Approved"
                st.success(f"Approved {participant_to_approve}!")
                st.rerun()
        else:
            st.write("No registrations yet.")
            
    elif password_input:
        st.error("Wrong Password")
    
    st.stop() # Stop further execution if in Admin mode

# 3. PUBLIC INTERFACE
# Header & Info
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🏆 CPC Club Contest Spring 2026</h1>", unsafe_allow_html=True)
st.markdown("---")

# Event Info Section
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎉 Prize Pool")
    st.markdown("""
    * 🥇 **1st Place:** BDT 5,000
    * 🥈 **2nd Place:** BDT 2,500
    * 🥉 **3rd Place:** BDT 1,000
    * 🏅 **Top 20:** Exclusive Certificates
    """)

with col2:
    st.subheader("🎁 All Participants Get")
    st.markdown("""
    * 👕 **Free Jersey**
    * 🍱 **Free Lunch**
    * 🎁 **Surprise Gift**
    """)

st.markdown("---")

# 4. AUTHENTICATION & REGISTRATION
if st.session_state['logged_in_user'] is None:
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Login")
        login_email = st.text_input("DIU Email", key="login_email")
        login_pass = st.text_input("Password", type="password", key="login_pass")
        if st.button("Sign In"):
            if login_user(login_email, login_pass):
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid email or password.")

    with tab2:
        st.subheader("Sign Up")
        st.info("Only @diu.edu.bd emails are allowed.")
        signup_name = st.text_input("Full Name")
        signup_email = st.text_input("DIU Email (ends with @diu.edu.bd)", key="signup_email")
        signup_pass = st.text_input("Password", type="password", key="signup_pass")
        
        if st.button("Create Account"):
            if not validate_email(signup_email):
                st.error("Email must end with @diu.edu.bd")
            elif not signup_name or not signup_pass:
                st.warning("Please fill all fields")
            else:
                if register_user(signup_email, signup_pass, signup_name):
                    st.success("Account created! Please login.")
                else:
                    st.error("User already exists.")

else:
    # 5. LOGGED IN USER VIEW
    user_email = st.session_state['logged_in_user']
    user_data = st.session_state['users'][user_email]
    
    # Navigation Menu
    selected = option_menu(
        menu_title=None,
        options=["Registration", "My Profile", "Status"],
        icons=["pencil-square", "person-circle", "info-circle"],
        orientation="horizontal",
    )
    
    # -- Registration Section --
    if selected == "Registration":
        st.header(f"Welcome, {user_data['name']}!")
        
        if user_data['payment_status'] == 'Approved':
            st.success("✅ You are fully registered and approved!")
        elif user_data['payment_status'] == 'Pending':
            st.warning("⏳ Your payment is pending Admin approval.")
        else:
            st.write("Please complete the form below to register for the contest.")
            
            with st.form("reg_form"):
                st.write("### Step 1: Student Details")
                # Auto-fill name
                st.text_input("Name", value=user_data['name'], disabled=True)
                student_id = st.text_input("Student ID (Format: xxx-xx-xxx)", placeholder="e.g., 221-15-1234")
                
                st.write("### Step 2: Payment")
                st.write(f"Please Send Payment to bKash Personal: **{BKASH_NUMBER}**")
                trx_id = st.text_input("Enter bKash Transaction ID")
                
                submitted = st.form_submit_button("Complete Payment")
                
                if submitted:
                    if not validate_student_id(student_id):
                        st.error("Invalid Student ID format. Use xxx-xx-xxx.")
                    elif not trx_id:
                        st.error("Please enter Transaction ID.")
                    else:
                        # Update User Data
                        st.session_state['users'][user_email]['id'] = student_id
                        st.session_state['users'][user_email]['trx_id'] = trx_id
                        st.session_state['users'][user_email]['payment_status'] = "Pending"
                        st.success("Registration Submitted! Waiting for Admin Approval.")
                        st.rerun()

    # -- Profile Section --
    elif selected == "My Profile":
        st.header("My Profile")
        
        col_p1, col_p2 = st.columns([1, 3])
        
        with col_p1:
            if user_data.get('pfp'):
                st.image(user_data['pfp'], width=150, caption="Profile Picture")
            else:
                st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=150)
            
            uploaded_file = st.file_uploader("Update PFP", type=['png', 'jpg', 'jpeg'])
            if uploaded_file is not None:
                st.session_state['users'][user_email]['pfp'] = uploaded_file
                st.rerun()

        with col_p2:
            st.subheader(user_data['name'])
            st.write(f"**Email:** {user_email}")
            st.write(f"**Student ID:** {user_data['id'] if user_data['id'] else 'Not set'}")
            
            new_bio = st.text_area("Bio", value=user_data.get('bio', ''))
            if st.button("Update Bio"):
                st.session_state['users'][user_email]['bio'] = new_bio
                st.success("Bio updated!")

    # -- Status Section --
    elif selected == "Status":
        st.header("Participation Status")
        status = user_data['payment_status']
        
        if status == "Approved":
            st.success("🎉 CONGRATULATIONS! You are officially a participant.")
            st.balloons()
            st.metric(label="Contest Date", value="Spring 2026")
            st.info("Don't forget to collect your Jersey and Lunch token at the venue!")
        elif status == "Pending":
            st.warning("Your payment is currently under review by the Admin.")
            st.write(f"**Transaction ID Submitted:** {user_data['trx_id']}")
        else:
            st.error("You have not registered yet.")
            st.write("Go to the **Registration** tab to join.")
