import streamlit as st
import pandas as pd
import json
import os
import time
import random
import plotly.express as px
from datetime import datetime
from streamlit_option_menu import option_menu

# --- 🚀 PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CPC Spring 2026 | Ultimate",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 🎨 ULTRA-MODERN CSS (CYBERPUNK GLASS) ---
st.markdown("""
<style>
    /* GLOBAL DARK THEME */
    .stApp {
        background-color: #000000;
        background-image: radial-gradient(circle at 50% 50%, #1a1a2e 0%, #000000 100%);
        color: #e0e0e0;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* NEON TEXT GLOW */
    .neon-text {
        color: #fff;
        text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc, 0 0 40px #00ffcc;
    }

    /* GLASS CARDS */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        border-color: #00ffcc;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.2);
    }

    /* CUSTOM BUTTONS */
    .stButton > button {
        background: linear-gradient(45deg, #00c6ff, #0072ff);
        border: none;
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        width: 100%;
    }
    .stButton > button:hover {
        box-shadow: 0 0 20px rgba(0, 114, 255, 0.6);
        transform: scale(1.02);
    }
    .stButton > button:active { transform: scale(0.98); }

    /* INPUT FIELDS */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #00c6ff !important;
        box-shadow: 0 0 10px rgba(0, 198, 255, 0.3);
    }

    /* PRIZE TYPOGRAPHY */
    .prize-amount { font-size: 2.5rem; font-weight: 800; background: -webkit-linear-gradient(#eee, #333); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .gold { color: #FFD700; text-shadow: 0 0 10px #FFD700; }
    
    /* SCROLLBAR */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #000; }
    ::-webkit-scrollbar-thumb { background: #333; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #00c6ff; }
</style>
""", unsafe_allow_html=True)

# --- 💾 DATABASE MANAGER ---
DB_FILE = "users.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_data(data):
    with open(DB_FILE, "w") as f: json.dump(data, f, indent=4)

if 'users' not in st.session_state: st.session_state['users'] = load_data()
if 'logged_in_user' not in st.session_state: st.session_state['logged_in_user'] = None

# --- CONSTANTS ---
ADMIN_KEY = "891011"
BKASH_NO = "01346561010"

# --- 🔐 AUTH LOGIC ---
def login(email, pwd):
    email = email.strip().lower()
    users = load_data()
    if email in users and users[email]['password'] == pwd.strip():
        st.session_state['logged_in_user'] = email
        return True
    return False

def register(email, pwd, name):
    email = email.strip().lower()
    if not email.endswith("@diu.edu.bd"): return "Domain Error"
    users = load_data()
    if email in users: return "Exists"
    
    users[email] = {
        'password': pwd.strip(),
        'name': name.strip(),
        'id': None,
        'payment_status': 'Incomplete',
        'trx_id': None,
        'bio': '',
        'skills': [],
        'joined_at': str(datetime.now())
    }
    save_data(users)
    return "Success"

# =========================================================
#  SECTION 1: 🛡️ THE GATEKEEPER (LOGIN/SIGNUP)
# =========================================================
if st.session_state['logged_in_user'] is None:
    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center;">
            <h1 class='neon-text' style="font-size: 3.5rem; margin-bottom: 0;">CPC SPRING 2026</h1>
            <p style="color: #00c6ff; letter-spacing: 3px; font-weight: bold;">THE ULTIMATE CODING ARENA</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Glassmorphism Login Box
        with st.container():
            st.markdown('<div class="glass-card" style="max-width: 500px; margin: 0 auto;">', unsafe_allow_html=True)
            
            tab_l, tab_s = st.tabs(["ACCESS TERMINAL", "NEW REGISTRATION"])
            
            with tab_l:
                email = st.text_input("University Email", key="l_e", placeholder="id@diu.edu.bd")
                pwd = st.text_input("Access Key", type="password", key="l_p")
                if st.button("INITIATE SESSION 🚀"):
                    if login(email, pwd): st.rerun()
                    else: st.error("❌ Access Denied: Invalid Credentials")
            
            with tab_s:
                name = st.text_input("Operator Name", placeholder="Full Name")
                n_email = st.text_input("University Email", key="s_e", placeholder="id@diu.edu.bd")
                n_pwd = st.text_input("Set Access Key", type="password", key="s_p")
                if st.button("CREATE PROFILE ✨"):
                    res = register(n_email, n_pwd, name)
                    if res == "Success": st.success("✅ Profile Created. Please Login.")
                    elif res == "Domain Error": st.error("⚠️ System Restriction: @diu.edu.bd only.")
                    else: st.error("⚠️ User already exists.")
            
            st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
