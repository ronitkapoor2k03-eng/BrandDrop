import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

# PAGE CONFIGURATION
st.set_page_config(
    page_title="BrandDrop - Experience Marketplace",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CUSTOM CSS
st.markdown("""
<style>
    .brand-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 2rem 2.5rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
    }
    .brand-header h1 { font-size: 2.8rem; font-weight: 700; margin: 0; }
    .brand-header p { font-size: 1.2rem; opacity: 0.9; margin: 0.5rem 0 0 0; }
    .brand-header .tagline { font-size: 1rem; opacity: 0.7; margin-top: 0.3rem; font-style: italic; }
    
    .experience-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        border-left: 5px solid #e74c3c;
        transition: transform 0.2s;
        height: 100%;
    }
    .experience-card:hover { transform: translateY(-3px); box-shadow: 0 4px 20px rgba(0,0,0,0.12); }
    .experience-card h4 { color: #1a1a2e; margin: 0 0 0.3rem 0; }
    .experience-card .brand-name { color: #e74c3c; font-weight: 600; font-size: 0.95rem; }
    .experience-card .meta { color: #666; font-size: 0.9rem; margin: 0.3rem 0; }
    .experience-card .description { color: #555; font-size: 0.9rem; margin: 0.5rem 0; }
    .experience-card .rating { color: #f39c12; font-weight: 600; }
    .experience-card .spots { font-weight: 600; color: #2ecc71; }
    .experience-card .spots-full { font-weight: 600; color: #e74c3c; }
    
    .progress-container {
        background: #e9ecef;
        height: 8px;
        border-radius: 4px;
        margin: 0.5rem 0;
        overflow: hidden;
    }
    .progress-fill {
        background: linear-gradient(90deg, #e74c3c, #c0392b);
        height: 100%;
        border-radius: 4px;
        transition: width 0.5s ease;
    }
    
    .metric-box {
        background: #f8f9fa;
        padding: 1.2rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #e9ecef;
        transition: transform 0.2s;
    }
    .metric-box:hover { transform: translateY(-2px); box-shadow: 0 2px 12px rgba(0,0,0,0.05); }
    .metric-box h1, .metric-box h2, .metric-box h3 { color: #e74c3c; margin: 0; }
    .metric-box p { margin: 0.3rem 0 0 0; color: #666; font-size: 0.9rem; }
    
    .passport-stamp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.3rem 1.2rem;
        border-radius: 20px;
        display: inline-block;
        font-size: 0.85rem;
        font-weight: 500;
        margin: 0.2rem;
    }
    
    .achievement-unlocked {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .achievement-locked {
        background: #f1f3f5;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        opacity: 0.6;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .achievement-locked h4, .achievement-unlocked h4 { margin: 0; }
    .achievement-locked p, .achievement-unlocked p { margin: 0; font-size: 0.9rem; opacity: 0.9; }
    
    .club-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        text-align: center;
        border: 1px solid #e9ecef;
        transition: transform 0.2s;
        height: 100%;
    }
    .club-card:hover { transform: translateY(-3px); box-shadow: 0 4px 16px rgba(0,0,0,0.08); }
    .club-card h3 { margin: 0.5rem 0; color: #1a1a2e; }
    .club-card .member-count { color: #666; font-size: 0.9rem; }
    .club-card .event-count { color: #e74c3c; font-weight: 600; font-size: 0.9rem; }
    
    .developer-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #e74c3c;
        margin-top: 1rem;
    }
    .developer-box h3 { margin-top: 0; color: #1a1a2e; }
    .developer-box .team-member {
        display: flex;
        justify-content: space-between;
        padding: 0.3rem 0;
        border-bottom: 1px solid #e9ecef;
    }
    .developer-box .team-member:last-child { border-bottom: none; }
    .developer-box .role { color: #666; font-size: 0.85rem; }
    
    .stButton > button {
        background-color: #e74c3c;
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        width: 100%;
        transition: background 0.2s;
    }
    .stButton > button:hover { background-color: #c0392b; color: white; }
    
    .sidebar-header { text-align: center; padding: 1rem 0; }
    .sidebar-header h1 { color: #e74c3c; margin: 0; font-size: 1.8rem; }
    .sidebar-header p { color: #666; margin: 0; font-size: 0.85rem; }
    
    .sidebar-user {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .sidebar-user p { margin: 0.2rem 0; }
    .sidebar-user .name { font-weight: 600; color: #1a1a2e; }
    .sidebar-user .points { color: #e74c3c; font-weight: 600; }
    
    .footer {
        text-align: center;
        color: #666;
        padding: 2rem 0 1rem 0;
        border-top: 1px solid #e9ecef;
        margin-top: 2rem;
    }
    .footer h4 { color: #1a1a2e; margin: 0; }
    .footer p { margin: 0.3rem 0; font-size: 0.9rem; }
    
    .divider { border: none; border-top: 2px solid #e9ecef; margin: 2rem 0; }
</style>
""", unsafe_allow_html=True)

# INITIALIZE SESSION STATE
def init_session_state():
    if 'user' not in st.session_state:
        st.session_state.user = {
            'name': 'Ahmed Al Maktoum',
            'email': 'ahmed@example.com',
            'points': 450,
            'level': 3,
            'interests': ['Coffee', 'Fashion', 'Tech', 'Food']
        }
    
    if 'passport' not in st.session_state:
        st.session_state.passport = {
            'Coffee Explorer': {'count': 7, 'target': 10, 'unlocked': False},
            'Beauty Insider': {'count': 4, 'target': 5, 'unlocked': False},
            'Food Adventurer': {'count': 3, 'target': 10, 'unlocked': False},
            'Tech Enthusiast': {'count': 2, 'target': 5, 'unlocked': False},
            'Fitness Fanatic': {'count': 1, 'target': 5, 'unlocked': False},
            'Sneaker Hunter': {'count': 5, 'target': 3, 'unlocked': True},
            'Luxury Seeker': {'count': 2, 'target': 5, 'unlocked': False},
            'Dubai Explorer': {'count': 8, 'target': 5, 'unlocked': True}
        }
    
    if 'experiences' not in st.session_state:
        st.session_state.experiences = [
            {'id': 1, 'title': 'Matcha Tasting Experience', 'brand': 'Matcha House', 'category': 'Food', 'location': 'Dubai Mall', 'date': '2026-07-05', 'time': '10:00 AM', 'spots': 15, 'claimed': 12, 'description': 'Sample premium Japanese matcha and learn traditional tea preparation.', 'qr_code': 'MT-2026-001', 'rating': 4.8, 'reviews': 24, 'type': 'Product Sampling'},
            {'id': 2, 'title': 'Sneaker Launch Event', 'brand': 'Sole Society', 'category': 'Fashion', 'location': 'Mall of Emirates', 'date': '2026-07-06', 'time': '2:00 PM', 'spots': 50, 'claimed': 35, 'description': 'Exclusive preview of limited edition sneakers before public release.', 'qr_code': 'SN-2026-002', 'rating': 4.6, 'reviews': 18, 'type': 'Product Launch'},
            {'id': 3, 'title': 'Skincare Workshop', 'brand': 'Glow Lab', 'category': 'Beauty', 'location': 'City Walk', 'date': '2026-07-07', 'time': '11:00 AM', 'spots': 20, 'claimed': 8, 'description': 'Learn about skincare routines and receive personalized product recommendations.', 'qr_code': 'SK-2026-003', 'rating': 4.9, 'reviews': 31, 'type': 'Workshop'},
            {'id': 4, 'title': 'Coffee Brewing Masterclass', 'brand': 'Bean Masters', 'category': 'Coffee', 'location': 'Alserkal Avenue', 'date': '2026-07-08', 'time': '9:00 AM', 'spots': 25, 'claimed': 18, 'description': 'Master the art of pour-over, espresso, and cold brew techniques.', 'qr_code': 'CB-2026-004', 'rating': 4.7, 'reviews': 42, 'type': 'Workshop'},
            {'id': 5, 'title': 'Beach Fitness Challenge', 'brand': 'FitHub Dubai', 'category': 'Fitness', 'location': 'Kite Beach', 'date': '2026-07-09', 'time': '6:00 AM', 'spots': 30, 'claimed': 22, 'description': 'Morning HIIT session with professional trainers on the beach.', 'qr_code': 'FC-2026-005', 'rating': 4.5, 'reviews': 15, 'type': 'Community Challenge'},
            {'id': 6, 'title': 'Mystery Gift Drop', 'brand': 'Mystery Box Co.', 'category': 'Luxury', 'location': 'Dubai Marina', 'date': '2026-07-10', 'time': '5:00 PM', 'spots': 10, 'claimed': 10, 'description': 'Be one of the first 10 to claim an exclusive mystery gift.', 'qr_code': 'MG-2026-006', 'rating': 4.9, 'reviews': 56, 'type': 'Mystery Drop'},
            {'id': 7, 'title': 'Tech Innovation Showcase', 'brand': 'Dubai Tech Hub', 'category': 'Tech', 'location': 'Dubai Internet City', 'date': '2026-07-11', 'time': '3:00 PM', 'spots': 40, 'claimed': 28, 'description': 'Experience the latest in AI, VR, and emerging technologies.', 'qr_code': 'TI-2026-007', 'rating': 4.7, 'reviews': 33, 'type': 'Product Launch'},
            {'id': 8, 'title': 'Emirati Cuisine Trail', 'brand': 'Taste of UAE', 'category': 'Food', 'location': 'Various Locations', 'date': '2026-07-12', 'time': '12:00 PM', 'spots': 20, 'claimed': 5, 'description': 'Explore authentic Emirati restaurants across Dubai.', 'qr_code': 'EC-2026-008', 'rating': 4.8, 'reviews': 12, 'type': 'Community Challenge'}
        ]
    
    if 'claimed_experiences' not in st.session_state:
        st.session_state.claimed_experiences = [1, 4, 7]
    
    if 'reviews' not in st.session_state:
        st.session_state.reviews = {}
    
    if 'clubs' not in st.session_state:
        st.session_state.clubs = {
            'Coffee Club': {'members': 234, 'events': 12, 'joined': True},
            'Beauty Club': {'members': 189, 'events': 9, 'joined': False},
            'Sneaker Club': {'members': 156, 'events': 7, 'joined': True},
            'Pet Club': {'members': 98, 'events': 5, 'joined': False},
            'Parents Club': {'members': 112, 'events': 6, 'joined': False},
            'Foodies Club': {'members': 312, 'events': 15, 'joined': True},
            'Gamers Club': {'members': 145, 'events': 8, 'joined': False},
            'Fitness Club': {'members': 178, 'events': 10, 'joined': False}
        }

init_session_state()

# SIDEBAR NAVIGATION
with st.sidebar:
    st.markdown('<div class="sidebar-header"><h1>🎯 BrandDrop</h1><p>UAEs Experience Marketplace</p></div>', unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("Navigate", ["Dashboard", "Discover", "My Passport", "Rewards", "Clubs", "For Brands", "About"], key="main_menu", label_visibility="collapsed")
    st.markdown("---")
    st.markdown(f'<div class="sidebar-user"><p class="name">👤 {st.session_state.user["name"]}</p><p>⭐ Level {st.session_state.user["level"]}</p><p class="points">🏆 {st.session_state.user["points"]} points</p></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div style="font-size:0.75rem; color:#999; text-align:center;"><p>📱 v2.0.0</p><p>🇦🇪 Made in UAE</p></div>', unsafe_allow_html=True)

# DASHBOARD
if menu == "Dashboard":
    st.markdown('<div class="brand-header"><h1>Welcome to BrandDrop</h1><p>UAEs First Consumer Experience Marketplace</p><p class="tagline">"Discover. Experience. Earn." — Where brands come to life.</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        attended = len(st.session_state.claimed_experiences)
        st.markdown(f'<div class="metric-box"><h3>{attended}</h3><p>Experiences Attended</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-box"><h3>{st.session_state.user["points"]}</h3><p>Total Points</p></div>', unsafe_allow_html=True)
    with col3:
        unlocked = sum(1 for v in st.session_state.passport.values() if v['unlocked'])
        total = len(st.session_state.passport)
        st.markdown(f'<div class="metric-box"><h3>{unlocked}/{total}</h3><p>Passport Stamps</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-box"><h3>{len(st.session_state.experiences)}</h3><p>Available Experiences</p></div>', unsafe_allow_html=True)
    
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("### 🔥 Featured Experiences")
    st.markdown("*Curated experiences based on your interests*")
    
    user_interests = [i.lower() for i in st.session_state.user['interests']]
    featured = [exp for exp in st.session_state.experiences if exp['category'].lower() in user_interests][:3]
    if not featured:
        featured = st.session_state.experiences[:3]
    
    cols = st.columns(3)
    for idx, exp in enumerate(featured):
        with cols[idx]:
            available = exp['spots'] - exp['claimed']
            progress = (exp['claimed'] / exp['spots']) * 100 if exp['spots'] > 0 else 0
            st.markdown(f'<div class="experience-card"><h4>{exp["title"]}</h4><p class="brand-name">{exp["brand"]}</p><p class="meta">📍 {exp["location"]} • 📅 {exp["date"]}</p><p class="meta">⏰ {exp["time"]} • 🏷️ {exp["type"]}</p><p class="description">{exp["description"][:80]}...</p><div class="progress-container"><div class="progress-fill" style="width:{progress}%;"></div></div><p class="spots">{available} spots remaining</p><p class="rating">⭐ {exp["rating"]} ({exp["reviews"]} reviews)</p></div>', unsafe_allow_html=True)
            if available > 0:
                if st.button(f"Reserve Now", key=f"dash_{exp['id']}"):
                    st.success(f"✅ Reserved! Your QR Code: {exp['qr_code']}")
                    st.balloons()
                    if exp['id'] not in st.session_state.claimed_experiences:
                        st.session_state.claimed_experiences.append(exp['id'])
                        st.session_state.user['points'] += 20
                        for passport_name in st.session_state.passport:
                            if exp['category'].lower() in passport_name.lower():
                                st.session_state.passport[passport_name]['count'] += 1
                                if st.session_state.passport[passport_name]['count'] >= st.session_state.passport[passport_name]['target']:
                                    st.session_state.passport[passport_name]['unlocked'] = True
    
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("### 📗 Experience Passport Progress")
    st.markdown("*Collect stamps and unlock achievements*")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        for idx, (category, data) in enumerate(list(st.session_state.passport.items())[:4]):
            progress = min(data['count'] / data['target'], 1)
            status = "✅" if data['unlocked'] else "🔒"
            st.markdown(f'<div style="margin:0.5rem 0;"><div style="display:flex; justify-content:space-between; align-items:center;"><span><strong>{status} {category}</strong></span><span style="font-size:0.85rem; color:#666;">{data["count"]}/{data["target"]}</span></div><div class="progress-container"><div class="progress-fill" style="width:{progress*100}%;"></div></div></div>', unsafe_allow_html=True)
    
    with col2:
        next_ach = None
        for name, data in st.session_state.passport.items():
            if not data['unlocked']:
                next_ach = (name, data)
                break
        if next_ach:
            name, data = next_ach
            progress = int((data['count'] / data['target']) * 100)
            st.markdown(f'<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding:1.5rem; border-radius:10px; color:white; height:100%;"><h4>🎯 Next Achievement</h4><p><strong>{name}</strong></p><p>Progress: {data["count"]}/{data["target"]}</p><div class="progress-container" style="background:rgba(255,255,255,0.3);"><div class="progress-fill" style="background:white; width:{progress}%;"></div></div><p style="font-size:0.85rem; opacity:0.8; margin-top:0.5rem;">Unlock exclusive experiences and VIP access</p></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="background: #27ae60; padding:1.5rem; border-radius:10px; color:white; height:100%;"><h4>🏆 All Achievements Unlocked!</h4><p>You are a BrandDrop Master!</p><p style="font-size:0.85rem; opacity:0.8;">New challenges coming soon</p></div>', unsafe_allow_html=True)

# DISCOVER
elif menu == "Discover":
    st.markdown('<div class="brand-header"><h1>📍 Discover Experiences</h1><p>Find brand experiences happening near you</p><p class="tagline">Instead of scrolling through ads, discover experiences</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        category_filter = st.selectbox("Category", ["All", "Beauty", "Fashion", "Food", "Coffee", "Fitness", "Tech", "Luxury", "Gaming"])
    with col2:
        type_filter = st.selectbox("Experience Type", ["All", "Product Sampling", "Product Launch", "Workshop", "Flash Reward", "Mystery Drop", "Treasure Hunt", "Community Challenge"])
    with col3:
        date_filter = st.date_input("Date", datetime.now())
    with col4:
        location_filter = st.text_input("Location", "Dubai")
    
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    
    filtered = st.session_state.experiences
    if category_filter != "All":
        filtered = [e for e in filtered if e['category'] == category_filter]
    if type_filter != "All":
        filtered = [e for e in filtered if e['type'] == type_filter]
    
    st.markdown(f"### 📋 {len(filtered)} Experiences Available")
    
    for exp in filtered:
        available = exp['spots'] - exp['claimed']
        progress = (exp['claimed'] / exp['spots']) * 100 if exp['spots'] > 0 else 0
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.markdown(f'<div style="border-left:4px solid #e74c3c; padding-left:1rem; margin:0.5rem 0;"><h4>{exp["title"]}</h4><p style="color:#e74c3c; font-weight:500;">{exp["brand"]} • {exp["category"]}</p><p style="font-size:0.9rem; color:#555;">🏷️ {exp["type"]}</p><p style="font-size:0.9rem;">📍 {exp["location"]} • 📅 {exp["date"]} at {exp["time"]}</p><p style="font-size:0.9rem; color:#555;">{exp["description"]}</p><p class="rating">⭐ {exp["rating"]} ({exp["reviews"]} reviews)</p></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div style="margin-top:1rem;"><p><strong>Availability</strong></p><p class="{"spots" if available > 0 else "spots-full"}">{available} spots remaining</p><div class="progress-container"><div class="progress-fill" style="width:{progress}%;"></div></div><p style="font-size:0.8rem; color:#666;">{exp["claimed"]}/{exp["spots"]} claimed</p><p style="font-size:0.8rem; color:#666;">🔑 QR: {exp["qr_code"]}</p></div>', unsafe_allow_html=True)
            with col3:
                if available > 0:
                    if st.button(f"🔴 Reserve", key=f"disc_{exp['id']}"):
                        st.success("✅ Reserved! Check your Passport.")
                        st.balloons()
                        if exp['id'] not in st.session_state.claimed_experiences:
                            st.session_state.claimed_experiences.append(exp['id'])
                            st.session_state.user['points'] += 20
                            for passport_name in st.session_state.passport:
                                if exp['category'].lower() in passport_name.lower():
                                    st.session_state.passport[passport_name]['count'] += 1
                                    if st.session_state.passport[passport_name]['count'] >= st.session_state.passport[passport_name]['target']:
                                        st.session_state.passport[passport_name]['unlocked'] = True
                else:
                    st.markdown("🔴 **Fully Booked**")

# MY PASSPORT
elif menu == "My Passport":
    st.markdown('<div class="brand-header"><h1>📗 My Experience Passport</h1><p>Collect stamps and unlock achievements</p><p class="tagline">Every experience adds a digital stamp to your passport</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        attended = len(st.session_state.claimed_experiences)
        st.markdown(f'<div class="metric-box"><h2>{attended}</h2><p>Total Experiences</p></div>', unsafe_allow_html=True)
    with col2:
        unlocked = sum(1 for v in st.session_state.passport.values() if v['unlocked'])
        total = len(st.session_state.passport)
        st.markdown(f'<div class="metric-box"><h2>{unlocked}/{total}</h2><p>Passport Stamps Unlocked</p></div>', unsafe_allow_html=True)
    with col3:
        points = st.session_state.user['points']
        st.markdown(f'<div class="metric-box"><h2>{points}</h2><p>Total Points Earned</p></div>', unsafe_allow_html=True)
    
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("### ✨ Your Passport Stamps")
    
    col1, col2 = st.columns(2)
    for idx, (category, data) in enumerate(st.session_state.passport.items()):
        with col1 if idx % 2 == 0 else col2:
            progress = min(data['count'] / data['target'], 1)
            status = "✅ Unlocked" if data['unlocked'] else f"🔒 {data['count']}/{data['target']}"
            st.markdown(f'<div style="background:#f8f9fa; padding:1rem; border-radius:8px; margin:0.5rem 0;"><div style="display:flex; justify-content:space-between; align-items:center;"><span class="passport-stamp">{category}</span><span style="font-size:0.85rem; font-weight:500;">{status}</span></div><div class="progress-container" style="margin-top:0.5rem;"><div class="progress-fill" style="width:{progress*100}%;"></div></div><p style="font-size:0.85rem; color:#666; margin-top:0.3rem;">{data["count"]}/{data["target"]} completed</p></div>', unsafe_allow_html=True)
    
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("### 🏆 Achievements")
    st.markdown("*Complete collections to unlock VIP invitations, early access, and exclusive merchandise*")
    
    achievements = [
        {"name": "Coffee Explorer", "desc": "Visit 10 independent cafes -> Unlock exclusive coffee tastings", "unlocked": st.session_state.passport['Coffee Explorer']['unlocked']},
        {"name": "Beauty Insider", "desc": "Attend 5 beauty launches -> Get early access to new products", "unlocked": st.session_state.passport['Beauty Insider']['unlocked']},
        {"name": "Dubai Explorer", "desc": "Complete experiences across 5 malls -> Earn city-wide rewards", "unlocked": st.session_state.passport['Dubai Explorer']['unlocked']},
        {"name": "Sneaker Hunter", "desc": "Attend 3 sneaker launches -> VIP access to limited editions", "unlocked": st.session_state.passport['Sneaker Hunter']['unlocked']},
        {"name": "Food Adventurer", "desc": "Visit 10 restaurants -> Exclusive dining experiences", "unlocked": st.session_state.passport['Food Adventurer']['unlocked']},
        {"name": "Tech Enthusiast", "desc": "Attend 5 tech events -> Early access to innovations", "unlocked": st.session_state.passport['Tech Enthusiast']['unlocked']},
        {"name": "Fitness Fanatic", "desc": "Complete 5 fitness challenges -> Premium wellness access", "unlocked": st.session_state.passport['Fitness Fanatic']['unlocked']}
    ]
    
    for ach in achievements:
        if ach['unlocked']:
            st.markdown(f'<div class="achievement-unlocked"><div><h4>✅ {ach["name"]}</h4><p>{ach["desc"]}</p></div><span style="font-size:2rem;">🏆</span></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="achievement-locked"><div><h4>🔒 {ach["name"]}</h4><p>{ach["desc"]}</p></div><span style="font-size:1.5rem; opacity:0.5;">🔒</span></div>', unsafe_allow_html=True)

# REWARDS
elif menu == "Rewards":
    st.markdown('<div class="brand-header"><h1>🏆 Rewards & Benefits</h1><p>Redeem your points for exclusive experiences</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-box"><h1>{st.session_state.user["points"]}</h1><p>Available Points</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-box"><h1>Level {st.session_state.user["level"]}</h1><p>Member Status</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-box"><h1>200</h1><p>Points to Next Level</p></div>', unsafe_allow_html=True)
    
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("### 🎁 Reward Catalog")
    
    rewards = [
        {"name": "AED 50 Gift Card", "points": 200},
        {"name": "Movie Tickets (2)", "points": 150},
        {"name": "Exclusive Event Invite", "points": 300},
        {"name": "Brand Merchandise", "points": 250},
        {"name": "Premium Coffee Tasting", "points": 180}
    ]
    
    for reward in rewards:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(f"**{reward['name']}**")
        with col2:
            st.markdown(f"{reward['points']} points")
        with col3:
            if st.button(f"Redeem", key=f"rew_{reward['name']}"):
                if st.session_state.user['points'] >= reward['points']:
                    st.success(f"✅ Redeemed: {reward['name']}")
                    st.session_state.user['points'] -= reward['points']
                else:
                    st.error("❌ Insufficient points")

# CLUBS
elif menu == "Clubs":
    st.markdown('<div class="brand-header"><h1>👥 Consumer Clubs</h1><p>Join niche communities and connect with like-minded enthusiasts</p></div>', unsafe_allow_html=True)
    
    clubs = [
        {"name": "☕ Coffee Club", "members": 234, "events": 12, "joined": st.session_state.clubs['Coffee Club']['joined']},
        {"name": "💄 Beauty Club", "members": 189, "events": 9, "joined": st.session_state.clubs['Beauty Club']['joined']},
        {"name": "👟 Sneaker Club", "members": 156, "events": 7, "joined": st.session_state.clubs['Sneaker Club']['joined']},
        {"name": "🐾 Pet Club", "members": 98, "events": 5, "joined": st.session_state.clubs['Pet Club']['joined']},
        {"name": "👨‍👩‍👧‍👦 Parents Club", "members": 112, "events": 6, "joined": st.session_state.clubs['Parents Club']['joined']},
        {"name": "🍽️ Foodies Club", "members": 312, "events": 15, "joined": st.session_state.clubs['Foodies Club']['joined']},
        {"name": "🎮 Gamers Club", "members": 145, "events": 8, "joined": st.session_state.clubs['Gamers Club']['joined']},
        {"name": "💪 Fitness Club", "members": 178, "events": 10, "joined": st.session_state.clubs['Fitness Club']['joined']}
    ]
    
    col1, col2, col3 = st.columns(3)
    for idx, club in enumerate(clubs):
        with [col1, col2, col3][idx % 3]:
            status = "✅ Joined" if club['joined'] else "🔘 Join Now"
            st.markdown(f'<div class="club-card"><h3>{club["name"]}</h3><p class="member-count">👥 {club["members"]} members</p><p class="event-count">🎯 {club["events"]} upcoming events</p><p style="margin-top:0.5rem; font-weight:600; color:{"#2ecc71" if club["joined"] else "#e74c3c"};">{status}</p></div>', unsafe_allow_html=True)
            if not club['joined']:
                if st.button(f"Join", key=f"join_{club['name']}"):
                    club_name = club['name'].replace("☕ ", "").replace("💄 ", "").replace("👟 ", "").replace("🐾 ", "").replace("👨‍👩‍👧‍👦 ", "").replace("🍽️ ", "").replace("🎮 ", "").replace("💪 ", "")
                    st.session_state.clubs[club_name]['joined'] = True
                    st.success(f"✅ Joined {club['name']}!")
                    st.rerun()

# FOR BRANDS
elif menu == "For Brands":
    st.markdown('<div class="brand-header"><h1>🏢 For Brands</h1><p>Launch campaigns and measure real engagement</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-box"><h3>1,247</h3><p>Total Attendees</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-box"><h3>12</h3><p>Active Campaigns</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-box"><h3>87%</h3><p>Avg. Redemption Rate</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-box"><h3>4.7</h3><p>Avg. Rating</p></div>', unsafe_allow_html=True)
    
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("### 🚀 Create New Campaign")
    
    with st.form("campaign_form"):
        col1, col2 = st.columns(2)
        with col1:
            campaign_name = st.text_input("Campaign Name", "Summer Launch 2026")
            brand_name = st.text_input("Brand Name", "Your Brand")
            category = st.selectbox("Category", ["Beauty", "Fashion", "Food", "Coffee", "Fitness", "Tech", "Luxury"])
            location = st.text_input("Location", "Dubai Mall")
        with col2:
            start_date = st.date_input("Start Date", datetime.now())
            end_date = st.date_input("End Date", datetime.now() + timedelta(days=7))
            capacity = st.number_input("Capacity", min_value=10, max_value=500, value=50)
            budget = st.number_input("Budget (AED)", min_value=1000, value=5000)
        submitted = st.form_submit_button("Launch Campaign", type="primary")
        if submitted:
            st.success("✅ Campaign created successfully! Your experience is now live.")
            st.balloons()
    
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("### 📊 Campaign Performance")
    
    data = pd.DataFrame({'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'], 'Attendees': [38, 55, 72, 85], 'Redemptions': [30, 48, 61, 72]})
    fig = px.line(data, x='Week', y=['Attendees', 'Redemptions'], title='Campaign Performance Trends', labels={'value': 'Users', 'variable': 'Metric'})
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

# ABOUT
elif menu == "About":
    st.markdown('<div class="brand-header"><h1>ℹ️ About BrandDrop</h1><p>UAEs First Consumer Experience Marketplace</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### Our Mission
        BrandDrop is revolutionizing how brands connect with consumers in the UAE. We are replacing traditional advertising with real-world experiences.
        
        ### The Problem We Solve
        - ❌ Consumers skip ads and ignore influencer promotions
        - ❌ Brands waste budget on activations without measuring ROI
        - ❌ No single platform exists for discovering brand experiences
        
        ### Our Solution
        - ✅ Single platform for discovering and booking brand experiences
        - ✅ Measurable engagement instead of just impressions
        - ✅ Experience Passport with achievements and rewards
        - ✅ Real-time analytics for brands
        
        ### Why UAE?
        - 🇦🇪 Retail- and mall-driven culture
        - 🇦🇪 Frequent product launches and brand activations
        - 🇦🇪 Large tourism volumes
        - 🇦🇪 Digitally connected population
        """)
    
    with col2:
        st.markdown("""
        <div style="background:#f8f9fa; padding:1.5rem; border-radius:10px;">
            <h3>📊 Quick Stats</h3>
            <p>👥 5,000+ Users</p>
            <p>🏢 200+ Brands</p>
            <p>🎯 500+ Experiences</p>
            <p>⭐ 4.7 Avg. Rating</p>
        </div>
        <div class="developer-box">
            <h3>👨‍💻 Development Team</h3>
            <div class="team-member"><span><strong>Ronit</strong></span><span class="role">Lead Developer</span></div>
            <div class="team-member"><span><strong>Syed</strong></span><span class="role">Backend Engineer</span></div>
            <div class="team-member"><span><strong>Shania</strong></span><span class="role">UI/UX Designer</span></div>
            <div class="team-member"><span><strong>Krishna</strong></span><span class="role">Frontend Developer</span></div>
            <div class="team-member"><span><strong>Khushil</strong></span><span class="role">Data Analyst</span></div>
            <div class="team-member"><span><strong>Vyomika</strong></span><span class="role">QA Engineer</span></div>
            <p style="margin-top:1rem; color:#666; font-size:0.9rem;">Built with ❤️ in Dubai, UAE<br>© 2026 BrandDrop</p>
        </div>
        """, unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div class="footer">
    <h4>BrandDrop - Where Brands Come to Life</h4>
    <p>Discover. Experience. Earn.</p>
    <p style="font-size:0.8rem;">© 2026 BrandDrop. All rights reserved. UAEs First Consumer Experience Marketplace.</p>
</div>
""", unsafe_allow_html=True)
