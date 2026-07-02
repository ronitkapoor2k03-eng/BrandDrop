import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import random
from streamlit_option_menu import option_menu
import folium
from streamlit_folium import st_folium

# Page Configuration
st.set_page_config(
    page_title="BrandDrop - Experience Marketplace",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Global Styles */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .experience-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #e74c3c;
        transition: transform 0.2s;
    }
    .experience-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    .passport-stamp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-block;
        margin: 0.2rem;
    }
    .metric-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #e9ecef;
    }
    .btn-primary {
        background: #e74c3c;
        color: white;
        padding: 0.5rem 2rem;
        border-radius: 25px;
        border: none;
        font-weight: 600;
    }
    .achievement-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .brand-drop-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .feature-box {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin: 0.5rem 0;
        border: 1px solid #e9ecef;
    }
    .developer-credit {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 2rem;
        border-left: 4px solid #e74c3c;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
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
            'Coffee Explorer': 7,
            'Beauty Insider': 4,
            'Food Adventurer': 3,
            'Tech Enthusiast': 2,
            'Fitness Fanatic': 1,
            'Sneaker Hunter': 5,
            'Luxury Seeker': 2
        }
    
    if 'experiences' not in st.session_state:
        st.session_state.experiences = [
            {
                'id': 1,
                'title': 'Matcha Tasting Experience',
                'brand': 'Matcha House',
                'category': 'Food',
                'location': 'Dubai Mall',
                'date': '2026-07-05',
                'time': '10:00 AM',
                'spots': 15,
                'claimed': 12,
                'description': 'Sample premium Japanese matcha and learn the art of traditional tea preparation.',
                'qr_code': 'MT-2026-001',
                'rating': 4.8,
                'reviews': 24
            },
            {
                'id': 2,
                'title': 'Sneaker Launch Event',
                'brand': 'Sole Society',
                'category': 'Fashion',
                'location': 'Mall of Emirates',
                'date': '2026-07-06',
                'time': '2:00 PM',
                'spots': 50,
                'claimed': 35,
                'description': 'Exclusive preview of limited edition sneakers before public release.',
                'qr_code': 'SN-2026-002',
                'rating': 4.6,
                'reviews': 18
            },
            {
                'id': 3,
                'title': 'Skincare Workshop',
                'brand': 'Glow Lab',
                'category': 'Beauty',
                'location': 'City Walk',
                'date': '2026-07-07',
                'time': '11:00 AM',
                'spots': 20,
                'claimed': 8,
                'description': 'Learn about skincare routines and receive personalized product recommendations.',
                'qr_code': 'SK-2026-003',
                'rating': 4.9,
                'reviews': 31
            },
            {
                'id': 4,
                'title': 'Coffee Brewing Masterclass',
                'brand': 'Bean Masters',
                'category': 'Coffee',
                'location': 'Alserkal Avenue',
                'date': '2026-07-08',
                'time': '9:00 AM',
                'spots': 25,
                'claimed': 18,
                'description': 'Master the art of pour-over, espresso, and cold brew techniques.',
                'qr_code': 'CB-2026-004',
                'rating': 4.7,
                'reviews': 42
            },
            {
                'id': 5,
                'title': 'Fitness Challenge',
                'brand': 'FitHub Dubai',
                'category': 'Fitness',
                'location': 'Kite Beach',
                'date': '2026-07-09',
                'time': '6:00 AM',
                'spots': 30,
                'claimed': 22,
                'description': 'Morning HIIT session with professional trainers on the beach.',
                'qr_code': 'FC-2026-005',
                'rating': 4.5,
                'reviews': 15
            },
            {
                'id': 6,
                'title': 'Mystery Gift Drop',
                'brand': 'Mystery Box Co.',
                'category': 'Luxury',
                'location': 'Dubai Marina',
                'date': '2026-07-10',
                'time': '5:00 PM',
                'spots': 10,
                'claimed': 10,
                'description': 'Be one of the first 10 to claim an exclusive mystery gift.',
                'qr_code': 'MG-2026-006',
                'rating': 4.9,
                'reviews': 56
            },
            {
                'id': 7,
                'title': 'Tech Innovation Showcase',
                'brand': 'Dubai Tech Hub',
                'category': 'Tech',
                'location': 'Dubai Internet City',
                'date': '2026-07-11',
                'time': '3:00 PM',
                'spots': 40,
                'claimed': 28,
                'description': 'Experience the latest in AI, VR, and emerging technologies.',
                'qr_code': 'TI-2026-007',
                'rating': 4.7,
                'reviews': 33
            }
        ]
    
    if 'claimed_experiences' not in st.session_state:
        st.session_state.claimed_experiences = [1, 4]
    
    if 'notifications' not in st.session_state:
        st.session_state.notifications = [
            {'message': 'New Matcha experience available', 'read': False},
            {'message': 'You earned 50 points for reviewing', 'read': False}
        ]

