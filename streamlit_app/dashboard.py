"""Streamlit dashboard for Reddit Trend Research."""
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# Page config
st.set_page_config(
    page_title="Reddit Trend Research Dashboard",
    page_icon="📊",
    layout="wide"
)

# API base URL
API_BASE_URL = "http://localhost:8000"


@st.cache_data(ttl=60)
def fetch_data(endpoint: str):
    """Fetch data from API with caching."""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return None


def main():
    """Main dashboard function."""
    st.title("📊 Reddit Trend Research Dashboard")
    st.markdown("Analyze trending discussions in AI/ML and fitness communities")
    
    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        page = st.radio(
            "Select Page",
            ["Overview", "Data Collection", "Analysis Results", "Trending Topics", "Common Questions"]
        )
        
        st.header("API Status")
        health = fetch_data("/health")
        if health:
            st.success("✅ API Connected")
            st.info(f"Rate Limit Remaining: {health.get('rate_limit_remaining', 'N/A')}")
        else:
            st.error("❌ API Not Connected")
            st.info("Make sure the FastAPI server is running on port 8000")
    
    # Route to appropriate page
    if page == "Overview":
        show_overview()
    elif page == "Data Collection":
        show_data_collection()
    elif page == "Analysis Results":
        show_analysis_results()
    elif page == "Trending Topics":
        show_trending_topics()
    elif page == "Common Questions":
        show_common_questions()


def show_overview():
    """Show overview page."""
    st.header("Overview")
    
    # Get subreddits
    subreddits_data = fetch_data("/subreddits")
    if subreddits_data:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("AI/ML Subreddits", len(subreddits_data.get("ai_ml", [])))
        with col2:
            st.metric("Running Subreddits", len(subreddits_data.get("running", [])))
        with col3:
            st.metric("Nutrition Subreddits", len(subreddits_data.get("nutrition", [])))
        with col4:
            st.metric("Strength Training", len(subreddits_data.get("strength_training", [])))
        
        st.subheader("Target Subreddits")
        st.json(subreddits_data)
    
    # List data files
    files_data = fetch_data("/data/files")
    if files_data:
        st.subheader("Available Data")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Collected Data Files:**")
            st.write(files_data.get("data_files", []))
        
        with col2:
            st.write("**Analysis Files:**")
            st.write(files_data.get("analysis_files", []))


def show_data_collection():
    """Show data collection page."""
    st.header("Data Collection")
    
    st.info("Use this page to collect data from Reddit subreddits")
    
    with st.form("collection_form"):
        st.subheader("Collection Settings")
        
        subreddits_input = st.text_area(
            "Subreddits (comma-separated, leave empty for all)",
            help="Enter subreddit names separated by commas, or leave empty to use all target subreddits"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            posts_per_subreddit = st.number_input("Posts per Subreddit", min_value=10, max_value=500, value=100)
            time_period_days = st.number_input("Time Period (days)", min_value=1, max_value=30, value=7)
        
        with col2:
            include_comments = st.checkbox("Include Comments", value=True)
            top_comments_limit = st.number_input("Top Comments Limit", min_value=1, max_value=50, value=10)
        
        submitted = st.form_submit_button("Start Collection", type="primary")
        
        if submitted:
            with st.spinner("Collecting data from Reddit..."):
                subreddits = [s.strip() for s in subreddits_input.split(",")] if subreddits_input else None
                
                payload = {
                    "subreddits": subreddits,
                    "posts_per_subreddit": posts_per_subreddit,
                    "time_period_days": time_period_days,
                    "include_comments": include_comments,
                    "top_comments_limit": top_comments_limit
                }
                
                try:
                    response = requests.post(f"{API_BASE_URL}/collect", json=payload, timeout=300)
                    response.raise_for_status()
                    result = response.json()
                    
                    st.success(f"✅ {result['message']}")
                    st.json(result)
                except requests.exceptions.RequestException as e:
                    st.error(f"Error: {e}")


def show_analysis_results():
    """Show analysis results page."""
    st.header("Analysis Results")
    
    # Get latest analysis
    latest_analysis = fetch_data("/analysis/latest")
    
    if latest_analysis:
        st.subheader("Latest Analysis")
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Posts", latest_analysis.get("total_posts", 0))
        with col2:
            st.metric("Total Comments", latest_analysis.get("total_comments", 0))
        with col3:
            st.metric("Subreddits Analyzed", latest_analysis.get("subreddits_analyzed", 0))
        with col4:
            st.metric("Trending Topics", len(latest_analysis.get("trending_topics", [])))
        
        # Time period
        time_period = latest_analysis.get("time_period", {})
        st.info(f"Analysis Period: {time_period.get('days', 'N/A')} days")
        
        # Category summaries
        st.subheader("Category Summaries")
        summaries = latest_analysis.get("category_summaries", {})
        st.json(summaries)
    else:
        st.warning("No analysis results found. Collect and analyze data first.")


def show_trending_topics():
    """Show trending topics page."""
    st.header("Trending Topics")
    
    latest_analysis = fetch_data("/analysis/latest")
    
    if latest_analysis:
        topics = latest_analysis.get("trending_topics", [])
        
        if topics:
            # Create DataFrame
            df = pd.DataFrame([
                {
                    "Topic": t["topic"],
                    "Mentions": t["mentions"],
                    "Trend": t["trend"],
                    "Subreddits": ", ".join(t["subreddits"])
                }
                for t in topics
            ])
            
            # Display table
            st.dataframe(df, use_container_width=True)
            
            # Visualization
            st.subheader("Trending Topics Visualization")
            
            fig = px.bar(
                df.head(20),
                x="Mentions",
                y="Topic",
                orientation="h",
                color="Trend",
                title="Top 20 Trending Topics",
                labels={"Mentions": "Number of Mentions", "Topic": "Topic"}
            )
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed view
            st.subheader("Topic Details")
            selected_topic = st.selectbox("Select a topic", df["Topic"].tolist())
            
            if selected_topic:
                topic_data = next((t for t in topics if t["topic"] == selected_topic), None)
                if topic_data:
                    st.json(topic_data)
        else:
            st.info("No trending topics found.")
    else:
        st.warning("No analysis results found. Collect and analyze data first.")


def show_common_questions():
    """Show common questions page."""
    st.header("Common Questions")
    
    latest_analysis = fetch_data("/analysis/latest")
    
    if latest_analysis:
        questions = latest_analysis.get("common_questions", [])
        
        if questions:
            # Create DataFrame
            df = pd.DataFrame([
                {
                    "Question": q["question"][:100] + "..." if len(q["question"]) > 100 else q["question"],
                    "Frequency": q["frequency"],
                    "Subreddits": ", ".join(q["subreddits"]),
                    "Avg Upvotes": q["avg_engagement"].get("avg_upvotes", 0),
                    "Avg Comments": q["avg_engagement"].get("avg_comments", 0)
                }
                for q in questions
            ])
            
            # Display table
            st.dataframe(df, use_container_width=True)
            
            # Visualization
            st.subheader("Question Frequency")
            fig = px.bar(
                df,
                x="Frequency",
                y="Question",
                orientation="h",
                title="Common Questions by Frequency",
                labels={"Frequency": "Frequency", "Question": "Question"}
            )
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed view
            st.subheader("Question Details")
            selected_idx = st.selectbox("Select a question", range(len(questions)))
            
            if selected_idx is not None:
                question_data = questions[selected_idx]
                st.json(question_data)
        else:
            st.info("No common questions found.")
    else:
        st.warning("No analysis results found. Collect and analyze data first.")


if __name__ == "__main__":
    main()

