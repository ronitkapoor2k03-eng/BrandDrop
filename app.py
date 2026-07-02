import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# PAGE CONFIGURATION
st.set_page_config(
    page_title="BrandDrop - Experience Marketplace",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS + LIVE TIMER JAVASCRIPT
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
    }
    
    .hero-section {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 3rem 3rem;
        border-radius: 24px;
        color: white;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 60%;
        height: 200%;
        background: radial-gradient(circle, rgba(231, 76, 60, 0.15) 0%, transparent 70%);
        transform: rotate(15deg);
    }
    
    .hero-section h1 {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff 0%, #e74c3c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        position: relative;
        z-index: 1;
    }
    
    .hero-section .subtitle {
        font-size: 1.3rem;
        opacity: 0.9;
        margin: 0.5rem 0 0 0;
        position: relative;
        z-index: 1;
    }
    
    .hero-section .tagline {
        font-size: 1rem;
        opacity: 0.6;
        margin-top: 0.3rem;
        font-style: italic;
        position: relative;
        z-index: 1;
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(231, 76, 60, 0.3);
        border: 1px solid rgba(231, 76, 60, 0.5);
        padding: 0.3rem 1.2rem;
        border-radius: 50px;
        font-size: 0.8rem;
        color: #e74c3c;
        font-weight: 600;
        position: relative;
        z-index: 1;
    }
    
    .experience-card-enhanced {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        margin-bottom: 1rem;
        border-left: 5px solid #e74c3c;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .experience-card-enhanced:hover {
        transform: translateY(-8px) scale(1.01);
        box-shadow: 0 12px 40px rgba(231, 76, 60, 0.15);
    }
    
    .experience-card-enhanced .badge-type {
        display: inline-block;
        background: #e74c3c;
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 50px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .experience-card-enhanced .full-description {
        color: #444;
        font-size: 0.9rem;
        margin: 0.5rem 0;
        line-height: 1.6;
    }
    
    .metric-card-enhanced {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.3);
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }
    
    .metric-card-enhanced:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .metric-card-enhanced .icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .metric-card-enhanced h2, .metric-card-enhanced h3 {
        color: #1a1a2e;
        margin: 0;
        font-weight: 800;
    }
    
    .metric-card-enhanced .label {
        color: #666;
        font-size: 0.9rem;
        margin: 0.3rem 0 0 0;
        font-weight: 500;
    }
    
    /* LIVE COUNTDOWN TIMER STYLES */
    .countdown-wrapper {
        display: flex;
        align-items: center;
        gap: 1.5rem;
        flex-wrap: wrap;
        margin-top: 1rem;
        position: relative;
        z-index: 1;
    }
    
    .countdown-timer {
        background: rgba(26, 26, 46, 0.95);
        padding: 1rem 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        display: inline-block;
        border: 2px solid rgba(231, 76, 60, 0.3);
        min-width: 220px;
        box-shadow: 0 0 30px rgba(231, 76, 60, 0.1);
    }
    
    .countdown-timer .time {
        font-size: 2.8rem;
        font-weight: 700;
        color: #e74c3c;
        font-variant-numeric: tabular-nums;
        letter-spacing: 3px;
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 20px rgba(231, 76, 60, 0.3);
    }
    
    .countdown-timer .label {
        font-size: 0.7rem;
        opacity: 0.6;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 0.2rem;
    }
    
    .live-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: #e74c3c;
        color: white;
        padding: 0.5rem 1.2rem;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        box-shadow: 0 0 30px rgba(231, 76, 60, 0.3);
        animation: pulse-glow 2s infinite;
    }
    
    @keyframes pulse-glow {
        0% { box-shadow: 0 0 20px rgba(231, 76, 60, 0.3); }
        50% { box-shadow: 0 0 40px rgba(231, 76, 60, 0.6); }
        100% { box-shadow: 0 0 20px rgba(231, 76, 60, 0.3); }
    }
    
    .live-dot {
        width: 10px;
        height: 10px;
        background: white;
        border-radius: 50%;
        display: inline-block;
        animation: pulse-dot 1s infinite;
    }
    
    @keyframes pulse-dot {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.8); opacity: 0.5; }
        100% { transform: scale(1); opacity: 1; }
    }
    
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
    
    .achievement-locked h4, .achievement-unlocked h4 {
        margin: 0;
    }
    
    .achievement-locked p, .achievement-unlocked p {
        margin: 0;
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
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
    
    .club-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    }
    
    .club-card h3 {
        margin: 0.5rem 0;
        color: #1a1a2e;
    }
    
    .club-card .member-count {
        color: #666;
        font-size: 0.9rem;
    }
    
    .club-card .event-count {
        color: #e74c3c;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .developer-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #e74c3c;
        margin-top: 1rem;
    }
    
    .developer-box h3 {
        margin-top: 0;
        color: #1a1a2e;
    }
    
    .developer-box .team-member {
        display: flex;
        justify-content: space-between;
        padding: 0.3rem 0;
        border-bottom: 1px solid #e9ecef;
    }
    
    .developer-box .team-member:last-child {
        border-bottom: none;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #e74c3c, #c0392b);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(231, 76, 60, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(231, 76, 60, 0.4);
    }
    
    .sidebar-header {
        text-align: center;
        padding: 1rem 0;
    }
    
    .sidebar-header h1 {
        color: #e74c3c;
        margin: 0;
        font-size: 1.8rem;
    }
    
    .sidebar-header p {
        color: #666;
        margin: 0;
        font-size: 0.85rem;
    }
    
    .sidebar-user {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .sidebar-user p {
        margin: 0.2rem 0;
    }
    
    .sidebar-user .name {
        font-weight: 600;
        color: #1a1a2e;
    }
    
    .sidebar-user .points {
        color: #e74c3c;
        font-weight: 600;
    }
    
    .sidebar-profile .avatar-large {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: linear-gradient(135deg, #e74c3c, #f39c12);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        color: white;
        margin: 0 auto 0.5rem auto;
        box-shadow: 0 4px 16px rgba(231, 76, 60, 0.3);
    }
    
    .sidebar-profile .name {
        font-weight: 700;
        color: #1a1a2e;
        font-size: 1.1rem;
    }
    
    .sidebar-profile .level {
        color: #666;
        font-size: 0.85rem;
    }
    
    .sidebar-profile .points {
        color: #e74c3c;
        font-weight: 700;
        font-size: 1.2rem;
    }
    
    .footer-enhanced {
        text-align: center;
        padding: 2rem 0 1rem 0;
        border-top: 1px solid rgba(0,0,0,0.05);
        margin-top: 2rem;
    }
    
    .footer-enhanced .brand {
        font-size: 1.5rem;
        font-weight: 800;
        color: #1a1a2e;
    }
    
    .footer-enhanced .brand span {
        color: #e74c3c;
    }
    
    .footer-enhanced .tagline {
        color: #666;
        font-size: 0.9rem;
    }
    
    .divider-glow {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #e74c3c, transparent);
        margin: 2rem 0;
        opacity: 0.3;
    }
    
    .notification-bell {
        background: #e74c3c;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .full-description-text {
        color: #444;
        font-size: 0.95rem;
        line-height: 1.7;
        margin: 0.5rem 0;
    }
    
    .testimonial-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        border: 1px solid rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .testimonial-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .testimonial-card .avatar {
        width: 70px;
        height: 70px;
        border-radius: 50%;
        background: linear-gradient(135deg, #e74c3c, #f39c12);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        color: white;
        margin: 0 auto 1rem auto;
        box-shadow: 0 4px 12px rgba(231, 76, 60, 0.3);
    }
    
    .testimonial-card .quote {
        font-size: 1rem;
        color: #444;
        line-height: 1.6;
        font-style: italic;
    }
    
    .testimonial-card .author {
        font-weight: 700;
        color: #1a1a2e;
        margin-top: 0.5rem;
    }
    
    .testimonial-card .role-text {
        color: #666;
        font-size: 0.85rem;
    }
    
    .testimonial-card .stars {
        color: #f39c12;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    
    .stats-bar {
        display: flex;
        justify-content: space-around;
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(10px);
        padding: 1rem 2rem;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.3);
        margin: 1rem 0;
    }
    
    .stats-bar .stat-item {
        text-align: center;
    }
    
    .stats-bar .stat-number {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1a1a2e;
    }
    
    .stats-bar .stat-label {
        font-size: 0.8rem;
        color: #666;
    }
</style>

<!-- LIVE COUNTDOWN TIMER JAVASCRIPT - UPDATES EVERY SECOND -->
<script>
    function startCountdown() {
        function updateTimer() {
            var now = new Date();
            var target = new Date(now);
            target.setHours(12, 0, 0, 0); // Next drop at 12:00 PM
            
            if (now > target) {
                target.setDate(target.getDate() + 1);
            }
            
            var diff = target - now;
            var hours = Math.floor(diff / 3600000);
            var minutes = Math.floor((diff % 3600000) / 60000);
            var seconds = Math.floor((diff % 60000) / 1000);
            
            var timeStr = String(hours).padStart(2, '0') + ':' + 
                         String(minutes).padStart(2, '0') + ':' + 
                         String(seconds).padStart(2, '0');
            
            var timerElement = document.getElementById('countdown-time');
            if (timerElement) {
                timerElement.textContent = timeStr;
            }
        }
        
        updateTimer();
        setInterval(updateTimer, 1000);
    }
    
    // Start the timer when the page loads
    document.addEventListener('DOMContentLoaded', startCountdown);
    // Also start if DOM already loaded
    if (document.readyState === 'complete' || document.readyState === 'interactive') {
        startCountdown();
    }
</script>
""", unsafe_allow_html=True)

# ============================================
# INITIALIZE SESSION STATE
# ============================================
def init_session_state():
    if 'user' not in st.session_state:
        st.session_state.user = {
            'name': 'Ahmed Al Maktoum',
            'email': 'ahmed@example.com',
            'points': 450,
            'level': 3,
            'interests': ['Coffee', 'Fashion', 'Tech', 'Food'],
            'join_date': 'January 2026'
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
            {'id': 1, 'title': 'Matcha Tasting Experience', 'brand': 'Matcha House', 'category': 'Food', 'location': 'Dubai Mall', 'date': '2026-07-05', 'time': '10:00 AM', 'spots': 15, 'claimed': 12, 'description': 'Sample premium Japanese matcha and learn the art of traditional tea preparation. Experience the rich flavors of ceremonial grade matcha.', 'qr_code': 'MT-2026-001', 'rating': 4.8, 'reviews': 24, 'type': 'Product Sampling', 'image': '🍵', 'featured': True},
            {'id': 2, 'title': 'Sneaker Launch Event', 'brand': 'Sole Society', 'category': 'Fashion', 'location': 'Mall of Emirates', 'date': '2026-07-06', 'time': '2:00 PM', 'spots': 50, 'claimed': 35, 'description': 'Exclusive preview of limited edition sneakers before public release. Be the first to see and purchase the most anticipated drop of the year.', 'qr_code': 'SN-2026-002', 'rating': 4.6, 'reviews': 18, 'type': 'Product Launch', 'image': '👟', 'featured': True},
            {'id': 3, 'title': 'Skincare Workshop', 'brand': 'Glow Lab', 'category': 'Beauty', 'location': 'City Walk', 'date': '2026-07-07', 'time': '11:00 AM', 'spots': 20, 'claimed': 8, 'description': 'Learn about skincare routines and receive personalized product recommendations. Discover your skin type and build the perfect routine.', 'qr_code': 'SK-2026-003', 'rating': 4.9, 'reviews': 31, 'type': 'Workshop', 'image': '✨', 'featured': True},
            {'id': 4, 'title': 'Coffee Brewing Masterclass', 'brand': 'Bean Masters', 'category': 'Coffee', 'location': 'Alserkal Avenue', 'date': '2026-07-08', 'time': '9:00 AM', 'spots': 25, 'claimed': 18, 'description': 'Master the art of pour-over, espresso, and cold brew techniques. Learn from certified baristas and taste the difference.', 'qr_code': 'CB-2026-004', 'rating': 4.7, 'reviews': 42, 'type': 'Workshop', 'image': '☕', 'featured': False},
            {'id': 5, 'title': 'Beach Fitness Challenge', 'brand': 'FitHub Dubai', 'category': 'Fitness', 'location': 'Kite Beach', 'date': '2026-07-09', 'time': '6:00 AM', 'spots': 30, 'claimed': 22, 'description': 'Morning HIIT session with professional trainers on the beach. Start your day with energy and achieve your fitness goals.', 'qr_code': 'FC-2026-005', 'rating': 4.5, 'reviews': 15, 'type': 'Community Challenge', 'image': '🏋️', 'featured': False},
            {'id': 6, 'title': 'Mystery Gift Drop', 'brand': 'Mystery Box Co.', 'category': 'Luxury', 'location': 'Dubai Marina', 'date': '2026-07-10', 'time': '5:00 PM', 'spots': 10, 'claimed': 10, 'description': 'Be one of the first 10 to claim an exclusive mystery gift. Curious? That\'s the point. Each box contains luxury items worth up to AED 500.', 'qr_code': 'MG-2026-006', 'rating': 4.9, 'reviews': 56, 'type': 'Mystery Drop', 'image': '🎁', 'featured': True},
            {'id': 7, 'title': 'Tech Innovation Showcase', 'brand': 'Dubai Tech Hub', 'category': 'Tech', 'location': 'Dubai Internet City', 'date': '2026-07-11', 'time': '3:00 PM', 'spots': 40, 'claimed': 28, 'description': 'Experience the latest in AI, VR, and emerging technologies. Interactive demos and hands-on workshops with industry experts.', 'qr_code': 'TI-2026-007', 'rating': 4.7, 'reviews': 33, 'type': 'Product Launch', 'image': '💻', 'featured': False},
            {'id': 8, 'title': 'Emirati Cuisine Trail', 'brand': 'Taste of UAE', 'category': 'Food', 'location': 'Various Locations', 'date': '2026-07-12', 'time': '12:00 PM', 'spots': 20, 'claimed': 5, 'description': 'Explore authentic Emirati restaurants across Dubai. Collect stamps at each location and earn a special culinary reward.', 'qr_code': 'EC-2026-008', 'rating': 4.8, 'reviews': 12, 'type': 'Community Challenge', 'image': '🍽️', 'featured': False}
        ]
    
    if 'claimed_experiences' not in st.session_state:
        st.session_state.claimed_experiences = [1, 4, 7]
    
    if 'reviews' not in st.session_state:
        st.session_state.reviews = {}
    
    if 'notifications' not in st.session_state:
        st.session_state.notifications = [
            {'message': '🎯 New Matcha experience available at Dubai Mall!', 'time': '2 min ago', 'read': False},
            {'message': '⭐ You earned 50 points for reviewing Sneaker Launch!', 'time': '1 hour ago', 'read': False},
            {'message': '🏆 You unlocked Sneaker Hunter achievement!', 'time': '3 hours ago', 'read': False}
        ]
    
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
    
    if 'testimonials' not in st.session_state:
        st.session_state.testimonials = [
            {'name': 'Sara', 'role': 'Beauty Enthusiast', 'quote': 'BrandDrop has completely changed how I discover new products. I have attended 5 exclusive launches this month!', 'stars': 5, 'avatar': '💄'},
            {'name': 'Mohammed', 'role': 'Coffee Lover', 'quote': 'The Coffee Brewing Masterclass was incredible. I learned techniques I never knew existed!', 'stars': 5, 'avatar': '☕'},
            {'name': 'Fatima', 'role': 'Fashion Influencer', 'quote': 'I discovered the Sneaker Launch event through BrandDrop. The VIP access was a game-changer!', 'stars': 4, 'avatar': '👗'},
            {'name': 'Khalid', 'role': 'Tech Enthusiast', 'quote': 'The Tech Innovation Showcase was mind-blowing. Got to try VR and AI demos before anyone else.', 'stars': 5, 'avatar': '💻'}
        ]

init_session_state()

# ============================================
# SIDEBAR NAVIGATION
# ============================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-profile">
        <div class="avatar-large">👤</div>
        <div class="name">{}</div>
        <div class="level">⭐ Level {} • Member since {}</div>
        <div class="points">🏆 {} points</div>
    </div>
    """.format(
        st.session_state.user['name'],
        st.session_state.user['level'],
        st.session_state.user['join_date'],
        st.session_state.user['points']
    ), unsafe_allow_html=True)
    
    st.markdown("---")
    
    menu = st.radio(
        "Navigate",
        ["Dashboard", "Discover", "Passport", "Rewards", "Clubs", "For Brands", "Testimonials", "About"],
        key="main_menu",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Live Stats in Sidebar
    st.markdown("""
    <div style="background:rgba(255,255,255,0.1); padding:1rem; border-radius:12px; border:1px solid rgba(255,255,255,0.1);">
        <div style="display:flex; justify-content:space-between;">
            <div><span style="color:#666;">👥</span><br><span style="font-weight:700; color:#1a1a2e;">5,247</span></div>
            <div><span style="color:#666;">🎯</span><br><span style="font-weight:700; color:#1a1a2e;">287</span></div>
            <div><span style="color:#666;">⭐</span><br><span style="font-weight:700; color:#1a1a2e;">4.7</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    unread = sum(1 for n in st.session_state.notifications if not n['read'])
    st.markdown(f"""
    <div style="text-align:center;">
        <div class="notification-bell">
            🔔 {unread} New Notification{'' if unread == 1 else 's'}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<div style="font-size:0.75rem; color:#999; text-align:center;"><p>📱 v2.0.0</p><p>🇦🇪 Made in UAE</p></div>', unsafe_allow_html=True)

# ============================================
# DASHBOARD - WITH LIVE COUNTDOWN TIMER
# ============================================
if menu == "Dashboard":
    st.markdown("""
    <div class="hero-section">
        <div class="hero-badge">🚀 LIVE NOW</div>
        <h1>Welcome to BrandDrop</h1>
        <p class="subtitle">UAE's First Consumer Experience Marketplace</p>
        <p class="tagline">"Discover. Experience. Earn." — Where brands come to life.</p>
        
        <div class="countdown-wrapper">
            <div class="countdown-timer">
                <div class="time" id="countdown-time">12:00:00</div>
                <div class="label">⏰ Next Experience Drops In</div>
            </div>
            <div class="live-indicator">
                <span class="live-dot"></span> Live Now
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        attended = len(st.session_state.claimed_experiences)
        st.markdown(f"""
        <div class="metric-card-enhanced">
            <div class="icon">🎯</div>
            <h3>{attended}</h3>
            <p class="label">Experiences Attended</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card-enhanced">
            <div class="icon">🏆</div>
            <h3>{st.session_state.user['points']}</h3>
            <p class="label">Total Points Earned</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        unlocked = sum(1 for v in st.session_state.passport.values() if v['unlocked'])
        total = len(st.session_state.passport)
        st.markdown(f"""
        <div class="metric-card-enhanced">
            <div class="icon">📗</div>
            <h3>{unlocked}/{total}</h3>
            <p class="label">Passport Stamps</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        available = len(st.session_state.experiences)
        st.markdown(f"""
        <div class="metric-card-enhanced">
            <div class="icon">🔥</div>
            <h3>{available}</h3>
            <p class="label">Available Experiences</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr class='divider-glow'>", unsafe_allow_html=True)
    
    # Stats Bar
    st.markdown("""
    <div class="stats-bar">
        <div class="stat-item">
            <div class="stat-number">5,247</div>
            <div class="stat-label">Total Users</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">287</div>
            <div class="stat-label">Active Brands</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">1,432</div>
            <div class="stat-label">Experiences Created</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">4.7</div>
            <div class="stat-label">Avg. Rating</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr class='divider-glow'>", unsafe_allow_html=True)
    
    # Featured Experiences with FULL description
    st.markdown("### 🔥 Featured Experiences")
    st.markdown("*Curated experiences based on your interests*")
    
    featured = [exp for exp in st.session_state.experiences if exp.get('featured', False)]
    if not featured:
        featured = st.session_state.experiences[:3]
    
    cols = st.columns(3)
    for idx, exp in enumerate(featured[:3]):
        with cols[idx]:
            available = exp['spots'] - exp['claimed']
            progress = (exp['claimed'] / exp['spots']) * 100 if exp['spots'] > 0 else 0
            st.markdown(f"""
            <div class="experience-card-enhanced">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <span style="font-size:2.5rem;">{exp.get('image', '🎯')}</span>
                    <span class="badge-type">{exp['type']}</span>
                </div>
                <h4 style="margin:0.5rem 0 0 0;">{exp['title']}</h4>
                <p class="brand-name" style="color:#e74c3c; font-weight:600;">{exp['brand']}</p>
                <p class="meta" style="color:#666; font-size:0.9rem;">📍 {exp['location']} • 📅 {exp['date']}</p>
                <p class="meta" style="color:#666; font-size:0.9rem;">⏰ {exp['time']}</p>
                <div class="full-description-text">{exp['description']}</div>
                <div class="progress-container">
                    <div class="progress-fill" style="width:{progress}%;"></div>
                </div>
                <p class="spots" style="font-weight:600; color:#2ecc71;">{available} spots remaining</p>
                <p class="rating" style="color:#f39c12; font-weight:600;">⭐ {exp['rating']} ({exp['reviews']} reviews)</p>
            </div>
            """, unsafe_allow_html=True)
            
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
    
    st.markdown("<hr class='divider-glow'>", unsafe_allow_html=True)
    
    # Passport Progress
    st.markdown("### 📗 Experience Passport Progress")
    st.markdown("*Collect stamps and unlock achievements*")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        for idx, (category, data) in enumerate(list(st.session_state.passport.items())[:4]):
            progress = min(data['count'] / data['target'], 1)
            status = "✅" if data['unlocked'] else "🔒"
            st.markdown(f"""
            <div style="margin:0.5rem 0; background:rgba(255,255,255,0.8); padding:0.8rem; border-radius:10px; backdrop-filter:blur(5px);">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span><strong>{status} {category}</strong></span>
                    <span style="font-size:0.85rem; color:#666;">{data['count']}/{data['target']}</span>
                </div>
                <div class="progress-container">
                    <div class="progress-fill" style="width:{progress*100}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        next_ach = None
        for name, data in st.session_state.passport.items():
            if not data['unlocked']:
                next_ach = (name, data)
                break
        if next_ach:
            name, data = next_ach
            progress = int((data['count'] / data['target']) * 100)
            st.markdown(f"""
            <div class="glass-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color:white;">
                <h4 style="color:white;">🎯 Next Achievement</h4>
                <p><strong>{name}</strong></p>
                <p>Progress: {data['count']}/{data['target']}</p>
                <div class="progress-container" style="background:rgba(255,255,255,0.3);">
                    <div class="progress-fill" style="background:white; width:{progress}%;"></div>
                </div>
                <p style="font-size:0.85rem; opacity:0.8; margin-top:0.5rem;">
                    ✨ Unlock exclusive experiences and VIP access
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="glass-card" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color:white;">
                <h4 style="color:white;">🏆 All Achievements Unlocked!</h4>
                <p>You're a BrandDrop Master!</p>
                <p style="font-size:0.85rem; opacity:0.8;">New challenges coming soon</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Notifications Section
    st.markdown("<hr class='divider-glow'>", unsafe_allow_html=True)
    st.markdown("### 🔔 Recent Notifications")
    
    for notif in st.session_state.notifications[:3]:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.7); padding:0.8rem 1.2rem; border-radius:10px; margin:0.3rem 0; border-left:3px solid {'#e74c3c' if not notif['read'] else '#ccc'};">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span>{notif['message']}</span>
                <span style="font-size:0.7rem; color:#999;">{notif['time']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# DISCOVER - WITH FULL DESCRIPTION
# ============================================
elif menu == "Discover":
    st.markdown("""
    <div class="hero-section">
        <h1>📍 Discover Experiences</h1>
        <p class="subtitle">Find brand experiences happening near you</p>
        <p class="tagline">Instead of scrolling through ads, discover experiences</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        category_filter = st.selectbox("Category", ["All", "Beauty", "Fashion", "Food", "Coffee", "Fitness", "Tech", "Luxury", "Gaming"])
    with col2:
        type_filter = st.selectbox("Experience Type", ["All", "Product Sampling", "Product Launch", "Workshop", "Flash Reward", "Mystery Drop", "Treasure Hunt", "Community Challenge"])
    with col3:
        date_filter = st.date_input("Date", datetime.now())
    with col4:
        location_filter = st.text_input("Location", "Dubai")
    
    st.markdown("<hr class='divider-glow'>", unsafe_allow_html=True)
    
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
                st.markdown(f"""
                <div class="experience-card-enhanced" style="border-left-color: {'#2ecc71' if available > 0 else '#e74c3c'};">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:2rem;">{exp.get('image', '🎯')}</span>
                        <span class="badge-type">{exp['type']}</span>
                    </div>
                    <h4 style="margin:0.5rem 0 0 0;">{exp['title']}</h4>
                    <p style="color:#e74c3c; font-weight:500;">{exp['brand']} • {exp['category']}</p>
                    <p style="font-size:0.9rem;">📍 {exp['location']} • 📅 {exp['date']} at {exp['time']}</p>
                    <div class="full-description-text">{exp['description']}</div>
                    <p class="rating">⭐ {exp['rating']} ({exp['reviews']} reviews)</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div style="margin-top:1rem; background:rgba(255,255,255,0.7); padding:1rem; border-radius:10px;">
                    <p><strong>Availability</strong></p>
                    <p class="{'spots' if available > 0 else 'spots-full'}" style="font-size:1.2rem;">{available} spots</p>
                    <div class="progress-container">
                        <div class="progress-fill" style="width:{progress}%;"></div>
                    </div>
                    <p style="font-size:0.8rem; color:#666;">{exp['claimed']}/{exp['spots']} claimed</p>
                    <p style="font-size:0.8rem; color:#666;">🔑 QR: {exp['qr_code']}</p>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                if available > 0:
                    if st.button(f"🔴 Reserve Now", key=f"disc_{exp['id']}"):
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
                    st.markdown("""
                    <div style="background:#e74c3c; color:white; padding:1rem; border-radius:10px; text-align:center; margin-top:2rem;">
                        <span style="font-size:2rem;">🔴</span>
                        <p style="font-weight:700; margin:0;">Fully Booked</p>
                    </div>
                    """, unsafe_allow_html=True)

# ============================================
# PASSPORT
# ============================================
elif menu == "Passport":
    st.markdown("""
    <div class="hero-section">
        <h1>📗 My Experience Passport</h1>
        <p class="subtitle">Collect stamps and unlock achievements</p>
        <p class="tagline">Every experience adds a digital stamp to your passport</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        attended = len(st.session_state.claimed_experiences)
        st.markdown(f"""
        <div class="metric-card-enhanced">
            <div class="icon">📗</div>
            <h2>{attended}</h2>
            <p class="label">Total Experiences</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        unlocked = sum(1 for v in st.session_state.passport.values() if v['unlocked'])
        total = len(st.session_state.passport)
        st.markdown(f"""
        <div class="metric-card-enhanced">
            <div class="icon">🏆</div>
            <h2>{unlocked}/{total}</h2>
            <p class="label">Passport Stamps Unlocked</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        points = st.session_state.user['points']
        st.markdown(f"""
        <div class="metric-card-enhanced">
            <div class="icon">⭐</div>
            <h2>{points}</h2>
            <p class="label">Total Points Earned</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr class='divider-glow'>", unsafe_allow_html=True)
    st.markdown("### ✨ Your Passport Stamps")
    
    col1, col2 = st.columns(2)
    for idx, (category, data) in enumerate(st.session_state.passport.items()):
        with col1 if idx % 2 == 0 else col2:
            progress = min(data['count'] / data['target'], 1)
            status = "✅ Unlocked" if data['unlocked'] else f"🔒 {data['count']}/{data['target']}"
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.8); padding:1rem; border-radius:12px; margin:0.5rem 0; backdrop-filter:blur(5px); border:1px solid rgba(255,255,255,0.3);">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="passport-stamp">{category}</span>
                    <span style="font-size:0.85rem; font-weight:500;">{status}</span>
                </div>
                <div class="progress-container" style="margin-top:0.5rem;">
                    <div class="progress-fill" style="width:{progress*100}%;"></div>
                </div>
                <p style="font-size:0.85rem; color:#666; margin-top:0.3rem;">
                    {data['count']}/{data['target']} completed
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<hr class='divider-glow'>", unsafe_allow_html=True)
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
            st.markdown(f"""
            <div class="achievement-unlocked">
                <div>
                    <h4>✅ {ach['name']}</h4>
                    <p>{ach['desc']}</p>
                </div>
                <span style="font-size:2rem;">🏆</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="achievement-locked">
                <div>
                    <h4>🔒 {ach['name']}</h4>
                    <p>{ach['desc']}</p>
                </div>
                <span style="font-size:1.5rem; opacity:0.5;">🔒</span>
            </div>
            """, unsafe_allow_html=True)

# ============================================
# REWARDS
# ============================================
elif menu == "Rewards":
    st.markdown("""
    <div class="hero-section">
        <h1>🏆 Rewards & Benefits</h1>
        <p class="subtitle">Redeem your points for exclusive experiences</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card-enhanced">
            <div class="icon">💰</div>
            <h1>{st.session_state.user['points']}</h1>
            <p class="label">Available Points</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card-enhanced">
            <div class="icon">⭐</div>
            <h1>Level {st.session_state.user['level']}</h1>
            <p class="label">Member Status</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        next_level = 200 - (st.session_state.user['points'] % 200)
        st.markdown(f"""
        <div class="metric-card-enhanced">
            <div class="icon">📈</div>
            <h1>{next_level}</h1>
            <p class="label">Points to Next Level</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr class='divider-glow'>", unsafe_allow_html=True)
    st.markdown("### 🎁 Reward Catalog")
    
    rewards = [
        {"name": "AED 50 Gift Card", "points": 200, "icon": "🎁", "popular": True},
        {"name": "Movie Tickets (2)", "points": 150, "icon": "🎬", "popular": False},
        {"name": "Exclusive Event Invite", "points": 300, "icon": "🎟️", "popular": True},
        {"name": "Brand Merchandise", "points": 250, "icon": "👕", "popular": False},
        {"name": "Premium Coffee Tasting", "points": 180, "icon": "☕", "popular": True}
    ]
    
    for reward in rewards:
        col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
        with col1:
            st.markdown(f'<span style="font-size:2rem;">{reward["icon"]}</span>', unsafe_allow_html=True)
        with col2:
            st.markdown(f"**{reward['name']}**")
            if reward['popular']:
                st.markdown('<span style="background:#e74c3c; color:white; padding:0.1rem 0.5rem; border-radius:50px; font-size:0.6rem; font-weight:600;">🔥 Popular</span>', unsafe_allow_html=True)
        with col3:
            st.markdown(f"**{reward['points']} points**")
        with col4:
            if st.button(f"Redeem", key=f"rew_{reward['name']}"):
                if st.session_state.user['points'] >= reward['points']:
                    st.success(f"✅ Redeemed: {reward['name']}")
                    st.session_state.user['points'] -= reward['points']
                else:
                    st.error("❌ Insufficient points")

# ============================================
# CLUBS
# ============================================
elif menu == "Clubs":
    st.markdown("""
    <div class="hero-section">
        <h1>👥 Consumer Clubs</h1>
        <p class="subtitle">Join niche communities and connect with like-minded enthusiasts</p>
        <p class="tagline">Brands engage niche communities instead of targeting everyone</p>
    </div>
    """, unsafe_allow_html=True)
    
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
            color = "#2ecc71" if club['joined'] else "#e74c3c"
            st.markdown(f"""
            <div class="club-card">
                <span style="font-size:2.5rem;">{club['name'].split()[0]}</span>
                <h3>{club['name']}</h3>
                <p class="member-count">👥 {club['members']:,} members</p>
                <p class="event-count">🎯 {club['events']} upcoming events</p>
                <p style="margin-top:0.5rem; font-weight:700; color:{color};">{status}</p>
            </div>
            """, unsafe_allow_html=True)
            if not club['joined']:
                if st.button(f"Join", key=f"join_{club['name']}"):
                    club_name = club['name'].replace("☕ ", "").replace("💄 ", "").replace("👟 ", "").replace("🐾 ", "").replace("👨‍👩‍👧‍👦 ", "").replace("🍽️ ", "").replace("🎮 ", "").replace("💪 ", "")
                    st.session_state.clubs[club_name]['joined'] = True
                    st.success(f"✅ Joined {club['name']}!")
                    st.rerun()

# ============================================
# FOR BRANDS
# ============================================
elif menu == "For Brands":
    st.markdown("""
    <div class="hero-section">
        <h1>🏢 For Brands</h1>
        <p class="subtitle">Launch campaigns and measure real engagement</p>
        <p class="tagline">Clear ROI instead of vague advertising metrics</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-card-enhanced">
            <div class="icon">👥</div>
            <h3>1,247</h3>
            <p class="label">Total Attendees</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card-enhanced">
            <div class="icon">🚀</div>
            <h3>12</h3>
            <p class="label">Active Campaigns</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card-enhanced">
            <div class="icon">📊</div>
            <h3>87%</h3>
            <p class="label">Avg. Redemption Rate</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-card-enhanced">
            <div class="icon">⭐</div>
            <h3>4.7</h3>
            <p class="label">Avg. Rating</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr class='divider-glow'>", unsafe_allow_html=True)
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
        
        target_audience = st.multiselect(
            "Target Audience",
            ["Beauty Club", "Coffee Club", "Sneaker Club", "Pet Club", "Parents Club", "Foodies Club", "Gamers Club", "Fitness Club"]
        )
        
        submitted = st.form_submit_button("🚀 Launch Campaign", type="primary")
        if submitted:
            st.success("✅ Campaign created successfully! Your experience is now live.")
            st.balloons()
    
    st.markdown("<hr class='divider-glow'>", unsafe_allow_html=True)
    st.markdown("### 📊 Campaign Performance")
    
    data = pd.DataFrame({
        'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        'Reservations': [45, 67, 89, 102],
        'Attendees': [38, 55, 72, 85],
        'Redemptions': [30, 48, 61, 72]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Week'], y=data['Reservations'], name='Reservations', mode='lines+markers', line=dict(color='#e74c3c', width=3), marker=dict(size=10)))
    fig.add_trace(go.Scatter(x=data['Week'], y=data['Attendees'], name='Attendees', mode='lines+markers', line=dict(color='#3498db', width=3), marker=dict(size=10)))
    fig.add_trace(go.Scatter(x=data['Week'], y=data['Redemptions'], name='Redemptions', mode='lines+markers', line=dict(color='#2ecc71', width=3), marker=dict(size=10)))
    fig.update_layout(
        title='Campaign Performance Trends',
        xaxis_title='Time Period',
        yaxis_title='Number of Users',
        height=400,
        template='plotly_white',
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# TESTIMONIALS
# ============================================
elif menu == "Testimonials":
    st.markdown("""
    <div class="hero-section">
        <h1>💬 What Our Community Says</h1>
        <p class="subtitle">Real stories from real BrandDrop users</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-card-enhanced">
            <div class="icon">⭐</div>
            <h2>4.7</h2>
            <p class="label">Average Rating</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card-enhanced">
            <div class="icon">📝</div>
            <h2>1,247</h2>
            <p class="label">Reviews</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card-enhanced">
            <div class="icon">👥</div>
            <h2>5K+</h2>
            <p class="label">Happy Users</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-card-enhanced">
            <div class="icon">🏆</div>
            <h2>98%</h2>
            <p class="label">Would Recommend</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr class='divider-glow'>", unsafe_allow_html=True)
    st.markdown("### 💬 User Testimonials")
    
    cols = st.columns(2)
    for idx, testimonial in enumerate(st.session_state.testimonials):
        with cols[idx % 2]:
            stars = "⭐" * testimonial['stars']
            st.markdown(f"""
            <div class="testimonial-card">
                <div class="avatar">{testimonial['avatar']}</div>
                <div class="stars">{stars}</div>
                <p class="quote">"{testimonial['quote']}"</p>
                <p class="author">{testimonial['name']}</p>
                <p class="role-text">{testimonial['role']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<hr class='divider-glow'>", unsafe_allow_html=True)
    st.markdown("### ✍️ Share Your Experience")
    
    with st.form("testimonial_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Name", placeholder="Enter your name")
            role = st.text_input("Your Role", placeholder="e.g., Coffee Lover, Fashion Enthusiast")
        with col2:
            rating = st.select_slider("Rating", options=[1, 2, 3, 4, 5], value=5)
            testimonial_text = st.text_area("Your Testimonial", placeholder="Share your BrandDrop experience...")
        
        submitted = st.form_submit_button("Submit Testimonial", type="primary")
        if submitted and name and testimonial_text:
            st.session_state.testimonials.append({
                'name': name,
                'role': role or "BrandDrop User",
                'quote': testimonial_text,
                'stars': rating,
                'avatar': random.choice(["😊", "🌟", "✨", "💫", "👏"])
            })
            st.success("✅ Thank you! Your testimonial has been added.")
            st.balloons()
            st.rerun()

# ============================================
# ABOUT - FIXED VERSION
# ============================================
elif menu == "About":
    st.markdown("""
    <div class="hero-section">
        <h1>ℹ️ About BrandDrop</h1>
        <p class="subtitle">UAE's First Consumer Experience Marketplace</p>
        <p class="tagline">Where brands compete for attention through experiences, not advertisements</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3>🎯 Our Mission</h3>
            <p>BrandDrop is revolutionizing how brands connect with consumers in the UAE. We're replacing traditional advertising with real-world experiences that create meaningful connections and measurable engagement.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### ❌ The Problem We Solve")
        st.markdown("""
        - Consumers skip ads and ignore influencer promotions
        - Brands waste budget on activations without measuring ROI
        - Exciting brand experiences are scattered across multiple platforms
        - No single platform exists for discovering brand experiences
        """)
        
        st.markdown("### ✅ Our Solution")
        st.markdown("""
        - Single platform for discovering, booking, and engaging with brand experiences
        - Measurable engagement instead of just impressions
        - Experience Passport with achievements and rewards
        - Real-time analytics for brands to track campaign performance
        """)
        
        st.markdown("### 🇦🇪 Why UAE?")
        st.markdown("""
        - Retail- and mall-driven culture
        - Frequent product launches and brand activations
        - Large tourism volumes
        - Digitally connected population
        - Strong government support for innovation
        """)
    
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3>📊 Quick Stats</h3>
            <div style="margin:1rem 0;">
                <div style="display:flex; justify-content:space-between; padding:0.5rem 0; border-bottom:1px solid #eee;">
                    <span>👥 Users</span>
                    <span style="font-weight:700;">5,000+</span>
                </div>
                <div style="display:flex; justify-content:space-between; padding:0.5rem 0; border-bottom:1px solid #eee;">
                    <span>🏢 Brands</span>
                    <span style="font-weight:700;">200+</span>
                </div>
                <div style="display:flex; justify-content:space-between; padding:0.5rem 0; border-bottom:1px solid #eee;">
                    <span>🎯 Experiences</span>
                    <span style="font-weight:700;">500+</span>
                </div>
                <div style="display:flex; justify-content:space-between; padding:0.5rem 0;">
                    <span>⭐ Avg. Rating</span>
                    <span style="font-weight:700;">4.7</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="developer-box">
            <h3>👨‍💻 Development Team</h3>
            <div class="team-member"><span><strong>Ronit</strong></span></div>
            <div class="team-member"><span><strong>Syed</strong></span></div>
            <div class="team-member"><span><strong>Shania</strong></span></div>
            <div class="team-member"><span><strong>Krishna</strong></span></div>
            <div class="team-member"><span><strong>Khushil</strong></span></div>
            <div class="team-member"><span><strong>Vyomika</strong></span></div>
            <p style="margin-top:1rem; color:#666; font-size:0.9rem;">Built with ❤️ in Dubai, UAE<br>© 2026 BrandDrop</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div class="footer-enhanced">
    <div class="brand">Brand<span>Drop</span></div>
    <p class="tagline">Discover. Experience. Earn. — Where brands come to life.</p>
    <p style="font-size:0.8rem; color:#999; margin-top:0.5rem;">© 2026 BrandDrop. All rights reserved. UAE's First Consumer Experience Marketplace.</p>
</div>
""", unsafe_allow_html=True)
