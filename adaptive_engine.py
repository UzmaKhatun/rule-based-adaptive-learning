"""
Adaptive Engine Module
Determines difficulty adjustments based on user performance
"""
from typing import Dict, List

class AdaptiveEngine:
    """
    Rule-based adaptive engine that adjusts difficulty based on performance
    
    Adaptation Rules:
    - If user answers 2+ of last 3 correctly AND average time < 8s → Increase difficulty
    - If user answers 1 or fewer of last 3 correctly → Decrease difficulty
    - Otherwise maintain current difficulty
    """
    
    DIFFICULTY_LEVELS = ['Easy', 'Medium', 'Hard']
    
    def __init__(self):
        """Initialize the adaptive engine"""
        self.current_difficulty = 'Medium'
        self.difficulty_history = []
    
    def adapt_difficulty(self, recent_attempts: List[Dict], current_difficulty: str) -> str:
        """
        Determine the next difficulty level based on recent performance
        
        Args:
            recent_attempts: List of recent attempt dictionaries
            current_difficulty: Current difficulty level
            
        Returns:
            Recommended difficulty level
        """
        # Need at least 2 attempts to make adaptation decisions
        if len(recent_attempts) < 2:
            return current_difficulty
        
        # Analyze recent performance
        correct_count = sum(1 for attempt in recent_attempts if attempt['is_correct'])
        avg_time = sum(attempt['time_spent'] for attempt in recent_attempts) / len(recent_attempts)
        
        # Get current difficulty index
        current_index = self.DIFFICULTY_LEVELS.index(current_difficulty)
        
        # Adaptation logic
        if correct_count >= 2 and avg_time < 8.0 and current_index < len(self.DIFFICULTY_LEVELS) - 1:
            # User is doing well - increase difficulty
            new_difficulty = self.DIFFICULTY_LEVELS[current_index + 1]
            reason = f"Great work! Moving to {new_difficulty} (accuracy: {correct_count}/{len(recent_attempts)})"
            
        elif correct_count <= 1 and current_index > 0:
            # User is struggling - decrease difficulty
            new_difficulty = self.DIFFICULTY_LEVELS[current_index - 1]
            reason = f"Let's try {new_difficulty} level (accuracy: {correct_count}/{len(recent_attempts)})"
            
        else:
            # Maintain current difficulty
            new_difficulty = current_difficulty
            reason = f"Staying at {current_difficulty} level"
        
        # Log difficulty change
        if new_difficulty != current_difficulty:
            self.difficulty_history.append({
                'from': current_difficulty,
                'to': new_difficulty,
                'reason': reason,
                'correct_count': correct_count,
                'total_attempts': len(recent_attempts),
                'avg_time': round(avg_time, 2)
            })
        
        self.current_difficulty = new_difficulty
        return new_difficulty
    
    def get_adaptation_summary(self) -> List[Dict]:
        """
        Get history of difficulty adaptations
        
        Returns:
            List of adaptation events
        """
        return self.difficulty_history
    
    def get_recommendation_explanation(self, recent_attempts: List[Dict]) -> str:
        """
        Get a detailed explanation of the adaptation decision
        
        Args:
            recent_attempts: List of recent attempts
            
        Returns:
            String explanation of the recommendation
        """
        if len(recent_attempts) < 2:
            return "Building your performance profile... Keep going!"
        
        correct_count = sum(1 for attempt in recent_attempts if attempt['is_correct'])
        avg_time = sum(attempt['time_spent'] for attempt in recent_attempts) / len(recent_attempts)
        
        explanation = f"Recent Performance Analysis:\n"
        explanation += f"✓ Correct: {correct_count}/{len(recent_attempts)}\n"
        explanation += f"⏱ Average Time: {avg_time:.1f}s\n\n"
        
        if correct_count >= 2 and avg_time < 8.0:
            explanation += "🎯 You're doing excellent! Ready for a challenge."
        elif correct_count <= 1:
            explanation += "💪 Let's work on building confidence at an easier level."
        else:
            explanation += "✨ You're at the perfect difficulty level. Keep it up!"
        
        return explanation