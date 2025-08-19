import pygame
from Setting.Configuration import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_BLUE, YELLOW


class Player:
    """Player class"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 60
        self.speed = 5
        self.direction = "down"

        # Initialize animation-related attributes
        self.anim_frame = 0
        self.anim_timer = 0
        self.character_images = {}
        self.load_character_images()
        
        # Add idle state detection
        self.last_direction = "down"
        self.is_moving = False

    def load_character_images(self):
        """Load character sprites"""
        try:
            self.character_images = {
                # Walking animation (left/right)
                'walk_a': pygame.image.load("assets/img/character_purple_walk_a.png").convert_alpha(),
                'walk_b': pygame.image.load("assets/img/character_purple_walk_b.png").convert_alpha(),
                # Climbing animation (up)
                'climb_a': pygame.image.load("assets/img/character_purple_climb_a.png").convert_alpha(),
                'climb_b': pygame.image.load("assets/img/character_purple_climb_b.png").convert_alpha(),
                # Downward animations
                'duck': pygame.image.load("assets/img/character_purple_duck.png").convert_alpha(),
                'jump': pygame.image.load("assets/img/character_purple_jump.png").convert_alpha(),
                # Idle state
                'front': pygame.image.load("assets/img/character_purple_front.png").convert_alpha()
            }
            
            # Resize all sprites to match player dimensions
            for key in self.character_images:
                self.character_images[key] = pygame.transform.scale(
                    self.character_images[key], (self.width, self.height))
        except Exception as e:
            print(f"Failed to load character sprites: {e}")
            self.character_images = {}

    def move(self, dx, dy, obstacles=None):
        """Move the player, with collision and boundary checking"""
        # Detect if the player is moving
        self.is_moving = (dx != 0 or dy != 0)
        
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Create a new rectangle for collision detection
        new_rect = pygame.Rect(new_x, new_y, self.width, self.height)
        
        # Check for collisions with obstacles
        can_move = True
        if obstacles:
            for obstacle in obstacles:
                if new_rect.colliderect(obstacle):
                    can_move = False
                    break
        
        # Room boundaries (with margin from walls)
        room_margin = 50
        in_bounds = (room_margin <= new_x <= SCREEN_WIDTH - self.width - room_margin and 
                    room_margin <= new_y <= SCREEN_HEIGHT - self.height - room_margin)
        
        # Move only if within bounds and no collision
        if can_move and in_bounds:
            self.x = new_x
            self.y = new_y
            
            if dx > 0:
                self.direction = "right"
                self.last_direction = "right"
            elif dx < 0:
                self.direction = "left"
                self.last_direction = "left"
            elif dy > 0:
                self.direction = "down"
                self.last_direction = "down"
            elif dy < 0:
                self.direction = "up"
                self.last_direction = "up"
        elif not in_bounds:
            # Boundary collision handling (optional: sliding effect)
            if room_margin <= new_x <= SCREEN_WIDTH - self.width - room_margin:
                self.x = new_x
            if room_margin <= new_y <= SCREEN_HEIGHT - self.height - room_margin:
                self.y = new_y
                
            # Update direction
            if dx > 0:
                self.direction = "right"
                self.last_direction = "right"
            elif dx < 0:
                self.direction = "left"
                self.last_direction = "left"
            elif dy > 0:
                self.direction = "down"
                self.last_direction = "down"
            elif dy < 0:
                self.direction = "up"
                self.last_direction = "up"

    def get_rect(self):
        """Get the player's collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        """Draw the player on the screen"""
        # Use sprites if loaded, otherwise fall back to basic drawing
        if hasattr(self, 'character_images') and self.character_images:
            # Update animation frame (only when moving)
            if self.is_moving:
                self.anim_timer += 1
                if self.anim_timer >= 10:  # Change frame every 10 ticks
                    self.anim_frame = (self.anim_frame + 1) % 2
                    self.anim_timer = 0
            
            # Select sprite based on movement state and direction
            if not self.is_moving:
                # Idle state: use last direction
                if self.last_direction == "up":
                    screen.blit(self.character_images['climb_a'], (self.x, self.y))
                else:
                    screen.blit(self.character_images['front'], (self.x, self.y))
            elif self.direction == "right":
                # Walking animation (right)
                if self.anim_frame == 0:
                    screen.blit(self.character_images['walk_a'], (self.x, self.y))
                else:
                    screen.blit(self.character_images['walk_b'], (self.x, self.y))
            elif self.direction == "left":
                # Flip walking animation for left movement
                if self.anim_frame == 0:
                    flipped_image = pygame.transform.flip(self.character_images['walk_a'], True, False)
                    screen.blit(flipped_image, (self.x, self.y))
                else:
                    flipped_image = pygame.transform.flip(self.character_images['walk_b'], True, False)
                    screen.blit(flipped_image, (self.x, self.y))
            elif self.direction == "up":
                # Climbing animation
                if self.anim_frame == 0:
                    screen.blit(self.character_images['climb_a'], (self.x, self.y))
                else:
                    screen.blit(self.character_images['climb_b'], (self.x, self.y))
            elif self.direction == "down":
                # Downward animation (alternating duck and jump)
                if self.anim_frame == 0:
                    screen.blit(self.character_images['duck'], (self.x, self.y))
                else:
                    screen.blit(self.character_images['jump'], (self.x, self.y))
        else:
            # Fallback: draw a simple rectangle with directional face
            pygame.draw.rect(screen, PLAYER_BLUE, (self.x, self.y, self.width, self.height))
            face_x, face_y = self.x + self.width // 2, self.y + self.height // 2
            if self.direction == "up":
                pygame.draw.circle(screen, YELLOW, (face_x, self.y + 5), 3)
            elif self.direction == "down":
                pygame.draw.circle(screen, YELLOW, (face_x, self.y + self.height - 5), 3)
            elif self.direction == "left":
                pygame.draw.circle(screen, YELLOW, (self.x + 5, face_y), 3)
            elif self.direction == "right":
                pygame.draw.circle(screen, YELLOW, (self.x + self.width - 5, face_y), 3)