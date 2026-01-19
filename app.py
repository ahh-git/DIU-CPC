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

# --- CUSTOM CSS (BETTER UI) ---
st.markdown("""
<style>
    /* Main Background & Fonts */
    .stApp {
        background-color: #0e1117;
    }
    h1, h2, h3 {
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Custom Cards for Prizes */
    .prize-card {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin-bottom: 10px;
    }
    .prize-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #e5e7eb;
    }
    .prize-amount {
        font-size: 1.5rem;
        font-weight: bold;
        color: #4CAF50;
    }
    
    /* Status Badges */
    .status-badge {
        padding: 5px 10px;
        border-radius: 5px;
        font-weight: bold;
        color: white;
    }
    .status-pending { background-color: #f59e0b; }
    .status-approved { background-color: #10b981; }
    .status-incomplete { background-color: #ef4444; }
</style>
""", unsafe_allow_html=True)

# --- FILE STORAGE SYSTEM ---
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

# --- HELPER FUNCTIONS ---
def validate_email(email):
    return email.endswith("@diu.edu.bd")

def validate_student_id(student_id):
    return re.match(r"^\d{3}-\d{2}-\d{3,4}$", student_id)

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
    password = password.strip()
    st.session_state['users'] = load_data()
    if email in st.session_state['users']:
        return False
    st.session_state['users'][email] = {
        'password': password,
        'name': name,
        'id': None,
        'payment_status': 'Incomplete', # Changed default status
        'trx_id': None,
        'bio': 'Ready to code!',
        'pfp': None
    }
    save_data(st.session_state['users'])
    return True

def update_user_data(email, key, value):
    st.session_state['users'][email][key] = value
    save_data(st.session_state['users'])

# --- SIDEBAR & ADMIN ---
with st.sidebar:
    st.title("🔧 Settings")
    admin_access = st.checkbox("Admin Mode", value=False)
    if st.session_state['logged_in_user']:
        if st.button("Logout", type="primary"):
            st.session_state['logged_in_user'] = None
            st.rerun()

if admin_access:
    st.title("🔒 Admin Panel")
    if st.text_input("Password", type="password") == ADMIN_PASSWORD:
        st.success("Access Granted")
        all_users = load_data()
        
        # Metrics
        total = len(all_users)
        approved = len([u for u in all_users.values() if u['payment_status'] == 'Approved'])
        pending = len([u for u in all_users.values() if u['payment_status'] == 'Pending'])
        
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Total Users", total)
        col_b.metric("Approved", approved)
        col_c.metric("Pending", pending)
        
        # Table
        data = []
        for email, info in all_users.items():
            data.append({
                "Name": info['name'],
                "ID": info['id'],
                "TrxID": info['trx_id'],
                "Status": info['payment_status'],
                "Email": email
            })
        st.dataframe(pd.DataFrame(data))
        
        # Action
        pending_users = [d['Email'] for d in data if d['Status'] == 'Pending']
        if pending_users:
            u_approve = st.selectbox("Select User to Approve", pending_users)
            if st.button("Approve User"):
                all_users[u_approve]['payment_status'] = "Approved"
                save_data(all_users)
                st.session_state['users'] = all_users
                st.success(f"Approved {u_approve}!")
                st.rerun()
    st.stop()

# --- MAIN UI ---
if st.session_state['logged_in_user'] is None:
    # LANDING PAGE UI
    st.markdown("<h1 style='text-align: center; color: #4CAF50; font-size: 3rem;'>🏆 CPC Spring 2026</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>The Ultimate Coding Showdown at DIU</p>", unsafe_allow_html=True)
    st.divider()

    # Prize Grid
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="prize-card">
            <div class="prize-title">🥇 1st Place</div>
            <div class="prize-amount">BDT 5,000</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="prize-card">
            <div class="prize-title">🥈 2nd Place</div>
            <div class="prize-amount">BDT 2,500</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="prize-card">
            <div class="prize-title">🥉 3rd Place</div>
            <div class="prize-amount">BDT 1,000</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Auth Tabs
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
    with tab1:
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            email = st.text_input("DIU Email", key="l_email")
            pwd = st.text_input("Password", type="password", key="l_pwd")
            if st.button("Login Now", use_container_width=True):
                if login_user(email, pwd):
                    st.rerun()
                else:
                    st.error("Invalid credentials")
    with tab2:
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            s_name = st.text_input("Full Name")
            s_email = st.text_input("DIU Email (@diu.edu.bd)", key="s_email")
            s_pwd = st.text_input("Password", type="password", key="s_pwd")
            if st.button("Create Account", use_container_width=True):
                if register_user(s_email, s_pwd, s_name):
                    st.success("Account Created! Please Login.")
                else:
                    st.error("Error creating account.")

