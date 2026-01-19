import streamlit as st
import pandas as pd
import re
import json
import os
from streamlit_option_menu import option_menu

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CPC Club Contest Spring 2026",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- FILE STORAGE SYSTEM (PERSISTENCE) ---
DB_FILE = "users.json"

def load_data():
    """Load users from the JSON file."""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_data(data):
    """Save users to the JSON file."""
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- SESSION STATE INITIALIZATION ---
if 'users' not in st.session_state:
    st.session_state['users'] = load_data()  # Load from file on startup

if 'logged_in_user' not in st.session_state:
    st.session_state['logged_in_user'] = None

# --- CONSTANTS ---
ADMIN_PASSWORD = "891011"
BKASH_NUMBER = "01346561010"

# --- HELPER FUNCTIONS ---
def validate_email(email):
    return email.endswith("@diu.edu.bd")

def validate_student_id(student_id):
    # Format: xxx-xx-xxx
    pattern = r"^\d{3}-\d{2}-\d{3,4}$"
    return re.match(pattern, student_id)

def login_user(email, password):
    email = email.strip().lower() # Remove spaces & make lowercase
    password = password.strip()
    
    # Reload data to ensure we have the latest registrations
    st.session_state['users'] = load_data()
    
    if email in st.session_state['users']:
        if st.session_state['users'][email]['password'] == password:
            st.session_state['logged_in_user'] = email
            return True
    return False

def register_user(email, password, name):
    email = email.strip().lower() # Remove spaces & make lowercase
    password = password.strip()
    name = name.strip()
    
    # Reload data first
    st.session_state['users'] = load_data()
    
    if email in st.session_state['users']:
        return False
        
    st.session_state['users'][email] = {
        'password': password,
        'name': name,
        'id': None,
        'payment_status': 'Not Registered',
        'trx_id': None,
        'bio': 'Coding enthusiast ready to win!',
        'pfp': None # Note: Images cannot be saved to JSON easily, bio will save.
    }
    save_data(st.session_state['users']) # Save to file immediately
    return True

def update_user_data(email, key, value):
    st.session_state['users'][email][key] = value
    save_data(st.session_state['users']) # Save changes

# --- MAIN APP LOGIC ---

# 1. SIDEBAR NAVIGATION
with st.sidebar:
    st.title("Navigation")
    admin_access = st.checkbox("Admin Mode (Restricted)", value=False)
    
    if st.session_state['logged_in_user']:
        curr_user = st.session_state['users'].get(st.session_state['logged_in_user'])
        if curr_user:
            st.write(f"Logged in as: **{curr_user['name']}**")
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
        
        # Reload latest data
        all_users = load_data()
        
        data = []
        for email, info in all_users.items():
            if info.get('payment_status') != 'Not Registered':
                data.append({
                    "Name": info['name'],
                    "Student ID": info['id'],
                    "Email": email,
                    "Transaction ID": info['trx_id'],
                    "Status": info['payment_status']
                })
        
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df) # Display data
            
            st.write("### Approve Payment")
            pending_users = [d['Email'] for d in data if d['Status'] == 'Pending']
            
            if pending_users:
                user_to_approve = st.selectbox("Select User to Approve", pending_users)
                if st.button("Approve Selected User"):
                    all_users[user_to_approve]['payment_status'] = "Approved"
                    save_data(all_users) # Save to file
                    st.session_state['users'] = all_users # Update session
                    st.success(f"Approved {user_to_approve}!")
                    st.rerun()
            else:
                st.info("No pending approvals.")
        else:
            st.write("No registrations yet.")
            
    elif password_input:
        st.error("Wrong Password")
    
    st.stop()

# 3. PUBLIC INTERFACE
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🏆 CPC Club Contest Spring 2026</h1>", unsafe_allow_html=True)
st.markdown("---")

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

# 4. AUTHENTICATION
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
        signup_email = st.text_input("DIU Email", key="signup_email")
        signup_pass = st.text_input("Password", type="password", key="signup_pass")
        
        if st.button("Create Account"):
            if not validate_email(signup_email.strip()):
                st.error("Email must end with @diu.edu.bd")
            elif not signup_name or not signup_pass:
                st.warning("Please fill all fields")
            else:
                if register_user(signup_email, signup_pass, signup_name):
                    st.success("Account created! Go to Login tab.")
                else:
                    st.error("User already exists.")

else:
    # 5. LOGGED IN USER VIEW
    user_email = st.session_state['logged_in_user']
    # Always read fresh from session state which is synced with file
    user_data = st.session_state['users'][user_email]
    
    selected = option_menu(
        menu_title=None,
        options=["Registration", "My Profile", "Status"],
        icons=["pencil-square", "person-circle", "info-circle"],
        orientation="horizontal",
    )
    
    if selected == "Registration":
        st.header(f"Welcome, {user_data['name']}!")
        
        if user_data['payment_status'] == 'Approved':
            st.success("✅ You are fully registered and approved!")
        elif user_data['payment_status'] == 'Pending':
            st.warning("⏳ Your payment is pending Admin approval.")
        else:
            with st.form("reg_form"):
                st.write("### Complete Registration")
                st.text_input("Name", value=user_data['name'], disabled=True)
                student_id = st.text_input("Student ID (Format: xxx-xx-xxx)", placeholder="e.g., 221-15-1234")
                st.write(f"Payment Number (bKash): **{BKASH_NUMBER}**")
                trx_id = st.text_input("Enter bKash Transaction ID")
                
                if st.form_submit_button("Complete Payment"):
                    if not validate_student_id(student_id):
                        st.error("Invalid ID format.")
                    elif not trx_id:
                        st.error("Enter Transaction ID.")
                    else:
                        update_user_data(user_email, 'id', student_id)
                        update_user_data(user_email, 'trx_id', trx_id)
                        update_user_data(user_email, 'payment_status', "Pending")
                        st.success("Submitted! Waiting for Admin.")
                        st.rerun()

    elif selected == "My Profile":
        st.header("My Profile")
        st.write(f"**Name:** {user_data['name']}")
        st.write(f"**Email:** {user_email}")
        
        new_bio = st.text_area("Bio", value=user_data.get('bio', ''))
        if st.button("Update Bio"):
            update_user_data(user_email, 'bio', new_bio)
            st.success("Bio updated!")

    elif selected == "Status":
        st.header("Status")
        status = user_data['payment_status']
        if status == "Approved":
            st.balloons()
            st.success("You are CONFIRMED for the contest!")
        elif status == "Pending":
            st.warning("Admin is reviewing your payment.")
        else:
            st.error("Not registered.")
