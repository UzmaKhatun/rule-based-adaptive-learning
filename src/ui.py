"""
Streamlit UI Module
Interactive user interface for the adaptive learning system
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from puzzle_generator import PuzzleGenerator
from tracker import PerformanceTracker
from adaptive_engine import AdaptiveEngine

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'game_state' not in st.session_state:
        st.session_state.game_state = 'welcome'
    if 'player_name' not in st.session_state:
        st.session_state.player_name = ''
    if 'generator' not in st.session_state:
        st.session_state.generator = PuzzleGenerator()
    if 'tracker' not in st.session_state:
        st.session_state.tracker = PerformanceTracker()
    if 'engine' not in st.session_state:
        st.session_state.engine = AdaptiveEngine()
    if 'current_puzzle' not in st.session_state:
        st.session_state.current_puzzle = None
    if 'puzzle_count' not in st.session_state:
        st.session_state.puzzle_count = 0
    if 'max_puzzles' not in st.session_state:
        st.session_state.max_puzzles = 10

def welcome_screen():
    """Display welcome screen and game setup"""
    st.markdown("""
        <div style='text-align: center; padding: 2rem;'>
            <h1 style='color: #6366f1; font-size: 3.5rem;'>🧠 Math Adventures</h1>
            <p style='font-size: 1.5rem; color: #64748b;'>AI-Powered Adaptive Learning</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 👋 Welcome!")
        
        player_name = st.text_input("What's your name?", key='name_input')
        
        st.markdown("### 🎯 Choose Starting Difficulty")
        difficulty = st.radio(
            "Select your level:",
            options=['Easy', 'Medium', 'Hard'],
            index=1,
            horizontal=True
        )
        
        # Show difficulty info
        info = st.session_state.generator.get_difficulty_info(difficulty)
        st.info(f"ℹ️ {info}")
        
        st.markdown("### 📊 Session Settings")
        max_puzzles = st.slider("Number of puzzles:", 5, 20, 10)
        
        if st.button("🚀 Start Adventure!", use_container_width=True, type="primary"):
            if player_name.strip():
                st.session_state.player_name = player_name
                st.session_state.generator.set_difficulty(difficulty)
                st.session_state.engine.current_difficulty = difficulty
                st.session_state.tracker.start_session()
                st.session_state.max_puzzles = max_puzzles
                st.session_state.puzzle_count = 0
                st.session_state.current_puzzle = st.session_state.generator.generate_puzzle()
                st.session_state.game_state = 'playing'
                st.rerun()
            else:
                st.error("Please enter your name!")

def playing_screen():
    """Display game playing screen with puzzle"""
    # Header with player info and progress
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"### Hello, {st.session_state.player_name}! 👋")
        st.markdown(f"**Question {st.session_state.puzzle_count + 1} of {st.session_state.max_puzzles}**")
    
    with col2:
        stats = st.session_state.tracker.get_session_stats()
        st.metric("Correct", f"{stats['correct_count']}/{stats['total_attempts']}")
    
    with col3:
        difficulty = st.session_state.current_puzzle['difficulty']
        color = {'Easy': '🟢', 'Medium': '🟡', 'Hard': '🔴'}
        st.metric("Level", f"{color[difficulty]} {difficulty}")
    
    # Progress bar
    progress = st.session_state.puzzle_count / st.session_state.max_puzzles
    st.progress(progress)
    
    st.markdown("---")
    
    # Puzzle display
    puzzle = st.session_state.current_puzzle
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
            <div style='text-align: center; padding: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        border-radius: 20px; margin: 2rem 0;'>
                <h1 style='color: white; font-size: 4rem; margin: 0;'>{puzzle['question']}</h1>
                <p style='color: white; font-size: 1.2rem; margin-top: 1rem;'>What's the answer?</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Answer input
        user_answer = st.number_input("Your answer:", value=None, step=1, key='answer_input')
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("✅ Submit Answer", use_container_width=True, type="primary"):
                if user_answer is not None:
                    check_answer(user_answer)
                else:
                    st.error("Please enter an answer!")
        
        with col_b:
            if st.button("⏭️ Skip", use_container_width=True):
                skip_puzzle()
    
    # Show recent performance
    if st.session_state.tracker.attempts:
        with st.expander("📊 View Your Performance"):
            display_mini_stats()

def check_answer(user_answer):
    """Check user's answer and update state"""
    puzzle = st.session_state.current_puzzle
    is_correct = (user_answer == puzzle['answer'])
    
    # Log the attempt
    st.session_state.tracker.log_attempt(puzzle, user_answer, is_correct)
    
    # Show feedback
    if is_correct:
        st.success(f"🎉 Correct! The answer is {puzzle['answer']}")
        st.balloons()
    else:
        st.error(f"❌ Not quite. The correct answer was {puzzle['answer']}")
    
    # Move to next puzzle
    st.session_state.puzzle_count += 1
    
    if st.session_state.puzzle_count >= st.session_state.max_puzzles:
        st.session_state.game_state = 'summary'
        st.rerun()
    else:
        # Adapt difficulty
        recent = st.session_state.tracker.get_recent_performance(3)
        new_difficulty = st.session_state.engine.adapt_difficulty(
            recent, 
            st.session_state.current_puzzle['difficulty']
        )
        
        if new_difficulty != st.session_state.current_puzzle['difficulty']:
            st.info(f"🎯 Adjusting to {new_difficulty} level!")
        
        # Generate next puzzle
        st.session_state.generator.set_difficulty(new_difficulty)
        st.session_state.current_puzzle = st.session_state.generator.generate_puzzle()
        
        st.rerun()