#  SECTION 2: 🚀 MAIN INTERFACE (LOGGED IN)
# =========================================================
else:
    user_email = st.session_state['logged_in_user']
    # Security Check (in case user was deleted)
    if user_email not in st.session_state['users']:
        st.session_state['logged_in_user'] = None
        st.rerun()
        
    user = st.session_state['users'][user_email]

    # --- 🤖 SIDEBAR (ADMIN & SETTINGS) ---
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2942/2942544.png", width=80)
        st.markdown(f"### {user['name']}")
        st.caption(user_email)
        st.markdown("---")
        
        # ADMIN MODE
        if st.checkbox("🔒 Admin Console"):
            key = st.text_input("Admin Password", type="password")
            if key == ADMIN_KEY:
                st.success("🔓 SYSTEM UNLOCKED")
                
                # --- AI ANALYTICS ---
                st.subheader("📊 AI Analytics")
                all_users = load_data()
                df = pd.DataFrame(all_users).T
                if not df.empty:
                    # Chart 1: Payment Status
                    fig_pie = px.pie(df, names='payment_status', title='Registration Health', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
                    fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
                    st.plotly_chart(fig_pie, use_container_width=True)

                st.markdown("---")
                # --- USER MANAGEMENT ---
                st.subheader("👥 User Control")
                
                # Approve
                pending = [u for u, d in all_users.items() if d['payment_status'] == 'Pending']
                if pending:
                    u_app = st.selectbox("⏳ Pending Approvals", pending)
                    if st.button("✅ Approve Selected"):
                        all_users[u_app]['payment_status'] = "Approved"
                        save_data(all_users)
                        st.session_state['users'] = all_users
                        st.success(f"Approved {u_app}")
                        st.rerun()
                else:
                    st.info("No pending payments.")
                
                # Ban/Delete
                st.markdown("#### 🚫 Danger Zone")
                u_ban = st.selectbox("Select User to Ban", list(all_users.keys()))
                if st.button("🔥 BAN USER"):
                    del all_users[u_ban]
                    save_data(all_users)
                    st.session_state['users'] = all_users
                    st.warning(f"User {u_ban} terminated.")
                    st.rerun()
            else:
                st.error("Access Denied")
        
        st.markdown("---")
        if st.button("🛑 LOGOUT"):
            st.session_state['logged_in_user'] = None
            st.rerun()

    # --- 🏠 MAIN CONTENT ---
    
    # NAVIGATION
    selected = option_menu(
        menu_title=None,
        options=["Command Center", "Registration", "AI Team Finder", "Profile"],
        icons=["hdd-network", "credit-card-2-front", "robot", "person-circle"],
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "rgba(255,255,255,0.05)"},
            "icon": {"color": "#00c6ff", "font-size": "16px"}, 
            "nav-link": {"font-size": "14px", "text-align": "center", "margin":"0px", "color": "white"},
            "nav-link-selected": {"background-color": "#0072ff"},
        }
    )
    
    # --- TAB 1: COMMAND CENTER (HOME) ---
    if selected == "Command Center":
        st.markdown(f"<h1 class='neon-text' style='text-align: center'>WELCOME, OPERATOR {user['name'].split()[0].upper()}</h1>", unsafe_allow_html=True)
        
        # Countdown
        st.markdown("""
        <div class="glass-card" style="text-align: center; margin-bottom: 20px;">
            <h3 style="color: #00c6ff;">MISSION START COUNTDOWN</h3>
            <h1 style="font-family: monospace; font-size: 3rem;">142 <span style="font-size:1rem">DAYS</span> : 05 <span style="font-size:1rem">HRS</span></h1>
        </div>
        """, unsafe_allow_html=True)
        
        # Prizes
        st.markdown("### 🏆 PRIZE POOL")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="glass-card" style="text-align:center; border-bottom: 4px solid #FFD700"><h2 class="gold">🥇 1ST</h2><h1>5,000 ৳</h1></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="glass-card" style="text-align:center; border-bottom: 4px solid #C0C0C0"><h2 style="color:#C0C0C0">🥈 2ND</h2><h1>2,500 ৳</h1></div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="glass-card" style="text-align:center; border-bottom: 4px solid #CD7F32"><h2 style="color:#CD7F32">🥉 3RD</h2><h1>1,000 ৳</h1></div>', unsafe_allow_html=True)

    # --- TAB 2: REGISTRATION WIZARD ---
    elif selected == "Registration":
        st.markdown("## 📝 EVENT REGISTRATION")
        
        status = user['payment_status']
        
        if status == "Approved":
            st.markdown("""
            <div class="glass-card" style="border-color: #00ff00; text-align: center;">
                <h1 style="color: #00ff00; font-size: 4rem;">✅</h1>
                <h2>ACCESS GRANTED</h2>
                <p>You are officially registered for the event.</p>
                <code style="background: #111; padding: 10px; border-radius: 5px;">ID: {uid}</code>
            </div>
            """.format(uid=user.get('id')), unsafe_allow_html=True)
            st.balloons()
            
        elif status == "Pending":
            st.warning("⏳ Transaction Under Verification. Please stand by.")
            
        else:
            # INTERACTIVE WIZARD
            if not user['id']:
                with st.container():
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.subheader("Step 1: Identity Verification")
                    with st.form("id_f"):
                        sid = st.text_input("Enter Student ID (xxx-xx-xxx)")
                        if st.form_submit_button("PROCEED TO PAYMENT ➡️"):
                            if re.match(r"^\d{3}-\d{2}-\d{3,4}$", sid):
                                user['id'] = sid
                                save_data(st.session_state['users'])
                                st.rerun()
                            else:
                                st.error("Invalid Format")
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                # PAYMENT POPUP
                with st.container():
                    st.markdown(f"""
                    <div class="glass-card" style="border-color: #e91e63;">
                        <h3 style="color: #e91e63;">💳 SECURE PAYMENT GATEWAY</h3>
                        <p>Transfer <strong>BDT 500</strong> via bKash Personal</p>
                        <h1 style="background: #222; padding: 10px; border-radius: 10px; text-align: center;">{BKASH_NO}</h1>
                    </div>
                    <br>
                    """, unsafe_allow_html=True)
                    
                    with st.form("pay_f"):
                        trx = st.text_input("ENTER TRANSACTION ID (TrxID)")
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.form_submit_button("⬅️ EDIT ID"):
                                user['id'] = None
                                save_data(st.session_state['users'])
                                st.rerun()
                        with c2:
                            if st.form_submit_button("CONFIRM PAYMENT ✅"):
                                if len(trx) > 5:
                                    user['trx_id'] = trx
                                    user['payment_status'] = 'Pending'
                                    save_data(st.session_state['users'])
                                    st.success("Payment Uploaded!")
                                    st.rerun()
                                else:
                                    st.error("Invalid TrxID")

    # --- TAB 3: AI TEAM FINDER (NEW FEATURE) ---
    elif selected == "AI Team Finder":
        st.markdown("## 🧠 AI TEAMMATES MATCHING")
        st.info("Our algorithm suggests teammates based on your bio keywords.")
        
        # User's own skills
        my_bio = user.get('bio', '')
        if not my_bio:
            st.warning("⚠️ Please update your Bio in 'Profile' to get matched!")
        else:
            # Simulate AI Matching
            st.markdown("### 🔍 Recommended Teammates For You")
            
            # Get other users
            all_users = load_data()
            candidates = [u for e, u in all_users.items() if e != user_email and u.get('bio')]
            
            if candidates:
                # Mock AI Selection (Random for demo, but represents logic)
                match = random.choice(candidates)
                
                col_a, col_b = st.columns([1,3])
                with col_a:
                    st.image("https://cdn-icons-png.flaticon.com/512/4140/4140048.png")
                with col_b:
                    st.markdown(f"<div class='glass-card'><h3>{match['name']}</h3><p>{match['bio']}</p><button style='background:green; color:white; border:none; padding:5px; border-radius:5px'>Request Team Up</button></div>", unsafe_allow_html=True)
            else:
                st.write("No active candidates found yet. Check back later!")

    # --- TAB 4: PROFILE ---
    elif selected == "Profile":
        c1, c2 = st.columns([1, 2])
        with c1:
            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=200)
        with c2:
            st.markdown(f"## {user['name']}")
            st.write(f"📧 **{user_email}**")
            st.write(f"🆔 **{user.get('id', 'N/A')}**")
            st.write(f"📅 Joined: {user.get('joined_at', 'Unknown')[:10]}")
            
            st.markdown("### 📝 Bio / Skills")
            new_bio = st.text_area("Write your skills for AI Matching...", value=user.get('bio', ''))
            if st.button("SAVE PROFILE"):
                user['bio'] = new_bio
                save_data(st.session_state['users'])
                st.success("Profile Updated!")
