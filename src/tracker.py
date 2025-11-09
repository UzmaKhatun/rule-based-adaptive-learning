"""
Performance Tracker Module
Tracks user performance metrics and session data
"""
import time
from typing import Dict, List
from datetime import datetime

class PerformanceTracker:
    """Tracks user performance across puzzle attempts"""
    
    def __init__(self):
        """Initialize the performance tracker"""
        self.attempts: List[Dict] = []
        self.session_start = None
        self.current_attempt_start = None
    
    def start_session(self):
        """Start a new tracking session"""
        self.session_start = time.time()
        self.attempts = []
        self.start_attempt()
    
    def start_attempt(self):
        """Start timing a new puzzle attempt"""
        self.current_attempt_start = time.time()
    
    def log_attempt(self, puzzle: Dict, user_answer: int, is_correct: bool):
        """
        Log a puzzle attempt with performance metrics
        
        Args:
            puzzle: The puzzle dictionary
            user_answer: User's submitted answer
            is_correct: Whether the answer was correct
        """
        time_spent = time.time() - self.current_attempt_start
        
        attempt = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'puzzle': puzzle['question'],
            'correct_answer': puzzle['answer'],
            'user_answer': user_answer,
            'is_correct': is_correct,
            'time_spent': round(time_spent, 2),
            'difficulty': puzzle['difficulty'],
            'operation': puzzle['operation']
        }
        
        self.attempts.append(attempt)
        self.start_attempt()  # Start timing next attempt
    
    def get_session_stats(self) -> Dict:
        """
        Calculate session statistics
        
        Returns:
            Dictionary containing various performance metrics
        """
        if not self.attempts:
            return {
                'total_attempts': 0,
                'correct_count': 0,
                'accuracy': 0.0,
                'average_time': 0.0,
                'total_time': 0.0
            }
        
        correct_count = sum(1 for attempt in self.attempts if attempt['is_correct'])
        total_time = sum(attempt['time_spent'] for attempt in self.attempts)
        
        stats = {
            'total_attempts': len(self.attempts),
            'correct_count': correct_count,
            'incorrect_count': len(self.attempts) - correct_count,
            'accuracy': round((correct_count / len(self.attempts)) * 100, 1),
            'average_time': round(total_time / len(self.attempts), 2),
            'total_time': round(total_time, 2),
            'fastest_time': min(a['time_spent'] for a in self.attempts),
            'slowest_time': max(a['time_spent'] for a in self.attempts)
        }
        
        return stats
    
    def get_recent_performance(self, n: int = 3) -> List[Dict]:
        """
        Get the n most recent attempts
        
        Args:
            n: Number of recent attempts to retrieve
            
        Returns:
            List of recent attempt dictionaries
        """
        return self.attempts[-n:] if len(self.attempts) >= n else self.attempts
    
    def get_difficulty_distribution(self) -> Dict[str, int]:
        """
        Get count of attempts by difficulty level
        
        Returns:
            Dictionary mapping difficulty levels to attempt counts
        """
        distribution = {}
        for attempt in self.attempts:
            difficulty = attempt['difficulty']
            distribution[difficulty] = distribution.get(difficulty, 0) + 1
        return distribution
    
    def get_operation_performance(self) -> Dict[str, Dict]:
        """
        Get performance statistics by operation type
        
        Returns:
            Dictionary with performance metrics per operation
        """
        operation_stats = {}
        
        for attempt in self.attempts:
            op = attempt['operation']
            if op not in operation_stats:
                operation_stats[op] = {
                    'total': 0,
                    'correct': 0,
                    'times': []
                }
            
            operation_stats[op]['total'] += 1
            if attempt['is_correct']:
                operation_stats[op]['correct'] += 1
            operation_stats[op]['times'].append(attempt['time_spent'])
        
        # Calculate accuracy and average time for each operation
        for op in operation_stats:
            stats = operation_stats[op]
            stats['accuracy'] = round((stats['correct'] / stats['total']) * 100, 1)
            stats['avg_time'] = round(sum(stats['times']) / len(stats['times']), 2)
        
        return operation_stats