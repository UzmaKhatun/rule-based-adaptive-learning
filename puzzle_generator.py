"""
Puzzle Generator Module
Generates math puzzles based on difficulty level
"""
import random
from typing import Dict, List

class PuzzleGenerator:
    """Generates math puzzles with varying difficulty levels"""
    
    DIFFICULTY_CONFIG = {
        'Easy': {
            'range': (1, 10),
            'operations': ['+', '-'],
            'description': 'Numbers 1-10, Addition & Subtraction'
        },
        'Medium': {
            'range': (1, 20),
            'operations': ['+', '-', '×'],
            'description': 'Numbers 1-20, Addition, Subtraction & Multiplication'
        },
        'Hard': {
            'range': (1, 50),
            'operations': ['+', '-', '×', '÷'],
            'description': 'Numbers 1-50, All Operations'
        }
    }
    
    def __init__(self):
        """Initialize the puzzle generator"""
        self.current_difficulty = 'Medium'
    
    def generate_puzzle(self, difficulty: str = None) -> Dict:
        """
        Generate a math puzzle based on difficulty level
        
        Args:
            difficulty: Difficulty level ('Easy', 'Medium', 'Hard')
            
        Returns:
            Dict containing puzzle question, answer, and metadata
        """
        if difficulty is None:
            difficulty = self.current_difficulty
            
        config = self.DIFFICULTY_CONFIG.get(difficulty, self.DIFFICULTY_CONFIG['Medium'])
        operation = random.choice(config['operations'])
        
        min_val, max_val = config['range']
        num1 = random.randint(min_val, max_val)
        num2 = random.randint(min_val, max_val)
        
        # Generate puzzle based on operation
        if operation == '+':
            answer = num1 + num2
            question = f"{num1} + {num2}"
            
        elif operation == '-':
            # Ensure positive result for easier understanding
            if num1 < num2:
                num1, num2 = num2, num1
            answer = num1 - num2
            question = f"{num1} - {num2}"
            
        elif operation == '×':
            answer = num1 * num2
            question = f"{num1} × {num2}"
            
        elif operation == '÷':
            # Ensure clean division
            answer = num2
            num1 = num1 * num2
            question = f"{num1} ÷ {num2}"
        
        return {
            'question': question,
            'answer': answer,
            'difficulty': difficulty,
            'operation': operation,
            'numbers': [num1, num2]
        }
    
    def set_difficulty(self, difficulty: str):
        """Set the current difficulty level"""
        if difficulty in self.DIFFICULTY_CONFIG:
            self.current_difficulty = difficulty
    
    def get_difficulty_info(self, difficulty: str = None) -> str:
        """Get description of difficulty level"""
        if difficulty is None:
            difficulty = self.current_difficulty
        return self.DIFFICULTY_CONFIG.get(difficulty, {}).get('description', '')