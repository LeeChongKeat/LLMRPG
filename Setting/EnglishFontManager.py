# EnglishFontManager.py
import os
import pygame

class EnglishFontManager:
    """
    English Font Manager for Pygame - Optimized for English text.
    Prioritizes Arial and common sans-serif fonts across platforms.
    Falls back gracefully to system defaults.
    """
    def __init__(self):
        """
        Initialize the font manager with three standard sizes:
        - font: main text (22px)
        - small_font: UI elements (18px)
        - tiny_font: hints/status (14px)
        """
        self.font = self.create_english_font(22)
        self.small_font = self.create_english_font(18)
        self.tiny_font = self.create_english_font(14)

    def create_english_font(self, size=22):
        """
        Creates a font suitable for English text, preferring Arial.
        Tries specific font files first, then system fonts.

        Args:
            size (int): Font size

        Returns:
            pygame.Font: A font object (Arial preferred), or fallback
        """
        # 1. Try Arial Unicode MS (common on Windows)
        arial_unicode_paths = [
            'C:/Windows/Fonts/ARIALUNI.TTF',           # Windows Arial Unicode
            'C:/Windows/Fonts/arial.ttf',              # Standard Arial
            '/usr/share/fonts/truetype/msttcorefonts/arial.ttf',  # Linux (if installed)
            '/System/Library/Fonts/Arial.ttf',         # macOS Arial
            '/System/Library/Fonts/Arial Unicode.ttf', # macOS fallback
        ]

        for font_path in arial_unicode_paths:
            if os.path.exists(font_path):
                try:
                    print(f"Using Arial font file: {font_path}")
                    return pygame.font.Font(font_path, size)
                except Exception as e:
                    print(f"Failed to load {font_path}: {e}")
                    continue

        # 2. Try system fonts with Arial priority
        try:
            print("Attempting to use Arial via SysFont...")
            # Try Arial first, then common sans-serif alternatives
            return pygame.font.SysFont('arial, helvetica, verdana, geneva, sans-serif', size)
        except Exception as e:
            print(f"SysFont with Arial failed: {e}")

        # 3. Final fallback: default pygame font
        try:
            print("Falling back to default system font.")
            return pygame.font.Font(None, size)
        except Exception:
            # Double fallback in case even Font(None) fails
            print("Using default font (via SysFont fallback).")
            return pygame.font.SysFont(None, size)