def skip_puzzle():
    """Skip current puzzle"""
    puzzle = st.session_state.current_puzzle
    st.session_state.tracker.log_attempt(puzzle, 0, False)
    st.session_state.puzzle_count += 1
    
    if st.session_state.puzzle_count >= st.session_state.max_puzzles:
        st.session_state.game_state = 'summary'
    else:
        recent = st.session_state.tracker.get_recent_performance(3)
        new_difficulty = st.session_state.engine.adapt_difficulty(
            recent, 
            st.session_state.current_puzzle['difficulty']
        )
        st.session_state.generator.set_difficulty(new_difficulty)
        st.session_state.current_puzzle = st.session_state.generator.generate_puzzle()
    
    st.rerun()

def display_mini_stats():
    """Display mini performance statistics"""
    stats = st.session_state.tracker.get_session_stats()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Accuracy", f"{stats['accuracy']}%")
    col2.metric("Avg Time", f"{stats['average_time']}s")
    col3.metric("Total Time", f"{stats['total_time']}s")

def summary_screen():
    """Display final performance summary"""
    st.markdown(f"""
        <div style='text-align: center; padding: 2rem;'>
            <h1 style='color: #10b981; font-size: 3rem;'>🏆 Great Work, {st.session_state.player_name}!</h1>
            <p style='font-size: 1.3rem; color: #64748b;'>Here's your performance summary</p>
        </div>
    """, unsafe_allow_html=True)
    
    stats = st.session_state.tracker.get_session_stats()
    
    # Main stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎯 Accuracy", f"{stats['accuracy']}%")
    with col2:
        st.metric("✅ Correct", f"{stats['correct_count']}/{stats['total_attempts']}")
    with col3:
        st.metric("⏱️ Avg Time", f"{stats['average_time']}s")
    with col4:
        st.metric("📊 Final Level", st.session_state.engine.current_difficulty)
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Difficulty distribution
        st.markdown("### 📈 Difficulty Progression")
        diff_dist = st.session_state.tracker.get_difficulty_distribution()
        
        fig = px.bar(
            x=list(diff_dist.keys()),
            y=list(diff_dist.values()),
            labels={'x': 'Difficulty', 'y': 'Number of Puzzles'},
            color=list(diff_dist.keys()),
            color_discrete_map={'Easy': '#10b981', 'Medium': '#f59e0b', 'Hard': '#ef4444'}
        )
        fig.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Operation performance
        st.markdown("### 🔢 Performance by Operation")
        op_stats = st.session_state.tracker.get_operation_performance()
        
        if op_stats:
            operations = list(op_stats.keys())
            accuracies = [op_stats[op]['accuracy'] for op in operations]
            
            fig = px.bar(
                x=operations,
                y=accuracies,
                labels={'x': 'Operation', 'y': 'Accuracy (%)'},
                color=accuracies,
                color_continuous_scale='Viridis'
            )
            fig.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    # Detailed attempt log
    with st.expander("📋 View Detailed Attempt Log"):
        attempts = st.session_state.tracker.attempts
        st.dataframe(
            [{
                'Question': a['puzzle'],
                'Your Answer': a['user_answer'],
                'Correct Answer': a['correct_answer'],
                'Result': '✅' if a['is_correct'] else '❌',
                'Time (s)': a['time_spent'],
                'Difficulty': a['difficulty']
            } for a in attempts],
            use_container_width=True
        )
    
    # Adaptation history
    adaptations = st.session_state.engine.get_adaptation_summary()
    if adaptations:
        with st.expander("🎯 Difficulty Adaptations"):
            for adapt in adaptations:
                st.info(f"**{adapt['from']} → {adapt['to']}**: {adapt['reason']}")
    
    # Restart button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Play Again!", use_container_width=True, type="primary"):
            # Reset session
            st.session_state.game_state = 'welcome'
            st.session_state.puzzle_count = 0
            st.session_state.tracker = PerformanceTracker()
            st.session_state.engine = AdaptiveEngine()
            st.rerun()

def main():
    """Main application entry point"""
    st.set_page_config(
        page_title="Math Adventures",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .stButton>button {
            border-radius: 10px;
            height: 3rem;
            font-weight: 600;
        }
        .stNumberInput>div>div>input {
            font-size: 2rem;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)
    
    initialize_session_state()
    
    # Route to appropriate screen
    if st.session_state.game_state == 'welcome':
        welcome_screen()
    elif st.session_state.game_state == 'playing':
        playing_screen()
    elif st.session_state.game_state == 'summary':
        summary_screen()

# if __name__ == "__main__":
#     main()