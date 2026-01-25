# Payal Kokane - M4 Memory Management
# Checkpoint manager for persistent memory

"""
Memory management module for the Ambient Email Agent.
Handles short-term (conversation) and long-term (preferences) memory persistence.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import json


class CheckpointManager:
    """
    Manages agent memory persistence using LangGraph checkpointing.
    
    Short-term memory: Conversation history stored in PostgreSQL checkpoints
    Long-term memory: User preferences and learned patterns
    """
    
    def __init__(self, db_connection=None):
        """
        Initialize checkpoint manager.
        
        Args:
            db_connection: Database connection for persistence
        """
        self.db = db_connection
        self.memory_cache = {}
    
    async def save_conversation_state(
        self,
        thread_id: str,
        state: Dict[str, Any]
    ) -> bool:
        """
        Save conversation state to checkpoint.
        
        Args:
            thread_id: Unique conversation identifier
            state: Current agent state to persist
            
        Returns:
            Success boolean
        """
        try:
            checkpoint_data = {
                "thread_id": thread_id,
                "state": state,
                "timestamp": datetime.now().isoformat()
            }
            
            if self.db:
                # Store in database
                # This is handled by LangGraph's AsyncPostgresSaver
                self.memory_cache[thread_id] = checkpoint_data
                return True
            else:
                # Fallback to in-memory
                self.memory_cache[thread_id] = checkpoint_data
                return True
                
        except Exception as e:
            print(f"Error saving checkpoint: {e}")
            return False
    
    async def load_conversation_state(
        self,
        thread_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Load conversation state from checkpoint.
        
        Args:
            thread_id: Conversation identifier
            
        Returns:
            Restored state or None
        """
        try:
            if thread_id in self.memory_cache:
                return self.memory_cache[thread_id]["state"]
            
            # If not in cache and db available, load from db
            # This is handled by LangGraph's checkpoint system
            return None
            
        except Exception as e:
            print(f"Error loading checkpoint: {e}")
            return None
    
    async def save_user_preferences(
        self,
        user_id: str,
        preferences: Dict[str, Any]
    ) -> bool:
        """
        Save long-term user preferences.
        
        Args:
            user_id: User identifier
            preferences: User preference dictionary
                Example: {"signature": "Best, John", "tone": "formal"}
        
        Returns:
            Success boolean
        """
        try:
            pref_key = f"prefs_{user_id}"
            self.memory_cache[pref_key] = {
                "user_id": user_id,
                "preferences": preferences,
                "updated_at": datetime.now().isoformat()
            }
            return True
            
        except Exception as e:
            print(f"Error saving preferences: {e}")
            return False
    
    async def load_user_preferences(
        self,
        user_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Load user preferences.
        
        Args:
            user_id: User identifier
            
        Returns:
            Preferences dictionary or default values
        """
        try:
            pref_key = f"prefs_{user_id}"
            if pref_key in self.memory_cache:
                return self.memory_cache[pref_key]["preferences"]
            
            # Return defaults if not found
            return {
                "signature": "Best regards",
                "tone": "professional",
                "auto_approve_safe": False
            }
            
        except Exception as e:
            print(f"Error loading preferences: {e}")
            return {
                "signature": "Best regards",
                "tone": "professional"
            }
    
    async def learn_from_edit(
        self,
        user_id: str,
        original_draft: str,
        edited_draft: str
    ) -> None:
        """
        Learn from human edits to improve future responses.
        
        Args:
            user_id: User identifier
            original_draft: Agent's original draft
            edited_draft: Human-edited version
        """
        try:
            # Extract patterns from edits
            # This is a placeholder for future ML-based learning
            
            learn_key = f"learn_{user_id}"
            if learn_key not in self.memory_cache:
                self.memory_cache[learn_key] = []
            
            self.memory_cache[learn_key].append({
                "original": original_draft,
                "edited": edited_draft,
                "timestamp": datetime.now().isoformat()
            })
            
            # Keep only last 100 examples
            if len(self.memory_cache[learn_key]) > 100:
                self.memory_cache[learn_key] = self.memory_cache[learn_key][-100:]
                
        except Exception as e:
            print(f"Error in learning: {e}")
    
    def clear_old_checkpoints(self, days_old: int = 30) -> int:
        """
        Clean up old checkpoints.
        
        Args:
            days_old: Age threshold in days
            
        Returns:
            Number of checkpoints deleted
        """
        # Placeholder for cleanup logic
        # In production, this would query the database
        return 0


# Singleton instance
_checkpoint_manager = None


def get_checkpoint_manager(db=None) -> CheckpointManager:
    """
    Get or create global checkpoint manager instance.
    
    Args:
        db: Optional database connection
        
    Returns:
        CheckpointManager instance
    """
    global _checkpoint_manager
    if _checkpoint_manager is None:
        _checkpoint_manager = CheckpointManager(db)
    return _checkpoint_manager
