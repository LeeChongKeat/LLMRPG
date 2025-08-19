import pygame
import sys

from Init.Game import Game

# Initialize pygame
pygame.init()

# Run the game
if __name__ == "__main__":
    try:
        print("=" * 60)
        print("LLM RPG Game - AI Dialogue Version (qwen3:8b)")
        print("=" * 60)
        print("✨ Features: Real-time display of model thinking process")
        print("=" * 60)
        print("Instructions:")
        print("1. Make sure the OLLAMA service is running")
        print("2. Ensure the qwen3:8b model is downloaded: ollama pull qwen3:8b")
        print("3. Use arrow keys to move the character")
        print("4. Press Z key to start conversation when near an NPC")
        print("5. Type in the chat box and press Enter to send")
        print("6. Watch the model's thinking and text generation in real time")
        print("7. Use ↑↓ keys to scroll and view full content")
        print("8. Press ESC to exit the conversation")
        print("=" * 60)
        
        # Check for required dependencies
        try:
            import pygame
            import requests
            print("✓ Required dependencies are installed")
        except ImportError as e:
            print(f"⚠ Missing dependency: {e}")
            print("Please run: pip install pygame requests")
            input("Press Enter to exit...")
            sys.exit(1)
        
        game = Game()
        game.run()
        
    except Exception as e:
        print(f"Error running the game: {e}")
        import traceback
        traceback.print_exc()
        print("\nPlease ensure the following:")
        print("1. pygame is installed: pip install pygame")
        print("2. requests is installed: pip install requests")
        print("3. OLLAMA service is running")
        print("4. qwen3:8b model is downloaded: ollama pull qwen3:8b")
        input("Press Enter to exit...")