import pygame
import threading
import queue
from Setting.Configuration import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GRAY, RED, OLLAMA_MODEL


class DialogueSystem:
    """Dialogue system for handling NPC conversations with streaming AI responses"""
    
    def __init__(self, font, small_font, tiny_font):
        """
        Initialize the dialogue system
        
        Args:
            font: Main font for NPC names
            small_font: Font for dialogue text
            tiny_font: Font for status/information text
        """
        self.font = font
        self.small_font = small_font
        self.tiny_font = tiny_font
        
        # System state
        self.active = False                  # Whether dialogue is active
        self.current_npc = None              # Current NPC being talked to
        self.input_active = True             # Whether player can type
        self.is_thinking = False             # Whether AI is generating response
        
        # Text content
        self.player_input = ""               # Current player input
        self.npc_response = ""               # Final NPC response
        self.thinking_process = ""           # Live thinking process (with <think> tags)
        self.final_response = ""             # Cleaned final response
        self.processed_content = ""          # Accumulated raw content from stream
        self.conversation_history = []       # History of conversation
        
        # Visual effects
        self.show_cursor = True              # Blinking cursor visibility
        self.cursor_timer = 0                # Timer for cursor blinking
        self.scroll_offset = 0               # Current scroll position
        self.auto_scroll = True              # Auto-scroll to newest content
        
        # Display settings
        self.text_height = 18                # Height of each text line
        self.max_visible_lines = 10          # Max lines visible in dialogue box
        self.show_thinking_process = True    # Show thinking process vs final response
        self.think_removed = False           # Whether <think> tags have been processed
        
        # Communication
        self.response_queue = queue.Queue()  # Thread-safe queue for AI responses
        self.api_thread = None               # Background thread for API calls
    
    def start_dialogue(self, npc):
        """
        Start a conversation with an NPC
        
        Args:
            npc: The NPC object to converse with
            
        Returns:
            str: Initial greeting message
        """
        print(f"Starting dialogue with {npc.name}")
        self.active = True
        self.current_npc = npc
        self.player_input = ""
        self.npc_response = ""
        self.thinking_process = f"Hello! I'm {npc.name}. How can I help you?"
        self.final_response = ""
        self.processed_content = ""
        self.input_active = True
        self.is_thinking = False
        self.conversation_history = [self.thinking_process]
        self.scroll_offset = 0
        self.show_thinking_process = True
        self.think_removed = False
        self.auto_scroll = True
        return self.thinking_process
    
    def add_input_char(self, char):
        """Add a character to player input (with length limit)"""
        if self.input_active and len(self.player_input) < 150:
            self.player_input += char
    
    def remove_input_char(self):
        """Remove the last character from player input"""
        if self.input_active and self.player_input:
            self.player_input = self.player_input[:-1]
    
    def send_message(self, ollama_api):
        """
        Send player message and start AI response generation
        
        Args:
            ollama_api: OllamaAPI instance for calling the LLM
        """
        if self.player_input.strip() and self.current_npc and not self.is_thinking:
            user_message = self.player_input.strip()
            print(f"Sending message: {user_message}")
            
            # Add to conversation history
            self.conversation_history.append(f"Player: {user_message}")
            
            # Reset response fields and enter thinking state
            self.npc_response = ""
            self.thinking_process = "Thinking..."
            self.final_response = ""
            self.processed_content = ""
            self.is_thinking = True
            self.player_input = ""
            self.input_active = False
            self.scroll_offset = 0
            self.show_thinking_process = True
            self.think_removed = False
            self.auto_scroll = True
            
            # Start API call in background thread
            def api_call():
                system_prompt = self.current_npc.get_personality_prompt()
                print("Conversation history:", self.conversation_history)
                
                # Use recent history only (last 10 messages)
                recent_history = self.conversation_history[-10:] if len(self.conversation_history) > 10 else self.conversation_history
                conversation_context = "\n".join(recent_history)
                
                full_prompt = f"{conversation_context}\nPlayer: {user_message}\n{self.current_npc.name}: "
                
                # Call streaming API
                ollama_api.generate_response_stream(full_prompt, system_prompt, self.response_queue)
            
            self.api_thread = threading.Thread(target=api_call)
            self.api_thread.daemon = True
            self.api_thread.start()
    
    def remove_think_tags(self, text):
        """
        Remove <think> tags from text, replacing them with thinking indicators
        
        Args:
            text (str): Text containing <think> tags
            
        Returns:
            str: Cleaned text
        """
        result = text
        # Remove all <think>...</think> blocks
        while "<think>" in result and "</think>" in result:
            start_idx = result.find("<think>")
            end_idx = result.find("</think>") + 8
            if start_idx >= 0 and end_idx > start_idx:
                result = result[:start_idx] + result[end_idx:]
            else:
                break
        
        # Replace remaining tags
        result = result.replace("</think>", "")
        result = result.replace("<think>", "Thinking...")
        return result.strip()
    
    def update_thinking_process(self):
        """Process incoming AI response chunks from the queue"""
        if self.is_thinking and not self.response_queue.empty():
            try:
                while not self.response_queue.empty():
                    msg_type, content = self.response_queue.get_nowait()
                    
                    if msg_type == 'chunk':
                        # Accumulate content
                        self.processed_content += content
                        
                        # Process think tags
                        cleaned_content = self.remove_think_tags(self.processed_content)
                        
                        # Update display based on think tag status
                        if len(cleaned_content) != len(self.processed_content):
                            self.think_removed = True
                            if "Thinking..." in self.thinking_process:
                                self.thinking_process = ""
                        
                        if self.think_removed:
                            self.thinking_process = cleaned_content
                            self.npc_response = cleaned_content
                        else:
                            self.thinking_process = self.processed_content
                            self.npc_response = self.processed_content
                        
                        # Auto-scroll to newest content
                        if self.auto_scroll:
                            self.update_scroll_position()
                    
                    elif msg_type == 'error':
                        # Handle errors
                        error_msg = f"❌ Error: {content}"
                        self.thinking_process = error_msg
                        self.npc_response = error_msg
                        self.final_response = error_msg
                        self.is_thinking = False
                        self.input_active = True
                        self.show_thinking_process = False
                        self.think_removed = True
                        self.auto_scroll = False
                        break
                        
            except queue.Empty:
                pass
    
    def update_scroll_position(self):
        """Update scroll position to show newest content"""
        display_text = self.thinking_process if self.show_thinking_process else self.npc_response
        lines = self.wrap_text(display_text, 25)
        max_scroll = max(0, len(lines) - self.max_visible_lines)
        self.scroll_offset = max_scroll
    
    def end_dialogue(self):
        """End the current dialogue session"""
        print("Ending dialogue")
        self.active = False
        if self.current_npc:
            self.current_npc.end_dialogue()
        
        # Reset all dialogue state
        self.current_npc = None
        self.player_input = ""
        self.npc_response = ""
        self.thinking_process = ""
        self.final_response = ""
        self.processed_content = ""
        self.input_active = True
        self.is_thinking = False
        self.conversation_history = []
        self.scroll_offset = 0
        self.show_thinking_process = True
        self.think_removed = False
        self.auto_scroll = True
        
        # Clear response queue
        while not self.response_queue.empty():
            try:
                self.response_queue.get_nowait()
            except queue.Empty:
                break
    
    def update_cursor(self):
        """Update blinking cursor state"""
        self.cursor_timer += 1
        if self.cursor_timer >= 30:  # ~0.5 seconds at 60 FPS
            self.show_cursor = not self.show_cursor
            self.cursor_timer = 0
    
    def scroll_up(self):
        """Scroll up one line"""
        if self.scroll_offset > 0:
            self.scroll_offset -= 1
            self.auto_scroll = False  # Disable auto-scroll when manually scrolling
    
    def scroll_down(self):
        """Scroll down one line"""
        display_text = self.thinking_process if self.show_thinking_process else self.npc_response
        lines = self.wrap_text(display_text, 25)
        max_scroll = max(0, len(lines) - self.max_visible_lines)
        if self.scroll_offset < max_scroll:
            self.scroll_offset += 1
            self.auto_scroll = False  # Disable auto-scroll when manually scrolling
    
    def wrap_text(self, text, max_chars_per_line):
        """
        Wrap text into multiple lines
        
        Args:
            text (str): Text to wrap
            max_chars_per_line (int): Maximum characters per line
            
        Returns:
            list: List of text lines
        """
        if not text:
            return []
        
        lines = []
        for i in range(0, len(text), max_chars_per_line):
            line = text[i:i + max_chars_per_line]
            lines.append(line)
        
        return lines
    
    def draw_dialogue_box(self, screen):
        """
        Draw the dialogue interface on screen
        
        Args:
            screen: Pygame surface to draw on
        """
        if not self.active:
            return
        
        # Draw semi-transparent dialogue box
        dialogue_surface = pygame.Surface((SCREEN_WIDTH - 40, 260), pygame.SRCALPHA)
        dialogue_surface.fill((200, 200, 200, 225))  # RGBA: 200 alpha = 78% opacity
        screen.blit(dialogue_surface, (20, SCREEN_HEIGHT - 280))
        
        # Draw border
        dialogue_rect = pygame.Rect(20, SCREEN_HEIGHT - 280, SCREEN_WIDTH - 40, 260)
        pygame.draw.rect(screen, BLACK, dialogue_rect, 2)

        # Draw NPC name
        if self.current_npc:
            name_text = f"{self.current_npc.name}:"
            try:
                name_surface = self.font.render(name_text, True, (0, 0, 139))  # Dark blue
                screen.blit(name_surface, (40, SCREEN_HEIGHT - 270))
            except Exception as e:
                print(f"Error rendering NPC name: {e}")
        
        # Draw model info
        model_text = f"Model: {OLLAMA_MODEL}"
        try:
            model_surface = self.tiny_font.render(model_text, True, GRAY)
            screen.blit(model_surface, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 270))
        except:
            pass
        
        # Draw status indicator
        if self.is_thinking and not self.think_removed:
            try:
                status_surface = self.tiny_font.render("Generating...", True, RED)
                screen.blit(status_surface, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 250))
            except:
                pass
        else:
            try:
                status_surface = self.tiny_font.render("Use ↑↓ to scroll", True, GRAY)
                screen.blit(status_surface, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 250))
            except:
                pass
        
        # Determine which text to display
        display_text = self.thinking_process if self.show_thinking_process else self.npc_response
        
        # Wrap text into lines
        lines = self.wrap_text(display_text, 78)
        
        # Calculate visible range
        start_line = self.scroll_offset
        end_line = min(start_line + self.max_visible_lines, len(lines))
        
        # Draw visible lines
        for i, line in enumerate(lines[start_line:end_line]):
            y_pos = SCREEN_HEIGHT - 240 + i * self.text_height
            if y_pos < SCREEN_HEIGHT - 60 and y_pos >= SCREEN_HEIGHT - 240:
                try:
                    text_surface = self.small_font.render(line, True, BLACK)
                    if text_surface.get_width() < SCREEN_WIDTH - 80:
                        screen.blit(text_surface, (40, y_pos))
                    else:
                        # Fallback for very wide text
                        short_line = line[:len(line)//2]
                        text_surface = self.small_font.render(short_line, True, BLACK)
                        screen.blit(text_surface, (40, y_pos))
                except Exception as e:
                    print(f"Error rendering text: {e}")
                    try:
                        # ASCII-only fallback
                        safe_line = "".join(c for c in line if ord(c) < 128)
                        text_surface = self.small_font.render(safe_line, True, BLACK)
                        screen.blit(text_surface, (40, y_pos))
                    except:
                        pass
        
        # Draw input box
        input_y = SCREEN_HEIGHT - 60
        pygame.draw.rect(screen, WHITE, (40, input_y, SCREEN_WIDTH - 80, 30))
        pygame.draw.rect(screen, BLACK, (40, input_y, SCREEN_WIDTH - 80, 30), 1)
        
        # Draw input text with cursor
        input_text = self.player_input
        if self.input_active and self.show_cursor:
            input_text += "|"
        
        # Ensure text fits in input box
        max_width = SCREEN_WIDTH - 100
        while True:
            try:
                input_surface = self.small_font.render(input_text, True, BLACK)
                if input_surface.get_width() <= max_width or len(input_text) <= 1:
                    break
                input_text = input_text[:-1]
            except:
                break
        
        try:
            screen.blit(input_surface, (45, input_y + 5))
        except:
            pass
        
        # Draw input instructions
        if self.is_thinking and not self.think_removed:
            status_text = "Generating..."
        else:
            status_text = "Type message and press Enter to send, ESC to exit"
        try:
            hint_surface = self.tiny_font.render(status_text, True, (100, 100, 100))
            screen.blit(hint_surface, (40, SCREEN_HEIGHT - 80))
        except:
            pass