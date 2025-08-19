import pygame
import sys
import math
import time
import requests

from Setting.Configuration import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, OLLAMA_MODEL,
    SKY_BLUE, WHITE, YELLOW, WALL_COLOR, FLOOR_COLOR, PLAYER_BLUE, BLACK
)
from LLM.OllamaAPI import OllamaAPI
from Player.Player import Player
from Player.NPC import NPC
from Setting.ChineseFontManager import ChineseFontManager
from Setting.EnglishFontManager import EnglishFontManager
from Env.RoomEnvironment import RoomEnvironment
from Setting.DialogueSystem import DialogueSystem


class Game:
    """Main game class"""
    def __init__(self):
        # Initialize display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("LLM RPG Game - AI Dialogue Edition")
        self.clock = pygame.time.Clock()
        
        # Initialize Chinese font support
        self.font_manager = EnglishFontManager()
        self.font = self.font_manager.font
        self.small_font = self.font_manager.small_font
        self.tiny_font = self.font_manager.tiny_font
        
        # Initialize Ollama API
        self.ollama_api = OllamaAPI(OLLAMA_MODEL)
        
        # Create game objects
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.room_env = RoomEnvironment()
        self.dialogue_system = DialogueSystem(self.font, self.small_font, self.tiny_font)
        
        # Create NPCs
        self.npcs = self.create_npcs()
        
        # Game state
        self.running = True
        self.show_title = False
        self.game_started = True

    def create_npcs(self):
        """Create and return a list of NPCs"""
        npcs = []
        
        # Colleague 1 (cat)
        librarian = NPC(124, 217, "Colleague 1", "animal", "wise")
        npcs.append(librarian)
        
        # Colleague 2 (rabbit)
        woman = NPC(193, 217, "Colleague 2", "animal", "mysterious")
        npcs.append(woman)
        
        # Colleague 3 (bear)
        butler = NPC(194, 348, "Colleague 3", "animal", "friendly")
        npcs.append(butler)
        
        # Resident (fox)
        resident = NPC(374, 348, "GTP", "animal", "playful")
        npcs.append(resident)

        # Programmer NPC
        programmer = NPC(363, 217, "Lee Chong Keat", "animal", "programmer")
        npcs.append(programmer)
        
        return npcs

    def check_npc_interaction(self):
        """Check if player is close enough to interact with an NPC"""
        if self.dialogue_system.active:
            return None
            
        for npc in self.npcs:
            distance = math.sqrt((self.player.x - npc.x)**2 + (self.player.y - npc.y)**2)
            if distance < 40:
                print(f"Detected NPC: {npc.name}, Distance: {distance:.2f}")
                return npc
        return None

    def handle_events(self):
        """Handle all user input and events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                print("Game exiting...")

            # Title screen input
            if self.show_title:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print("Game started")
                        self.show_title = False
                        self.game_started = True

            # Dialogue system input
            elif self.dialogue_system.active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print("Exiting dialogue")
                        self.dialogue_system.end_dialogue()
                    elif event.key == pygame.K_RETURN:
                        if self.dialogue_system.input_active and not self.dialogue_system.is_thinking:
                            # Rate limiting for message sending
                            if not hasattr(self, '_last_send_time'):
                                self._last_send_time = 0
                            current_time = time.time()
                            if current_time - self._last_send_time > 0.5:  # Minimum 0.5s between sends
                                print("Sending message")
                                self.dialogue_system.send_message(self.ollama_api)
                                self._last_send_time = current_time
                    elif event.key == pygame.K_BACKSPACE:
                        self.dialogue_system.remove_input_char()
                    elif event.key == pygame.K_UP:
                        self.dialogue_system.scroll_up()
                    elif event.key == pygame.K_DOWN:
                        self.dialogue_system.scroll_down()
                    else:
                        # Handle printable characters
                        if event.unicode and event.unicode.isprintable() and event.unicode != '\r':
                            self.dialogue_system.add_input_char(event.unicode)
                            print(f"Input character: {repr(event.unicode)}")
            else:
                # Game input (outside dialogue)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        print("Z key pressed")
                        npc = self.check_npc_interaction()
                        if npc:
                            print(f"Starting dialogue with {npc.name}")
                            self.dialogue_system.start_dialogue(npc)
                        else:
                            print("No NPC nearby")

    def update(self):
        """Update game logic"""
        if self.show_title:
            return
            
        # Update dialogue system
        if self.dialogue_system.active:
            self.dialogue_system.update_cursor()
            self.dialogue_system.update_thinking_process()
            
        # Handle player movement
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        # Only allow movement when not in dialogue
        if not self.dialogue_system.active:
            if keys[pygame.K_UP]:
                dy = -1
            if keys[pygame.K_DOWN]:
                dy = 1
            if keys[pygame.K_LEFT]:
                dx = -1
            if keys[pygame.K_RIGHT]:
                dx = 1
            
            # Get obstacles from environment and move player
            obstacles = self.room_env.get_obstacles()
            self.player.move(dx, dy, obstacles)

    def draw_title_screen(self):
        """Draw the title screen"""
        self.screen.fill(SKY_BLUE)
        
        # Draw title
        title_text = "LLM RPG Game - AI Dialogue Edition"
        try:
            title_surface = self.font.render(title_text, True, WHITE)
            title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            self.screen.blit(title_surface, title_rect)
        except:
            pass
        
        # Draw subtitle
        subtitle_text = "Press SPACE to start"
        try:
            subtitle_surface = self.small_font.render(subtitle_text, True, WHITE)
            subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
            self.screen.blit(subtitle_surface, subtitle_rect)
        except:
            pass
        
        # Draw controls hint
        hint_text = "Use arrow keys to move, press Z to talk to NPCs"
        try:
            hint_surface = self.small_font.render(hint_text, True, WHITE)
            hint_rect = hint_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 70))
            self.screen.blit(hint_surface, hint_rect)
        except:
            pass
        
        # Draw AI model info
        ai_hint_text = f"Using OLLAMA Model: {OLLAMA_MODEL}"
        try:
            ai_hint_surface = self.small_font.render(ai_hint_text, True, WHITE)
            ai_hint_rect = ai_hint_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 120))
            self.screen.blit(ai_hint_surface, ai_hint_rect)
        except:
            pass
        
        # Draw feature highlight
        feature_text = "Real-time display of model thinking process"
        try:
            feature_surface = self.tiny_font.render(feature_text, True, YELLOW)
            feature_rect = feature_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 160))
            self.screen.blit(feature_surface, feature_rect)
        except:
            pass
        
        # Draw decorative room
        pygame.draw.rect(self.screen, WALL_COLOR, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 180, 200, 100))
        pygame.draw.rect(self.screen, FLOOR_COLOR, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 + 200, 160, 60))
        
        # Draw player character
        pygame.draw.rect(self.screen, PLAYER_BLUE, (SCREEN_WIDTH//2 - 12, SCREEN_HEIGHT//2 + 220, 24, 24))

    def draw_game(self):
        """Draw the main game screen"""
        # Draw environment
        self.room_env.draw_room(self.screen)
        
        # Draw NPCs
        for npc in self.npcs:
            npc.draw(self.screen)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw dialogue box
        self.dialogue_system.draw_dialogue_box(self.screen)
        
        # Draw controls hint (when not in dialogue)
        if not self.dialogue_system.active:
            hint_text = "Arrow keys: Move | Z: Talk | ESC: Exit dialogue"
            try:
                hint_surface = self.tiny_font.render(hint_text, True, WHITE)
                # Background for better readability
                hint_rect = pygame.Rect(10, 10, 350, 30)
                pygame.draw.rect(self.screen, (0, 0, 0, 180), hint_rect)
                pygame.draw.rect(self.screen, WHITE, hint_rect, 1)
                self.screen.blit(hint_surface, (15, 15))
            except:
                pass
        
        # Draw NPC labels when nearby
        if not self.dialogue_system.active:
            for npc in self.npcs:
                distance = math.sqrt((self.player.x - npc.x)**2 + (self.player.y - npc.y)**2)
                if distance < 60:
                    try:
                        name_surface = self.small_font.render(npc.name, True, WHITE)
                        name_width = name_surface.get_width()
                        name_height = name_surface.get_height()
                        
                        # Position above NPC (centered)
                        npc_center_x = npc.x + npc.width // 2
                        npc_center_y = npc.y + npc.height // 2
                        
                        name_x = npc_center_x - name_width // 2
                        name_y = npc_center_y - npc.height - 20
                        
                        # Background for readability
                        name_bg_rect = pygame.Rect(name_x - 5, name_y - 5, name_width + 10, name_height + 10)
                        pygame.draw.rect(self.screen, (0, 0, 0, 180), name_bg_rect)
                        pygame.draw.rect(self.screen, WHITE, name_bg_rect, 1)
                        self.screen.blit(name_surface, (name_x, name_y))
                    except Exception as e:
                        print(f"Error rendering NPC name: {e}")

    def draw(self):
        """Draw the current screen"""
        if self.show_title:
            self.draw_title_screen()
        else:
            self.draw_game()
        
        pygame.display.flip()

    def run(self):
        """Main game loop"""
        print("Starting game...")
        print(f"Using OLLAMA model: Local large language model")
        print("Please ensure the OLLAMA service is running")
        
        # Check OLLAMA service availability
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                models = [model['name'] for model in data.get('models', [])]
                print("✓ OLLAMA service connected successfully")
                if OLLAMA_MODEL in models:
                    print(f"✓ Model found: {OLLAMA_MODEL}")
                else:
                    print(f"⚠ Model not found: {OLLAMA_MODEL}, please ensure it's downloaded")
                    print("Available models:", models)
            else:
                print("⚠ Failed to connect to OLLAMA service, please ensure it's running")
        except Exception as e:
            print(f"⚠ Unable to connect to OLLAMA service: {e}")
            print("Please ensure the OLLAMA service is running")
        
        # Main game loop
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        # Cleanup
        pygame.quit()
        sys.exit()