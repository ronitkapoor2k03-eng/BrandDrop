import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page config
st.set_page_config(
    page_title="BrandDrop - Experience Marketplace",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .brand-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .experience-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #e74c3c;
    }
    .metric-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #e9ecef;
    }
    .passport-stamp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.2rem;
        font-size: 0.9rem;
    }
    .developer-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 1rem;
        border-left: 4px solid #e74c3c;
    }
    .stButton > button {
        background-color: #e74c3c;
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #c0392b;
        color: white;
    }
    .sidebar-nav {
        padding: 0.5rem 0;
    }
    .sidebar-nav .stRadio > div {
        gap: 0.3rem;
    }
    .sidebar-nav label {
        padding: 0.5rem 1rem;
        border-radius: 8px;
        transition: background 0.2s;
    }
    .sidebar-nav label:hover {
        background: #f0f0f0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'user' not in st.session_state:
    st.session_state.user = {
        'name': 'Ahmed Al Maktoum',
        'points': 450,
        'level': 3
    }

if 'passport' not in st.session_state:
    st.session_state.passport = {
        'Coffee Explorer': 7,
        'Beauty Insider': 4,
        'Food Adventurer': 3,
        'Fitness Fanatic': 1,
        'Sneaker Hunter': 5,
        'Tech Enthusiast': 2
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
            'description': 'Sample premium Japanese matcha and learn traditional tea preparation.',
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
            'description': 'Learn skincare routines and receive personalized product recommendations.',
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
            'description': 'Master pour-over, espresso, and cold brew techniques.',
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
            'rating': 4.5,
            'reviews': 15
        },
        {
            'id': 6,
            'title': 'Tech Innovation Showcase',
            'brand': 'Dubai Tech Hub',
            'category': 'Tech',
            'location': 'Dubai Internet City',
            'date': '2026-07-11',
            'time': '3:00 PM',
            'spots': 40,
            'claimed': 28,
            'description': 'Experience the latest in AI, VR, and emerging technologies.',
            'rating': 4.7,
            'reviews': 33
        }
    ]

if 'claimed' not in st.session_state:
    st.session_state.claimed = []

