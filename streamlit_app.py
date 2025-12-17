import streamlit as st
import requests
from streamlit_lottie import st_lottie
import json

# Config
st.set_page_config(
    page_title="SHL Assessment Recommender Pro",
    layout="wide",
    page_icon="🎯",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    /* Assessment card with modern design */
    .assessment-card {
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
        background: linear-gradient(145deg, #2d3a3a, #1a2525);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        border-left: 5px solid #4CAF50;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .assessment-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(76, 175, 80, 0.3);
    }
    
    /* Relevance badge with gradient */
    .relevance-badge {
        background: linear-gradient(135deg, #1e3a1e, #2d5a2d);
        color: #8bc34a;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.9rem;
        box-shadow: 0 4px 12px rgba(139, 195, 74, 0.3);
    }
    
    /* AI insights with modern styling */
    .ai-insights {
        background: linear-gradient(135deg, #2a3535, #1f2828);
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 1.5rem;
        border-left: 4px solid #607d8b;
        box-shadow: inset 0 2px 8px rgba(0,0,0,0.2);
    }
    
    /* Detail rows with better spacing */
    .detail-container {
        display: flex;
        margin: 0.75rem 0;
        padding: 0.5rem;
        border-radius: 6px;
        background: rgba(255,255,255,0.02);
    }
    
    .detail-label {
        font-weight: 700;
        color: #a8c7cb;
        min-width: 140px;
        text-transform: uppercase;
        font-size: 0.85rem;
        letter-spacing: 0.5px;
    }
    
    .detail-value {
        color: #ffffff;
        font-size: 0.95rem;
    }
    
    /* Progress indicator */
    .progress-step {
        display: inline-block;
        padding: 0.5rem 1rem;
        margin: 0.5rem;
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        border-radius: 25px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
    }
    
    .progress-step.completed {
        background: linear-gradient(135deg, #2196F3, #1976D2);
    }
    
    /* Instruction cards */
    .instruction-card {
        background: linear-gradient(145deg, #1e2a2a, #2d3a3a);
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
        border-left: 5px solid #2196F3;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }
    
    /* Example and tip boxes */
    .example-box, .tip-box {
        background: linear-gradient(145deg, #252f2f, #1a2424);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.75rem 0;
        font-family: 'Courier New', monospace;
        border-left: 4px solid #4CAF50;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .tip-box {
        border-left: 4px solid #FF9800;
    }
    
    /* Success checkmark */
    .checkmark {
        color: #4CAF50;
        font-size: 1.2rem;
        margin-right: 0.5rem;
    }
    
    /* Header styling */
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("SHL Assessment Recommender")
st.caption("Intelligent matching for talent acquisition professionals")

# Add Instructions Section at the top
with st.expander("How to Use This Application", expanded=False):
    st.markdown("""
    <div class="instruction-card">
        <h3>Getting Started</h3>
        <p>This AI-powered tool helps you find the most relevant SHL assessments for your hiring needs. Simply describe the role or paste a job description URL, and get instant recommendations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Input Methods")
        st.markdown("""
        <div class="tip-box">
            <strong>Method 1: Text Description</strong><br>
            Describe the role in your own words with key details like:
            <ul>
                <li>Job title and level (entry, mid, senior)</li>
                <li>Key skills required</li>
                <li>Industry or domain</li>
                <li>Specific competencies needed</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="tip-box">
            <strong>Method 2: Job Description URL</strong><br>
            Paste a direct link to any job posting, and the system will automatically extract and analyze the requirements.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Example Prompts")
        
        st.markdown("""
        <div class="example-box">
            <strong>Example 1:</strong><br>
            "Senior Java developer with strong team collaboration and stakeholder management skills"
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="example-box">
            <strong>Example 2:</strong><br>
            "Mid-level data analyst proficient in Python, SQL, and data visualization tools"
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="example-box">
            <strong>Example 3:</strong><br>
            "Entry-level customer service representative with excellent communication and problem-solving abilities"
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="example-box">
            <strong>Example 4:</strong><br>
            "Project manager with 5+ years experience in agile methodologies and cross-functional team leadership"
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="example-box">
            <strong>Example 5:</strong><br>
            "Financial analyst requiring strong analytical thinking, Excel proficiency, and attention to detail"
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### Best Practices for Optimal Results")
    
    tips_col1, tips_col2, tips_col3 = st.columns(3)
    
    with tips_col1:
        st.markdown("""
        **Be Specific**
        - Include job level (junior/mid/senior)
        - Mention key skills or competencies
        - Add industry context if relevant
        """)
    
    with tips_col2:
        st.markdown("""
        **Keep It Clear**
        - Use natural language
        - Focus on core requirements
        - Avoid overly complex jargon
        """)
    
    with tips_col3:
        st.markdown("""
        **Enable AI Insights**
        - Toggle AI insights for detailed analysis
        - Get personalized recommendations
        - Understand assessment fit better
        """)
    
    st.markdown("---")
    
    st.markdown("### Understanding Results")
    st.markdown("""
    - **Relevance Score**: Ranges from 0.0 (perfect match) to 1.0 (less relevant). Lower scores indicate better matches.
    - **AI Insights**: When enabled, provides expert analysis on key skills measured, ideal candidate level, and best use cases.
    - **Assessment Details**: Includes duration, language support, job level suitability, and testing format options.
    """)

# Sidebar
with st.sidebar:
    st.header("Configuration")
    use_ai = st.toggle("Enable AI Insights", value=True)
    
    with st.expander("Advanced Settings"):
        api_url = st.text_input(
            "API Endpoint",
            value="http://127.0.0.1:8000/recommend",
        )
    
    st.markdown("---")
    st.markdown("""
    **Interpretation Guide**
    - **Relevance Score**: Lower is better (0.0 = perfect match)
    - **Support Icons**: 
      - [YES] = Supported 
      - [NO] = Not Supported 
      - [N/A] = Unknown
    """)

# Main Content
st.markdown("### Search for Assessments")

# Example selector
example_queries = [
    "-- Select an example or type your own --",
    "Senior Java developer with strong team collaboration and stakeholder management skills",
    "Mid-level data analyst proficient in Python, SQL, and data visualization tools",
    "Entry-level customer service representative with excellent communication and problem-solving abilities",
    "Project manager with 5+ years experience in agile methodologies and cross-functional team leadership",
    "Financial analyst requiring strong analytical thinking, Excel proficiency, and attention to detail",
    "Software architect with expertise in microservices and cloud-native applications",
    "Marketing manager with digital marketing and campaign management experience",
    "HR specialist with talent acquisition and employee relations skills"
]

col1, col2 = st.columns([3, 1])
with col1:
    selected_example = st.selectbox(
        "Quick Examples:",
        example_queries,
        index=0,
        help="Select an example query or type your own below"
    )

with col2:
    if st.button("Use Example", type="secondary", disabled=(selected_example == example_queries[0])):
        st.session_state.query = selected_example

# Initialize session state for query
if 'query' not in st.session_state:
    st.session_state.query = ""

# Text input for custom query
query = st.text_area(
    "Or describe the role:",
    value=st.session_state.query if selected_example == example_queries[0] else selected_example,
    placeholder="e.g., 'Senior software engineer with expertise in cloud architecture and team leadership'",
    height=100,
    help="Describe the job role, required skills, and experience level"
)

if st.button("Find Assessments", type="primary") and query:
    # Progress indicator
    progress_container = st.container()
    with progress_container:
        st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <span class='progress-step completed'>✓ Query Received</span>
            <span class='progress-step'>→ Analyzing...</span>
        </div>
        """, unsafe_allow_html=True)
    
    with st.spinner("Finding optimal assessments..."):
        try:
            response = requests.post(
                api_url,
                json={"text": query, "use_ai": use_ai},
                timeout=120
            ).json()

            # Update progress
            progress_container.empty()
            with progress_container:
                st.markdown("""
                <div style='text-align: center; padding: 1rem;'>
                    <span class='progress-step completed'>✓ Query Received</span>
                    <span class='progress-step completed'>✓ Analysis Complete</span>
                    <span class='progress-step completed'>✓ Results Ready</span>
                </div>
                """, unsafe_allow_html=True)

            if not response:
                st.warning("No assessments found. Try different keywords.")
            else:
                st.success(f"Found {len(response)} matching assessments")
                
                # Results summary
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #1e3a1e, #2d5a2d); 
                            padding: 1rem; border-radius: 10px; margin: 1rem 0;
                            box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);'>
                    <h3 style='color: #8bc34a; margin: 0;'>
                        <span class='checkmark'>✓</span>
                        {len(response)} Relevant Assessments Found
                    </h3>
                    <p style='color: #a8c7cb; margin: 0.5rem 0 0 0;'>
                        Sorted by relevance score (lower is better)
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                for idx, item in enumerate(sorted(response, key=lambda x: x['score']), 1):
                    # Safely handle all fields with defaults
                    name = item.get('name', 'Unknown Assessment')
                    url = item.get('url', '#')
                    score = item.get('score', 1.0)
                    duration = item.get('duration', 'Not specified')
                    languages = ''.join(item.get('languages', [])) or 'Not specified'
                    job_level = item.get('job_level', 'Not specified')
                    remote_testing = item.get('remote_testing', '❓')
                    adaptive_support = item.get('adaptive_support', item.get('adaptive/irt_support', '❓'))
                    test_type = item.get('test_type', 'Not specified')
                    description = item.get('description', 'No description available')
                    ai_insights = item.get('ai_insights', '') if use_ai else ''
                    
                    # Rank badge color based on position
                    rank_color = '#4CAF50' if idx <= 3 else '#2196F3' if idx <= 6 else '#607d8b'
                    
                    # Create assessment card using Streamlit components
                    with st.container():
                        st.markdown('<div class="assessment-card">', unsafe_allow_html=True)
                        
                        # Header row with rank badge
                        col1, col2, col3 = st.columns([1, 6, 2])
                        with col1:
                            st.markdown(f"""
                            <div style='background: {rank_color}; color: white; 
                                        padding: 0.5rem; border-radius: 50%; 
                                        width: 50px; height: 50px; 
                                        display: flex; align-items: center; 
                                        justify-content: center; font-weight: bold;
                                        font-size: 1.2rem; box-shadow: 0 4px 12px rgba(0,0,0,0.3);'>
                                #{idx}
                            </div>
                            """, unsafe_allow_html=True)
                        with col2:
                            st.subheader(name)
                        with col3:
                            st.markdown(f'<span class="relevance-badge">Score: {score:.3f}</span>', 
                                      unsafe_allow_html=True)
                        
                        # Details using columns for layout
                        def detail_row(label, value):
                            cols = st.columns([1, 3])
                            with cols[0]:
                                st.markdown(f'<div class="detail-label">{label}</div>', unsafe_allow_html=True)
                            with cols[1]:
                                st.markdown(f'<div class="detail-value">{value}</div>', unsafe_allow_html=True)
                        
                        detail_row("URL:", f'<a href="{url}" target="_blank">View Assessment</a>')
                        detail_row("Duration:", duration)
                        detail_row("Languages:", languages)
                        detail_row("Job Level:", job_level)
                        detail_row("Remote Testing:", f'<span class="support-icon">{remote_testing}</span>')
                        detail_row("Adaptive/IRT:", f'<span class="support-icon">{adaptive_support}</span>')
                        detail_row("Test Type:", test_type)
                        
                        # Description
                        st.markdown("---")
                        st.markdown("**Description:**")
                        st.markdown(description)
                        
                        # AI Insights
                        if ai_insights:
                            st.markdown('<div class="ai-insights">', unsafe_allow_html=True)
                            st.markdown("**AI Analysis:**")
                            for line in ai_insights.split('\n'):
                                if line.strip():
                                    st.markdown(f"• {line.strip()}")
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Please ensure the API is running at the specified endpoint")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #888;'>
        <p>SHL Assessment Recommender | Professional Edition</p>
        <p>Created by <strong>Abhay Gupta</strong> | 
        <a href='https://www.abhaygupta6187.me/' target='_blank' style='color: #4CAF50;'>Website</a> | 
        <a href='https://www.linkedin.com/in/abhay-gupta-197b17264/' target='_blank' style='color: #0077B5;'>LinkedIn</a>
        </p>
    </div>
""", unsafe_allow_html=True)