else:
    # LOGGED IN DASHBOARD
    user_email = st.session_state['logged_in_user']
    user = st.session_state['users'][user_email]
    
    # Custom Menu
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Registration", "Payment", "My Profile"],
        icons=["speedometer2", "pencil-square", "credit-card", "person-circle"],
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#1f2937"},
            "icon": {"color": "orange", "font-size": "18px"}, 
            "nav-link": {"font-size": "15px", "text-align": "center", "margin":"0px", "--hover-color": "#374151"},
            "nav-link-selected": {"background-color": "#4CAF50"},
        }
    )
    
    if selected == "Dashboard":
        st.subheader(f"👋 Hello, {user['name']}")
        
        # Status Logic
        status = user['payment_status']
        if status == "Approved":
            st.success("You are officially registered for the contest! 🎉")
            st.image("https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExcjR6d3J6bmY1cnZ6bmY1cnZ6bmY1cnZ6bmY1cnZ6bmY1cnZ6bmY1cnZ6bmY1/26u4lOMA8JKSnL9Uk/giphy.gif", width=300)
        elif status == "Pending":
            st.warning("Payment Submitted. Waiting for Admin Approval. ⏳")
        elif status == "Registered":
            st.info("Step 1 Complete. Please go to the 'Payment' tab to finalize. 💸")
        else:
            st.error("Registration Incomplete. Go to 'Registration' tab. 📝")

        st.write("### Contest Details")
        st.write("📅 **Date:** Spring 2026")
        st.write("📍 **Venue:** DIU Permanent Campus")
        
    elif selected == "Registration":
        st.header("Step 1: Student Details")
        
        if user['id']:
            st.success(f"✅ Student ID Saved: {user['id']}")
            st.info("You can now proceed to the **Payment** page.")
        else:
            with st.form("id_form"):
                sid = st.text_input("Enter Student ID (xxx-xx-xxx)")
                if st.form_submit_button("Save Details"):
                    if validate_student_id(sid):
                        update_user_data(user_email, 'id', sid)
                        # Only update status if they haven't paid yet
                        if user['payment_status'] == 'Incomplete':
                            update_user_data(user_email, 'payment_status', 'Registered')
                        st.success("Saved! Go to Payment tab.")
                        st.rerun()
                    else:
                        st.error("Invalid ID Format.")

    elif selected == "Payment":
        st.header("Step 2: Payment Gateway")
        
        # Gatekeeper: Must have ID first
        if not user['id']:
            st.error("⚠️ Please complete the 'Registration' tab first!")
            st.stop()
            
        if user['payment_status'] in ['Pending', 'Approved']:
            st.info(f"Payment Status: **{user['payment_status']}**")
            st.write(f"Transaction ID: `{user['trx_id']}`")
        else:
            c1, c2 = st.columns([1, 2])
            with c1:
                st.write("### Send Money To:")
                st.code(BKASH_NUMBER, language="text")
                st.caption("bKash Personal (Send Money)")
                
            with c2:
                with st.form("pay_form"):
                    trx = st.text_input("Enter Transaction ID (TrxID)")
                    if st.form_submit_button("Submit Payment"):
                        if len(trx) > 5:
                            update_user_data(user_email, 'trx_id', trx)
                            update_user_data(user_email, 'payment_status', 'Pending')
                            st.success("Payment Sent! Admin will verify shortly.")
                            st.rerun()
                        else:
                            st.error("Invalid TrxID")

    elif selected == "My Profile":
        st.header("My Profile")
        c1, c2 = st.columns([1, 3])
        with c1:
            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=120)
        with c2:
            st.write(f"**Name:** {user['name']}")
            st.write(f"**Email:** {user_email}")
            st.write(f"**Bio:** {user.get('bio', '')}")
            
            new_bio = st.text_area("Update Bio")
            if st.button("Save Bio"):
                update_user_data(user_email, 'bio', new_bio)
                st.success("Bio Updated")