# Sidebar Navigation
with st.sidebar:
    st.markdown("## 🎯 BrandDrop")
    st.markdown("### UAE's Experience Marketplace")
    st.markdown("---")
    
    menu = st.radio(
        "Navigate",
        ["Dashboard", "Discover", "My Passport", "Rewards", "For Brands", "About"],
        key="menu_nav",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown(f"""
    <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px;">
        <p><strong>👤 {st.session_state.user['name']}</strong></p>
        <p>⭐ Level {st.session_state.user['level']}</p>
        <p>🏆 {st.session_state.user['points']} points</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# DASHBOARD
# ============================================
if menu == "Dashboard":
    st.markdown("""
    <div class="brand-header">
        <h1>Welcome to BrandDrop</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">UAE's First Consumer Experience Marketplace</p>
        <p style="font-size: 1rem; opacity: 0.7;">Discover. Experience. Earn.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-box"><h3 style="color:#e74c3c;">12</h3><p>Experiences Attended</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-box"><h3 style="color:#e74c3c;">{st.session_state.user["points"]}</h3><p>Total Points</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-box"><h3 style="color:#e74c3c;">6</h3><p>Passport Stamps</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-box"><h3 style="color:#e74c3c;">24</h3><p>Available Experiences</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Featured Experiences
    st.markdown("### 🔥 Featured Experiences")
    
    featured = st.session_state.experiences[:3]
    cols = st.columns(3)
    for idx, exp in enumerate(featured):
        with cols[idx]:
            available = exp['spots'] - exp['claimed']
            progress = (exp['claimed'] / exp['spots']) * 100
            st.markdown(f"""
            <div class="experience-card">
                <h4>{exp['title']}</h4>
                <p style="color:#e74c3c; font-weight:600;">{exp['brand']}</p>
                <p>📍 {exp['location']}</p>
                <p>📅 {exp['date']} at {exp['time']}</p>
                <div style="background:#e9ecef; height:6px; border-radius:3px; margin:0.5rem 0;">
                    <div style="background:#e74c3c; width:{progress}%; height:6px; border-radius:3px;"></div>
                </div>
                <p>🎯 {available} spots remaining</p>
                <p>⭐ {exp['rating']} ({exp['reviews']} reviews)</p>
            </div>
            """, unsafe_allow_html=True)
            if available > 0:
                if st.button(f"Reserve Now", key=f"dash_{exp['id']}"):
                    st.success(f"✅ Reserved! QR Code: BD-{exp['id']}-2026")
                    st.balloons()
                    if exp['id'] not in st.session_state.claimed:
                        st.session_state.claimed.append(exp['id'])
    
    st.markdown("---")
    
    # Passport Progress
    st.markdown("### 📗 Passport Progress")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        for category, count in st.session_state.passport.items():
            progress = min(count / 10, 1)
            st.markdown(f"**{category}**")
            st.progress(progress)
            st.markdown(f"*{count}/10 completed*")
            st.markdown("")
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 10px; color: white;">
            <h4>🏆 Next Achievement</h4>
            <p><strong>Food Adventurer:</strong> Visit 10 restaurants</p>
            <p>Progress: 3/10</p>
            <p style="font-size:0.9rem;">Unlock exclusive dining experiences</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# DISCOVER
# ============================================
elif menu == "Discover":
    st.markdown("""
    <div class="brand-header">
        <h1>Discover Experiences</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">Find brand experiences happening near you</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        category_filter = st.selectbox(
            "Category",
            ["All", "Beauty", "Fashion", "Food", "Coffee", "Fitness", "Tech"]
        )
    with col2:
        date_filter = st.date_input("Date", datetime.now())
    with col3:
        location_filter = st.text_input("Location", "Dubai")
    
    st.markdown("---")
    
    filtered = st.session_state.experiences
    if category_filter != "All":
        filtered = [e for e in filtered if e['category'] == category_filter]
    
    st.markdown(f"### 📋 {len(filtered)} Experiences Available")
    
    for exp in filtered:
        available = exp['spots'] - exp['claimed']
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.markdown(f"""
                <div style="border-left: 4px solid #e74c3c; padding-left: 1rem; margin: 0.5rem 0;">
                    <h4>{exp['title']}</h4>
                    <p style="color:#e74c3c; font-weight:500;">{exp['brand']} • {exp['category']}</p>
                    <p>📍 {exp['location']} • 📅 {exp['date']} at {exp['time']}</p>
                    <p style="font-size:0.9rem;">{exp['description']}</p>
                    <p>⭐ {exp['rating']} ({exp['reviews']} reviews)</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div style="margin-top:1rem;">
                    <p>Available: <strong>{available}</strong> spots</p>
                    <div style="background:#e9ecef; height:6px; border-radius:3px;">
                        <div style="background:#e74c3c; width:{(exp['claimed']/exp['spots']*100)}%; height:6px; border-radius:3px;"></div>
                    </div>
                    <p style="font-size:0.8rem; color:#666;">{exp['claimed']}/{exp['spots']} claimed</p>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                if available > 0:
                    if st.button(f"🔴 Reserve", key=f"disc_{exp['id']}"):
                        st.success(f"✅ Reserved! Check your Passport.")
                        st.balloons()
                        if exp['id'] not in st.session_state.claimed:
                            st.session_state.claimed.append(exp['id'])
                else:
                    st.markdown("🔴 **Fully Booked**")

# ============================================
# MY PASSPORT
# ============================================
elif menu == "My Passport":
    st.markdown("""
    <div class="brand-header">
        <h1>My Experience Passport</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">Collect stamps and unlock achievements</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-box"><h2 style="color:#e74c3c;">12</h2><p>Total Experiences</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-box"><h2 style="color:#e74c3c;">6</h2><p>Passport Categories</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-box"><h2 style="color:#e74c3c;">3</h2><p>Achievements Unlocked</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ✨ Your Passport Stamps")
    
    col1, col2 = st.columns(2)
    for idx, (category, count) in enumerate(st.session_state.passport.items()):
        with col1 if idx % 2 == 0 else col2:
            progress = min(count / 10, 1)
            st.markdown(f"""
            <div style="background:#f8f9fa; padding:1rem; border-radius:8px; margin:0.5rem 0;">
                <span class="passport-stamp">{category}</span>
                <p style="margin-top:0.5rem;">Progress: {count}/10</p>
                <div style="background:#e9ecef; height:8px; border-radius:4px;">
                    <div style="background:linear-gradient(90deg,#667eea,#764ba2); 
                                width:{progress*100}%; height:8px; border-radius:4px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🏆 Unlocked Achievements")
    
    achievements = [
        {"name": "Coffee Explorer", "desc": "Visit 10 independent cafés", "unlocked": st.session_state.passport.get('Coffee Explorer', 0) >= 10},
        {"name": "Beauty Insider", "desc": "Attend 5 beauty launches", "unlocked": st.session_state.passport.get('Beauty Insider', 0) >= 5},
        {"name": "Dubai Explorer", "desc": "Complete experiences across 5 malls", "unlocked": True},
        {"name": "Sneaker Hunter", "desc": "Attend 3 sneaker launches", "unlocked": st.session_state.passport.get('Sneaker Hunter', 0) >= 3},
        {"name": "Tech Enthusiast", "desc": "Attend 5 tech events", "unlocked": st.session_state.passport.get('Tech Enthusiast', 0) >= 5}
    ]
    
    for ach in achievements:
        if ach['unlocked']:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#f093fb 0%,#f5576c 100%); 
                        padding:1rem; border-radius:10px; margin:0.5rem 0; color:white;">
                <h4>✅ {ach['name']}</h4>
                <p>{ach['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:#f1f3f5; padding:1rem; border-radius:10px; margin:0.5rem 0; opacity:0.6;">
                <h4>🔒 {ach['name']}</h4>
                <p>{ach['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

# ============================================
# REWARDS
# ============================================
elif menu == "Rewards":
    st.markdown("""
    <div class="brand-header">
        <h1>Rewards & Benefits</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">Redeem your points for exclusive experiences</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-box"><h1 style="color:#e74c3c;">{st.session_state.user["points"]}</h1><p>Available Points</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-box"><h1 style="color:#e74c3c;">Level {st.session_state.user["level"]}</h1><p>Member Status</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-box"><h1 style="color:#e74c3c;">200</h1><p>Points to Next Level</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
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

# ============================================
# FOR BRANDS
# ============================================
elif menu == "For Brands":
    st.markdown("""
    <div class="brand-header">
        <h1>For Brands</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">Launch campaigns and measure real engagement</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-box"><h3 style="color:#e74c3c;">1,247</h3><p>Total Attendees</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-box"><h3 style="color:#e74c3c;">12</h3><p>Active Campaigns</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-box"><h3 style="color:#e74c3c;">87%</h3><p>Avg. Redemption Rate</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-box"><h3 style="color:#e74c3c;">4.7</h3><p>Avg. Rating</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
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
            end_date = st.date_input("End Date", datetime.now())
            capacity = st.number_input("Capacity", min_value=10, max_value=500, value=50)
            budget = st.number_input("Budget (AED)", min_value=1000, value=5000)
        
        submitted = st.form_submit_button("Launch Campaign", type="primary")
        if submitted:
            st.success("✅ Campaign created successfully! Your experience is now live.")
            st.balloons()
    
    st.markdown("---")
    st.markdown("### 📊 Campaign Performance")
    
    # Simple chart
    data = pd.DataFrame({
        'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        'Attendees': [38, 55, 72, 85],
        'Redemptions': [30, 48, 61, 72]
    })
    
    fig = px.line(data, x='Week', y=['Attendees', 'Redemptions'], 
                  title='Campaign Performance Trends',
                  labels={'value': 'Users', 'variable': 'Metric'})
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# ABOUT
# ============================================
elif menu == "About":
    st.markdown("""
    <div class="brand-header">
        <h1>About BrandDrop</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">UAE's First Consumer Experience Marketplace</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### Our Mission
        BrandDrop is revolutionizing how brands connect with consumers in the UAE. 
        We're replacing traditional advertising with real-world experiences.
        
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
            <p><strong>Ronit Kapoor</strong> - Lead Developer</p>
            <p><strong>Syed Ali</strong> - Backend Engineer</p>
            <p><strong>Shania Ahmed</strong> - UI/UX Designer</p>
            <p><strong>Krishna Patel</strong> - Frontend Developer</p>
            <p><strong>Khushil Sharma</strong> - Data Analyst</p>
            <p><strong>Vyomika Reddy</strong> - QA Engineer</p>
            <p style="margin-top:1rem; color:#666; font-size:0.9rem;">
                Built with ❤️ in Dubai, UAE<br>
                © 2026 BrandDrop
            </p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem 0;">
    <p><strong>BrandDrop</strong> - Discover. Experience. Earn.</p>
    <p style="font-size:0.8rem;">© 2026 BrandDrop. UAE's First Consumer Experience Marketplace.</p>
</div>
""", unsafe_allow_html=True)
