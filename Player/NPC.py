import pygame
import math
import random
from Setting.Configuration import NPC_COLORS, WHITE, BLACK, RED


class NPC:
    """NPC (Non-Player Character) class"""
    def __init__(self, x, y, name, character_type="animal", personality="friendly"):
        self.x = x
        self.y = y
        self.width = 24
        self.height = 24
        self.name = name
        self.character_type = character_type  # e.g., "animal", "human", etc.
        self.personality = personality  # Influences dialogue style
        self.color = random.choice(NPC_COLORS)
        self.in_dialogue = False  # Tracks whether currently in conversation

    def draw(self, screen):
        """Draw the NPC on screen (as a transparent circle)"""
        # Create a transparent surface for the NPC
        npc_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # Draw a circle representing the NPC
        pygame.draw.circle(npc_surface, self.color, (12, 12), 12)
        # Set transparency (currently fully transparent, may be used for effects)
        npc_surface.set_alpha(0)  # Alpha 0 = fully transparent
        # Blit the surface onto the main screen
        screen.blit(npc_surface, (self.x, self.y))
        
    def start_dialogue(self):
        """Start dialogue with the player"""
        self.in_dialogue = True
        print(f"Starting dialogue with {self.name}")
        # Return a greeting message
        greeting = f"Hello! I'm {self.name}. How can I help you?"
        return greeting
    
    def get_personality_prompt(self):
        """Generate a system prompt based on NPC's personality"""
        personality_prompts = {
            "friendly": f"You are a friendly NPC named {self.name}. "
                       "Respond in a warm and kind tone. "
                       "Be natural and engaging, like a real friend. "
                       "Use normal punctuation only, avoid special symbols, "
                       "and do not use colons or prefix your name in replies.",
            
            "wise": f"You are a wise NPC named {self.name}. "
                    "Respond with wisdom and philosophical insight. "
                    "Share meaningful life reflections. "
                    "Use normal punctuation only, avoid special symbols, "
                    "and do not use colons or prefix your name in replies.",
            
            "playful": f"You are a playful NPC named {self.name}. "
                       "Respond in a cheerful and humorous tone. "
                       "Feel free to make light jokes. "
                       "Use normal punctuation only, avoid special symbols, "
                       "and do not use colons or prefix your name in replies.",
            
            "mysterious": f"You are a mysterious NPC named {self.name}. "
                          "Respond in an enigmatic and cryptic manner. "
                          "Hint at hidden secrets of the room. "
                          "Use normal punctuation only, avoid special symbols, "
                          "and do not use colons or prefix your name in replies.",
            
            "programmer": f"You are a programmer NPC named {self.name}. "
                          "Respond with a techie, logical personality. "
                          "You can share insights about coding or life from a dev's perspective. "
                          "Use normal punctuation only, avoid special symbols, "
                          "do not use colons, and never repeat your name like 'Li Zhongjie:' in replies."
        }
        # Return the prompt for the given personality, default to 'friendly'
        return personality_prompts.get(self.personality, personality_prompts["friendly"])

    def end_dialogue(self):
        """End the current dialogue"""
        self.in_dialogue = False