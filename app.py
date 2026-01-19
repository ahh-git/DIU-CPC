import streamlit as st
import pandas as pd
import re
import json
import os
from streamlit_option_menu import option_menu

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CPC Spring 2026",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ADVANCED CSS (BEAUTIFICATION) ---
st.markdown("""
<style>
    /* Dark Theme Background */
    .stApp {
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        color: white;
    }
    
    /* Login Card Styling */
    .login-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(4px);
        -webkit-backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        text-align: center;
    }
    
    /* Input Fields Styling */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid #4CAF50;
        border-radius: 10px;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        font-weight: bold;
        border: none;
        padding: 10px 20px;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #45a049;
        transform: scale(1.02);
    }

    /* Prize Cards */
    .prize-card {
        background: rgba(0, 0, 0, 0.3);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #FFD700;
        margin-bottom: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA MANAGER (JSON) ---
DB_FILE = "users.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

if 'users' not in st.session_state:
    st.session_state['users'] = load_data()
if 'logged_in_user' not in st.session_state:
    st.session_state['logged_in_user'] = None

# --- CONSTANTS ---
ADMIN_PASSWORD = "891011"
BKASH_NUMBER = "01346561010"

# --- AUTH FUNCTIONS ---
def login_user(email, password):
    email = email.strip().lower()
    password = password.strip()
    st.session_state['users'] = load_data()
    if email in st.session_state['users']:
        if st.session_state['users'][email]['password'] == password:
            st.session_state['logged_in_user'] = email
            return True
    return False

def register_user(email, password, name):
    email = email.strip().lower()
    if not email.endswith("@diu.edu.bd"):
        return "Invalid Email Domain"
    
    st.session_state['users'] = load_data()
    if email in st.session_state['users']:
        return "User Exists"
        
    st.session_state['users'][email] = {
        'password': password.strip(),
        'name': name.strip(),
        'id': None,
        'payment_status': 'Incomplete', 
        'trx_id': None,
        'bio': '',
        'pfp': None
    }
    save_data(st.session_state['users'])
    return "Success"

def update_user_data(email, key, value):
    st.session_state['users'][email][key] = value
    save_data(st.session_state['users'])

# =========================================================
#  SECTION 1: LOGIN PAGE (The Gatekeeper)
# =========================================================
if st.session_state['logged_in_user'] is None:
    
    # Center Layout using Columns
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True) # Spacing
        st.markdown("""
        <div class='login-container'>
            <h1>🏆 CPC Spring 2026</h1>
            <p>Welcome to the Ultimate Coding Battle</p>
            <p style='font-size: 0.8rem; color: gray;'>Please Login to Access Contest Details</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab_login, tab_signup = st.tabs(["🔐 Login", "📝 Sign Up"])
        
        with tab_login:
            l_email = st.text_input("DIU Email", key="l_email", placeholder="student@diu.edu.bd")
            l_pass = st.text_input("Password", type="password", key="l_pass")
            if st.button("ENTER CONTEST"):
                if login_user(l_email, l_pass):
                    st.rerun()
                else:
                    st.error("Invalid Email or Password")
        
        with tab_signup:
            s_name = st.text_input("Full Name", placeholder="Nazmus Shakib")
            s_email = st.text_input("DIU Email", key="s_email", placeholder="xxx@diu.edu.bd")
            s_pass = st.text_input("Create Password", type="password", key="s_pass")
            if st.button("CREATE ACCOUNT"):
                result = register_user(s_email, s_pass, s_name)
                if result == "Success":
                    st.success("Account Created! Please Login now.")
                elif result == "Invalid Email Domain":
                    st.error("Only @diu.edu.bd emails allowed!")
                else:
                    st.error("User already exists.")

# =========================================================
#  SECTION 2: MAIN DASHBOARD (Only for Logged In Users)
# =========================================================
else:
    user_email = st.session_state['logged_in_user']
    user = st.session_state['users'][user_email]

    # --- Sidebar Admin Toggle ---
    with st.sidebar:
        st.title("Settings")
        if st.checkbox("Admin Mode"):
            pwd = st.text_input("Admin Key", type="password")
            if pwd == ADMIN_PASSWORD:
                st.success("Admin Unlocked")
                # Admin Logic
                all_data = load_data()
                df = pd.DataFrame(all_data).T
                st.dataframe(df)
                
                # Simple Approve System
                to_approve = st.text_input("Paste Email to Approve")
                if st.button("Approve Payment"):
                    if to_approve in all_data:
                        all_data[to_approve]['payment_status'] = 'Approved'
                        save_data(all_data)
                        st.session_state['users'] = all_data
                        st.success("Approved!")
            else:
                st.warning("Restricted Access")

        if st.button("Logout", type="secondary"):
            st.session_state['logged_in_user'] = None
            st.rerun()

    # --- Header ---
    st.markdown(f"### 👋 Welcome, **{user['name']}**")
    
    # --- Navigation Menu ---
    selected = option_menu(
        menu_title=None,
        options=["Contest Info", "Registration", "My Profile"],
        icons=["trophy", "pencil-square", "person-circle"],
        orientation="horizontal",
        styles={"nav-link-selected": {"background-color": "#4CAF50"}}
    )

    # --- TAB 1: CONTEST INFO ---
    if selected == "Contest Info":
        st.markdown("<h1 style='text-align: center;'>🏆 CPC Club Contest Spring 2026</h1>", unsafe_allow_html=True)
        st.divider()
        
        # Prize Grid
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("<div class='prize-card'><h3>🥇 1st Place</h3><h1>5,000 ৳</h1></div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='prize-card'><h3>🥈 2nd Place</h3><h1>2,500 ৳</h1></div>", unsafe_allow_html=True)
        with c3:
            st.markdown("<div class='prize-card'><h3>🥉 3rd Place</h3><h1>1,000 ৳</h1></div>", unsafe_allow_html=True)
            
        st.info("🎁 **Bonus:** All participants get a Free Jersey, Lunch & Surprise Gift!")

    # --- TAB 2: REGISTRATION (With Payment Popup Flow) ---
    elif selected == "Registration":
        st.header("📝 Contest Registration")
        
        # STATUS CHECKER
        status = user.get('payment_status', 'Incomplete')
        
        if status == "Approved":
            st.success("✅ REGISTRATION COMPLETE")
            st.balloons()
            st.markdown("### You are all set for the contest!")
            st.write(f"**Student ID:** {user.get('id')}")
            st.write(f"**Transaction ID:** {user.get('trx_id')}")
            
        elif status == "Pending":
            st.warning("⏳ Payment Under Review")
            st.write("We have received your request. Admin will approve it shortly.")
            
        else:
            # INTERACTIVE FLOW
            # Step 1: Check if Student ID is missing
            if not user['id']:
                with st.form("step1_form"):
                    st.subheader("Step 1: Student Details")
                    sid = st.text_input("Enter Student ID", placeholder="xxx-xx-xxx")
                    if st.form_submit_button("Continue to Payment ➡️"):
                        if re.match(r"^\d{3}-\d{2}-\d{3,4}$", sid):
                            update_user_data(user_email, 'id', sid)
                            st.rerun()
                        else:
                            st.error("Invalid ID Format (Use: xxx-xx-xxx)")
            
            # Step 2: Payment "Popup" (Conditional Render)
            else:
                st.markdown("""
                <div style='background-color: #1a2526; padding: 20px; border-radius: 10px; border: 1px solid #4CAF50;'>
                    <h3 style='color: #4CAF50;'>💸 Payment Gateway</h3>
                    <p>Please send registration fee to <strong>bKash Personal</strong></p>
                    <h2 style='text-align: center; color: white;'>01346561010</h2>
                </div>
                <br>
                """, unsafe_allow_html=True)
                
                with st.form("payment_form"):
                    trx = st.text_input("Enter bKash Transaction ID (TrxID)")
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        # Back Button Logic
                        if st.form_submit_button("⬅️ Back"):
                             # Hack to clear ID to go back, or just handle navigation
                             pass 
                    with c2:
                        submit_pay = st.form_submit_button("Confirm Payment ✅")
                    
                    if submit_pay:
                        if len(trx) > 5:
                            update_user_data(user_email, 'trx_id', trx)
                            update_user_data(user_email, 'payment_status', 'Pending')
                            st.success("Payment Sent! Wait for approval.")
                            st.rerun()
                        else:
                            st.error("Invalid TrxID")

    # --- TAB 3: PROFILE ---
    elif selected == "My Profile":
        c1, c2 = st.columns([1, 3])
        with c1:
            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=150)
        with c2:
            st.title(user['name'])
            st.write(f"📧 {user_email}")
            st.write(f"🆔 {user.get('id', 'Not Set')}")
            
            st.markdown("---")
            bio = st.text_area("About Me", value=user.get('bio', ''))
            if st.button("Save Profile"):
                update_user_data(user_email, 'bio', bio)
                st.success("Profile Updated")