init_session_state()

# Sidebar Navigation
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1 style="color: #e74c3c; margin: 0;">BrandDrop</h1>
        <p style="color: #666; margin: 0;">UAE's Experience Marketplace</p>
    </div>
    """, unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title="Navigation",
        options=["Dashboard", "Discover", "My Passport", "Rewards", "For Brands", "Community", "About"],
        icons=["house", "compass", "book", "trophy", "building", "people", "info-circle"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "#e74c3c", "font-size": "20px"},
            "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#e74c3c"},
        }
    )
    
    st.markdown("---")
    st.markdown(f"""
    <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px;">
        <h4>👤 {st.session_state.user['name']}</h4>
        <p>⭐ Level {st.session_state.user['level']}</p>
        <p>🏆 {st.session_state.user['points']} points</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.8rem; color: #666;">
        <p>📱 Version 2.0.0</p>
        <p>🇦🇪 Made in UAE</p>
    </div>
    """, unsafe_allow_html=True)

# Main Content
if selected == "Dashboard":
    # Header
    st.markdown("""
    <div class="brand-drop-header">
        <h1>Welcome to BrandDrop</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">Discover amazing brand experiences happening near you</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-box">
            <h3 style="color: #e74c3c;">12</h3>
            <p>Experiences Attended</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-box">
            <h3 style="color: #e74c3c;">450</h3>
            <p>Total Points Earned</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-box">
            <h3 style="color: #e74c3c;">7</h3>
            <p>Passport Stamps</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-box">
            <h3 style="color: #e74c3c;">24</h3>
            <p>Available Experiences</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Actions
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("🎯 Find Experiences", use_container_width=True)
    with col2:
        st.button("📗 View Passport", use_container_width=True)
    with col3:
        st.button("🏆 Redeem Rewards", use_container_width=True)
    
    st.markdown("---")
    
    # Recommended Experiences
    st.markdown("### 🔥 Recommended For You")
    st.markdown("*Based on your interests and activity*")
    
    # Filter by user interests
    filtered_experiences = [exp for exp in st.session_state.experiences 
                           if exp['category'].lower() in [i.lower() for i in st.session_state.user['interests']]]
    
    cols = st.columns(3)
    for idx, exp in enumerate(filtered_experiences[:3]):
        with cols[idx]:
            with st.container():
                availability = exp['spots'] - exp['claimed']
                progress = (exp['claimed'] / exp['spots']) * 100
                st.markdown(f"""
                <div class="experience-card">
                    <h4>{exp['title']}</h4>
                    <p style="color: #e74c3c; font-weight: 600;">{exp['brand']}</p>
                    <p>📍 {exp['location']}</p>
                    <p>📅 {exp['date']} at {exp['time']}</p>
                    <div style="background: #e9ecef; height: 6px; border-radius: 3px; margin: 0.5rem 0;">
                        <div style="background: #e74c3c; width: {progress}%; height: 6px; border-radius: 3px;"></div>
                    </div>
                    <p>🎯 {availability} spots remaining</p>
                    <p style="font-size: 0.85rem; color: #666;">⭐ {exp['rating']} ({exp['reviews']} reviews)</p>
                </div>
                """, unsafe_allow_html=True)
                if availability > 0:
                    if st.button(f"Reserve Now", key=f"dash_reserve_{exp['id']}"):
                        st.success(f"✅ Reserved! QR: {exp['qr_code']}")
                        st.balloons()
    
    # Passport Progress
    st.markdown("---")
    st.markdown("### 📗 Experience Passport Progress")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        for category, count in st.session_state.passport.items():
            progress = min(count / 10, 1)
            st.markdown(f"**{category}**")
            st.progress(progress)
            st.markdown(f"*{count}/10 experiences completed*")
            st.markdown("")
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 10px; color: white;">
            <h4>🏆 Next Achievement</h4>
            <p><strong>Food Adventurer:</strong> Visit 10 restaurants</p>
            <p>Progress: 3/10</p>
            <p style="font-size: 0.9rem;">Unlock exclusive dining experiences</p>
        </div>
        """, unsafe_allow_html=True)

elif selected == "Discover":
    st.markdown("""
    <div class="brand-drop-header">
        <h1>Discover Experiences</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">Find brand experiences happening near you</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        category_filter = st.selectbox(
            "Category",
            ["All", "Beauty", "Fashion", "Food", "Coffee", "Fitness", "Tech", "Luxury", "Gaming"]
        )
    with col2:
        date_filter = st.date_input("Date", datetime.now())
    with col3:
        location_filter = st.text_input("Location", "Dubai")
    with col4:
        sort_by = st.selectbox("Sort By", ["Relevance", "Date", "Rating", "Availability"])
    
    # Map View
    st.markdown("### 📍 Interactive Map")
    m = folium.Map(location=[25.2048, 55.2708], zoom_start=12)
    
    # Add experience markers with different colors
    colors = {'Food': 'green', 'Fashion': 'red', 'Beauty': 'pink', 'Coffee': 'darkgreen', 
              'Fitness': 'orange', 'Tech': 'blue', 'Luxury': 'purple', 'Gaming': 'cadetblue'}
    
    for exp in st.session_state.experiences:
        folium.Marker(
            location=[25.2048 + random.uniform(-0.02, 0.02), 55.2708 + random.uniform(-0.02, 0.02)],
            popup=f"""
            <b>{exp['title']}</b><br>
            {exp['brand']}<br>
            📍 {exp['location']}<br>
            📅 {exp['date']}<br>
            🎯 {exp['spots'] - exp['claimed']} spots left
            """,
            tooltip=f"{exp['title']} - {exp['brand']}",
            icon=folium.Icon(color=colors.get(exp['category'], 'blue'), icon='info-sign')
        ).add_to(m)
    
    st_data = st_folium(m, width=725, height=400)
    
    # Experience List
    st.markdown("### 📋 Available Experiences")
    
    filtered_exps = st.session_state.experiences
    if category_filter != "All":
        filtered_exps = [exp for exp in filtered_exps if exp['category'] == category_filter]
    
    for exp in filtered_exps:
        availability = exp['spots'] - exp['claimed']
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
            with col1:
                st.markdown(f"""
                <div style="border-left: 4px solid #e74c3c; padding-left: 1rem; margin: 0.5rem 0;">
                    <h4>{exp['title']}</h4>
                    <p style="color: #e74c3c; font-weight: 500;">{exp['brand']} • {exp['category']}</p>
                    <p>📍 {exp['location']} • 📅 {exp['date']} at {exp['time']}</p>
                    <p style="font-size: 0.9rem;">{exp['description']}</p>
                    <p>⭐ {exp['rating']} ({exp['reviews']} reviews)</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div style="margin-top: 1rem;">
                    <p>Available: <strong>{availability}</strong> spots</p>
                    <div style="background: #e9ecef; height: 6px; border-radius: 3px;">
                        <div style="background: #e74c3c; width: {(exp['claimed']/exp['spots']*100)}%; height: 6px; border-radius: 3px;"></div>
                    </div>
                    <p style="font-size: 0.8rem; color: #666;">{exp['claimed']}/{exp['spots']} claimed</p>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                if st.button(f"📱 View Details", key=f"view_{exp['id']}"):
                    st.info(f"QR Code: {exp['qr_code']}\nExperience ID: {exp['id']}")
            with col4:
                if availability > 0:
                    if st.button(f"🔴 Reserve", key=f"claim_{exp['id']}"):
                        st.success("✅ Experience reserved! Check your Passport.")
                        st.balloons()
                        st.session_state.claimed_experiences.append(exp['id'])
                else:
                    st.markdown("🔴 **Fully Booked**")

elif selected == "My Passport":
    st.markdown("""
    <div class="brand-drop-header">
        <h1>My Experience Passport</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">Collect stamps and unlock achievements</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-box">
            <h2 style="color: #e74c3c;">12</h2>
            <p>Total Experiences</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-box">
            <h2 style="color: #e74c3c;">5</h2>
            <p>Active Categories</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-box">
            <h2 style="color: #e74c3c;">3</h2>
            <p>Achievements Unlocked</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Passport Stamps
    st.markdown("### ✨ Your Passport Stamps")
    
    col1, col2 = st.columns(2)
    with col1:
        for category, count in list(st.session_state.passport.items())[:4]:
            progress = min(count / 10, 1)
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;">
                <span class="passport-stamp">{category}</span>
                <p style="margin-top: 0.5rem;">Progress: {count}/10</p>
                <div style="background: #e9ecef; height: 8px; border-radius: 4px;">
                    <div style="background: linear-gradient(90deg, #667eea, #764ba2); 
                                width: {progress*100}%; height: 8px; border-radius: 4px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        for category, count in list(st.session_state.passport.items())[4:]:
            progress = min(count / 10, 1)
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;">
                <span class="passport-stamp">{category}</span>
                <p style="margin-top: 0.5rem;">Progress: {count}/10</p>
                <div style="background: #e9ecef; height: 8px; border-radius: 4px;">
                    <div style="background: linear-gradient(90deg, #667eea, #764ba2); 
                                width: {progress*100}%; height: 8px; border-radius: 4px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Unlocked Achievements
    st.markdown("---")
    st.markdown("### 🏆 Unlocked Achievements")
    
    achievements = [
        {"name": "Coffee Explorer", "description": "Visit 10 independent cafés", "unlocked": st.session_state.passport.get('Coffee Explorer', 0) >= 10},
        {"name": "Beauty Insider", "description": "Attend 5 beauty launches", "unlocked": st.session_state.passport.get('Beauty Insider', 0) >= 5},
        {"name": "Dubai Explorer", "description": "Complete experiences across 5 malls", "unlocked": True},
        {"name": "Sneaker Hunter", "description": "Attend 3 sneaker launches", "unlocked": st.session_state.passport.get('Sneaker Hunter', 0) >= 3},
        {"name": "Fitness Fanatic", "description": "Complete 5 fitness challenges", "unlocked": st.session_state.passport.get('Fitness Fanatic', 0) >= 5}
    ]
    
    for achievement in achievements:
        if achievement['unlocked']:
            st.markdown(f"""
            <div class="achievement-card">
                <h4>✅ {achievement['name']}</h4>
                <p>{achievement['description']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: #f1f3f5; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; opacity: 0.6;">
                <h4>🔒 {achievement['name']}</h4>
                <p>{achievement['description']}</p>
            </div>
            """, unsafe_allow_html=True)

elif selected == "Rewards":
    st.markdown("""
    <div class="brand-drop-header">
        <h1>Rewards & Benefits</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">Redeem your points for exclusive experiences and merchandise</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Points Balance
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-box">
            <h1 style="color: #e74c3c;">450</h1>
            <p>Available Points</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-box">
            <h1 style="color: #e74c3c;">Level 3</h1>
            <p>Member Status</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-box">
            <h1 style="color: #e74c3c;">200</h1>
            <p>Points to Next Level</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Reward Catalog
    st.markdown("### 🎁 Reward Catalog")
    
    rewards = [
        {"name": "AED 50 Gift Card", "points": 200, "category": "Gift Cards"},
        {"name": "Movie Tickets (2)", "points": 150, "category": "Entertainment"},
        {"name": "Exclusive Event Invite", "points": 300, "category": "Experiences"},
        {"name": "Brand Merchandise", "points": 250, "category": "Merchandise"},
        {"name": "Premium Coffee Tasting", "points": 180, "category": "Experiences"},
        {"name": "Spa Voucher", "points": 350, "category": "Wellness"}
    ]
    
    for reward in rewards:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"**{reward['name']}**")
            st.markdown(f"*{reward['category']}*")
        with col2:
            st.markdown(f"**{reward['points']} points**")
        with col3:
            if st.button(f"Redeem", key=f"redeem_{reward['name']}"):
                if st.session_state.user['points'] >= reward['points']:
                    st.success(f"✅ Redeemed: {reward['name']}")
                    st.session_state.user['points'] -= reward['points']
                else:
                    st.error("❌ Insufficient points")

elif selected == "For Brands":
    st.markdown("""
    <div class="brand-drop-header">
        <h1>For Brands</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">Launch campaigns and measure real engagement</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Brand Dashboard
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-box">
            <h3 style="color: #e74c3c;">1,247</h3>
            <p>Total Attendees</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-box">
            <h3 style="color: #e74c3c;">12</h3>
            <p>Active Campaigns</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-box">
            <h3 style="color: #e74c3c;">87%</h3>
            <p>Avg. Redemption Rate</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-box">
            <h3 style="color: #e74c3c;">4.7</h3>
            <p>Avg. Rating</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Campaign Creation
    st.markdown("### 🚀 Create New Campaign")
    
    with st.form("campaign_creation"):
        col1, col2 = st.columns(2)
        with col1:
            campaign_name = st.text_input("Campaign Name", "Summer Launch 2026")
            brand_name = st.text_input("Brand Name", "BrandDrop Official")
            category = st.selectbox("Category", ["Beauty", "Fashion", "Food", "Coffee", "Fitness", "Tech", "Luxury"])
            location = st.text_input("Location", "Dubai Mall")
        
        with col2:
            start_date = st.date_input("Start Date", datetime.now())
            end_date = st.date_input("End Date", datetime.now() + timedelta(days=7))
            capacity = st.number_input("Capacity", min_value=10, max_value=500, value=50)
            budget = st.number_input("Budget (AED)", min_value=1000, value=5000)
        
        target_audience = st.multiselect(
            "Target Audience",
            ["Beauty Club", "Coffee Club", "Sneaker Club", "Pet Club", 
             "Parents Club", "Foodies Club", "Gamers Club", "Fitness Club"]
        )
        
        rewards_offered = st.text_area("Rewards Offered", "Exclusive samples, VIP access, merchandise")
        
        submitted = st.form_submit_button("Launch Campaign", type="primary")
        if submitted:
            st.success("✅ Campaign created successfully! Your experience is now live.")
            st.balloons()
    
    st.markdown("---")
    
    # Analytics
    st.markdown("### 📊 Campaign Performance")
    
    # Sample data for chart
    df = pd.DataFrame({
        'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        'Reservations': [45, 67, 89, 102],
        'Attendees': [38, 55, 72, 85],
        'Redemptions': [30, 48, 61, 72]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Week'], y=df['Reservations'], name='Reservations', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=df['Week'], y=df['Attendees'], name='Attendees', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=df['Week'], y=df['Redemptions'], name='Redemptions', mode='lines+markers'))
    fig.update_layout(
        title='Campaign Performance Trends',
        xaxis_title='Time Period',
        yaxis_title='Number of Users',
        height=400,
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True)

elif selected == "Community":
    st.markdown("""
    <div class="brand-drop-header">
        <h1>Community</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">Join clubs and connect with like-minded enthusiasts</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Community Clubs
    col1, col2, col3 = st.columns(3)
    
    clubs = [
        {"name": "☕ Coffee Club", "members": 234, "events": 12, "description": "For coffee lovers and enthusiasts"},
        {"name": "💄 Beauty Club", "members": 189, "events": 9, "description": "Skincare, makeup, and wellness"},
        {"name": "👟 Sneaker Club", "members": 156, "events": 7, "description": "Limited editions and releases"},
        {"name": "🐾 Pet Club", "members": 98, "events": 5, "description": "Pet-friendly experiences"},
        {"name": "🍽️ Foodies Club", "members": 312, "events": 15, "description": "Culinary adventures and tastings"},
        {"name": "🎮 Gamers Club", "members": 145, "events": 8, "description": "Gaming tournaments and events"}
    ]
    
    for idx, club in enumerate(clubs):
        with [col1, col2, col3][idx % 3]:
            st.markdown(f"""
            <div class="feature-box">
                <h3>{club['name']}</h3>
                <p>{club['description']}</p>
                <p>👥 {club['members']} members</p>
                <p>🎯 {club['events']} upcoming events</p>
                <button style="background: #e74c3c; color: white; padding: 0.3rem 1rem; border: none; border-radius: 15px; cursor: pointer;">
                    Join Club
                </button>
            </div>
            """, unsafe_allow_html=True)

elif selected == "About":
    st.markdown("""
    <div class="brand-drop-header">
        <h1>About BrandDrop</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">UAE's First Consumer Experience Marketplace</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Our Mission
        BrandDrop is revolutionizing how brands connect with consumers in the UAE. 
        We're replacing traditional advertising with real-world experiences that create 
        meaningful connections and measurable engagement.
        
        ### The Problem We Solve
        - ❌ Consumers skip ads and ignore influencer promotions
        - ❌ Brands waste budget on activations without measurable ROI
        - ❌ Exciting brand experiences are scattered across multiple platforms
        - ❌ No single platform exists for discovering and booking brand experiences
        
        ### Our Solution
        - ✅ Single platform for discovering, booking, and engaging with brand experiences
        - ✅ Measurable engagement instead of just impressions
        - ✅ Experience Passport with achievements and rewards
        - ✅ Real-time analytics for brands to track campaign performance
        
        ### Why UAE?
        - 🇦🇪 Retail- and mall-driven culture
        - 🇦🇪 Frequent product launches and brand activations
        - 🇦🇪 Large tourism volumes
        - 🇦🇪 Digitally connected population
        - 🇦🇪 Strong government support for innovation
        """)
    
    with col2:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px;">
            <h3>📊 Key Metrics</h3>
            <p>👥 5,000+ Users</p>
            <p>🏢 200+ Brands</p>
            <p>🎯 500+ Experiences</p>
            <p>⭐ 4.7 Avg. Rating</p>
        </div>
        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin-top: 1rem;">
            <h3>📱 Version</h3>
            <p>v2.0.0</p>
            <p>Released: July 2026</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div class="developer-credit">
        <h3>👨‍💻 Development Team</h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1rem;">
            <div>
                <strong>Ronit Kapoor</strong>
                <p style="color: #666; font-size: 0.9rem;">Lead Developer</p>
            </div>
            <div>
                <strong>Syed Ali</strong>
                <p style="color: #666; font-size: 0.9rem;">Backend Engineer</p>
            </div>
            <div>
                <strong>Shania Ahmed</strong>
                <p style="color: #666; font-size: 0.9rem;">UI/UX Designer</p>
            </div>
            <div>
                <strong>Krishna Patel</strong>
                <p style="color: #666; font-size: 0.9rem;">Frontend Developer</p>
            </div>
            <div>
                <strong>Khushil Sharma</strong>
                <p style="color: #666; font-size: 0.9rem;">Data Analyst</p>
            </div>
            <div>
                <strong>Vyomika Reddy</strong>
                <p style="color: #666; font-size: 0.9rem;">QA Engineer</p>
            </div>
        </div>
        <p style="margin-top: 1rem; color: #666; font-size: 0.9rem;">
            Built with ❤️ in Dubai, UAE | © 2026 BrandDrop
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <h4>BrandDrop - Where Brands Come to Life</h4>
    <p>Discover. Experience. Earn.</p>
    <p style="font-size: 0.8rem;">© 2026 BrandDrop. All rights reserved. UAE's First Consumer Experience Marketplace.</p>
</div>
""", unsafe_allow_html=True)
