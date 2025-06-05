"""
Context Manager for APL Context-Aware.

Provides energy level detection from user input text using simple
keyword and pattern matching. Designed to be lightweight and reliable
without external dependencies.
"""

import re
from typing import Dict, List, Any
from utils import logger


class ContextManager:
    """
    Manages context detection for user interactions.
    
    Analyzes user input text to determine energy levels and provides
    confidence scoring for the detection results.
    """
    
    def __init__(self):
        """Initialize the ContextManager with detection patterns."""
        self._setup_energy_patterns()
    
    def _setup_energy_patterns(self) -> None:
        """Set up keyword patterns for energy level detection."""
        
        # High energy indicators
        self.high_energy_patterns = {
            'enthusiasm': ['excited', 'pumped', 'motivated', 'enthusiastic', 'energetic'],
            'action_words': ['tackle', 'dive', 'build', 'create', 'ambitious', 'challenging'],
            'intensity': ['!!', 'amazing', 'awesome', 'fantastic', 'love', 'passionate'],
            'urgency': ['now', 'immediately', 'quickly', 'fast', 'urgent'],
            'confidence': ['definitely', 'absolutely', 'certainly', 'sure', 'confident']
        }
        
        # Low energy indicators  
        self.low_energy_patterns = {
            'fatigue': ['tired', 'exhausted', 'worn out', 'drained', 'sleepy'],
            'uncertainty': ['maybe', 'perhaps', 'not sure', 'think', 'might', 'possibly'],
            'hesitation': ['but', 'however', 'hmm', 'well', 'uh', 'er'],
            'small_scope': ['small', 'simple', 'easy', 'quick', 'little', 'minor'],
            'low_focus': ['distracted', 'unfocused', 'scattered', 'confused', 'lost', 'not feeling'],
            'minimal_energy': ['bit', 'a bit', 'kinda', 'sort of', 'let me think']
        }
        
        # Medium energy indicators (neutral or balanced)
        self.medium_energy_patterns = {
            'neutral_starters': ['what', 'how', 'when', 'where', 'can you', 'could you'],
            'planning': ['should', 'would', 'could', 'let me', 'planning', 'thinking'],
            'questions': ['?'],
            'moderate_action': ['work on', 'start', 'begin', 'try', 'attempt', 'ready to get started']
        }
    
    def detect_energy_level(self, text: str) -> Dict[str, Any]:
        """
        Detect energy level from user input text.
        
        Args:
            text: User input text to analyze
            
        Returns:
            Dict containing energy level, confidence score, and reasoning
        """
        if not text or not text.strip():
            return {
                "energy": "medium",
                "confidence": 0.5,
                "reasoning": "Empty input, defaulting to medium energy"
            }
        
        # Normalize text for analysis
        normalized_text = text.lower().strip()
        
        # Calculate pattern matches for each energy level
        high_score = self._calculate_pattern_score(normalized_text, self.high_energy_patterns)
        low_score = self._calculate_pattern_score(normalized_text, self.low_energy_patterns)
        medium_score = self._calculate_pattern_score(normalized_text, self.medium_energy_patterns)
        
        # Additional scoring adjustments
        exclamation_count = text.count('!')
        question_count = text.count('?')
        
        # Boost high energy for multiple exclamations
        if exclamation_count >= 2:
            high_score += 0.3
        elif exclamation_count == 1:
            high_score += 0.1
            
        # Boost medium energy for questions ONLY if no strong low energy signals
        if question_count > 0 and low_score < 0.2:
            medium_score += 0.2
        elif question_count > 0:
            # If there are low energy signals, reduce the question boost
            medium_score += 0.05
        
        # Check for mixed signals (high and low indicators together)
        mixed_signal_penalty = 0
        if high_score > 0 and low_score > 0:
            mixed_signal_penalty = 0.2
            
        # Apply penalty to all scores for mixed signals
        high_score = max(0, high_score - mixed_signal_penalty)
        low_score = max(0, low_score - mixed_signal_penalty)
        
        # Determine energy level and confidence
        scores = {
            'high': high_score,
            'medium': medium_score,
            'low': low_score
        }
        
        # Find the highest scoring energy level
        energy_level = max(scores, key=scores.get)
        max_score = scores[energy_level]
        
        # Calculate confidence based on score difference
        sorted_scores = sorted(scores.values(), reverse=True)
        if len(sorted_scores) > 1:
            score_difference = sorted_scores[0] - sorted_scores[1]
            confidence = min(0.95, max(0.3, 0.5 + score_difference))
        else:
            confidence = 0.5
            
        # Special case: if all scores are very low, default to medium with lower confidence
        if max_score < 0.1:
            energy_level = "medium"
            confidence = 0.4
            
        # Generate reasoning
        reasoning = self._generate_reasoning(energy_level, text, scores, mixed_signal_penalty > 0)
        
        result = {
            "energy": energy_level,
            "confidence": round(confidence, 2),
            "reasoning": reasoning
        }
        
        logger.debug(f"Energy detection: {result} for text: '{text[:50]}...'")
        return result
    
    def _calculate_pattern_score(self, text: str, patterns: Dict[str, List[str]]) -> float:
        """
        Calculate pattern match score for given text.
        
        Args:
            text: Normalized text to analyze
            patterns: Dictionary of pattern categories and keywords
            
        Returns:
            float: Pattern match score
        """
        total_score = 0.0
        
        for category, keywords in patterns.items():
            category_matches = 0
            for keyword in keywords:
                if keyword in text:
                    category_matches += 1
                    
            # Score based on category matches (diminishing returns)
            if category_matches > 0:
                category_score = min(0.3, 0.1 + (category_matches - 1) * 0.05)
                total_score += category_score
                
        return min(1.0, total_score)
    
    def _generate_reasoning(self, energy_level: str, text: str, scores: Dict[str, float], mixed_signals: bool) -> str:
        """
        Generate human-readable reasoning for the energy detection.
        
        Args:
            energy_level: Detected energy level
            text: Original text
            scores: Energy level scores
            mixed_signals: Whether mixed signals were detected
            
        Returns:
            str: Reasoning explanation
        """
        reasoning_parts = []
        
        if energy_level == "high":
            if '!' in text:
                reasoning_parts.append("enthusiasm markers (!)")
            if any(word in text.lower() for word in ['excited', 'pumped', 'motivated']):
                reasoning_parts.append("excitement keywords")
            if any(word in text.lower() for word in ['tackle', 'dive', 'build', 'ambitious']):
                reasoning_parts.append("action-oriented language")
                
        elif energy_level == "low":
            if any(word in text.lower() for word in ['tired', 'maybe', 'small', 'simple']):
                reasoning_parts.append("low-energy indicators")
            if any(word in text.lower() for word in ['not sure', 'perhaps', 'might']):
                reasoning_parts.append("uncertainty markers")
                
        elif energy_level == "medium":
            if '?' in text:
                reasoning_parts.append("question format")
            if any(word in text.lower() for word in ['what', 'how', 'should', 'could']):
                reasoning_parts.append("neutral inquiry language")
        
        if mixed_signals:
            reasoning_parts.append("mixed energy signals detected")
            
        if not reasoning_parts:
            reasoning_parts.append("general language patterns")
            
        base_reasoning = f"Detected {energy_level} energy based on " + ", ".join(reasoning_parts)
        
        # Add confidence note if low
        confidence = scores[energy_level]
        if confidence < 0.5:
            base_reasoning += " (low confidence detection)"
            
        return base_reasoning