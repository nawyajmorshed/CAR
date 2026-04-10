"""
Main game loop and entry point for the 3D Racing Game
Supports 2-Player Local Co-op or Single Player vs AI
"""
import pygame
from pygame.locals import *
import OpenGL.GL as gl
from OpenGL.GL import *
from OpenGL.GLU import gluLookAt, gluPerspective
import numpy as np
import sys
import time
import os
import math

# Add project directories to path for module imports
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, 'src'))
sys.path.insert(0, project_root)

import config
from graphics import SimpleRenderer, Camera
from game import Car, World
from debug import PerformanceMonitor, DebugRenderer


def show_start_menu_gui():
    """Display graphical start menu using pygame"""
    pygame.init()
    
    # Create menu window
    menu_display = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    pygame.display.set_caption(config.WINDOW_TITLE)
    
    # Menu state
    selected = 0  # 0 = 2-Player, 1 = Single Player
    menu_active = True
    
    # Create font
    title_font = pygame.font.Font(None, 72)
    option_font = pygame.font.Font(None, 48)
    desc_font = pygame.font.Font(None, 32)
    
    clock = pygame.time.Clock()
    
    while menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    selected = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    selected = 1
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    pygame.quit()
                    return 'multiplayer' if selected == 0 else 'singleplayer'
        
        # Clear screen (dark blue background)
        menu_display.fill((20, 40, 80))
        
        # Draw title
        title = title_font.render("🏎️  3D RACING GAME  🏎️", True, (255, 215, 0))
        title_rect = title.get_rect(center=(config.WINDOW_WIDTH // 2, 80))
        menu_display.blit(title, title_rect)
        
        # Draw divider line
        pygame.draw.line(menu_display, (100, 200, 255), (100, 160), (config.WINDOW_WIDTH - 100, 160), 2)
        
        # Left option - 2-Player
        left_color = (255, 255, 0) if selected == 0 else (150, 150, 150)
        left_box_color = (100, 100, 200) if selected == 0 else (50, 50, 100)
        
        left_box = pygame.Rect(50, 250, config.WINDOW_WIDTH // 2 - 100, 300)
        pygame.draw.rect(menu_display, left_box_color, left_box, 3)
        pygame.draw.rect(menu_display, (20, 40, 80), left_box)
        
        left_title = option_font.render("🏁 2-PLAYER RACE", True, left_color)
        left_desc1 = desc_font.render("Play with Friend", True, left_color)
        left_desc2 = desc_font.render("Player 1: W/A/S/D + Shift", True, (200, 200, 200))
        left_desc3 = desc_font.render("Player 2: Arrows + Shift", True, (200, 200, 200))
        
        menu_display.blit(left_title, (80, 270))
        menu_display.blit(left_desc1, (90, 320))
        menu_display.blit(left_desc2, (85, 370))
        menu_display.blit(left_desc3, (85, 410))
        
        # Right option - Single Player
        right_color = (255, 255, 0) if selected == 1 else (150, 150, 150)
        right_box_color = (100, 100, 200) if selected == 1 else (50, 50, 100)
        
        right_box = pygame.Rect(config.WINDOW_WIDTH // 2 + 50, 250, config.WINDOW_WIDTH // 2 - 100, 300)
        pygame.draw.rect(menu_display, right_box_color, right_box, 3)
        pygame.draw.rect(menu_display, (20, 40, 80), right_box)
        
        right_title = option_font.render("🤖 SINGLE PLAYER", True, right_color)
        right_desc1 = desc_font.render("vs AI Opponents", True, right_color)
        right_desc2 = desc_font.render("Control: W/A/S/D + Shift", True, (200, 200, 200))
        right_desc3 = desc_font.render("Beat 3 AI racers to win", True, (200, 200, 200))
        
        menu_display.blit(right_title, (config.WINDOW_WIDTH // 2 + 70, 270))
        menu_display.blit(right_desc1, (config.WINDOW_WIDTH // 2 + 85, 320))
        menu_display.blit(right_desc2, (config.WINDOW_WIDTH // 2 + 60, 370))
        menu_display.blit(right_desc3, (config.WINDOW_WIDTH // 2 + 75, 410))
        
        # Draw instructions at bottom
        instruction = desc_font.render("← Use Arrow Keys to Select | Press ENTER to Start →", True, (100, 200, 255))
        instruction_rect = instruction.get_rect(center=(config.WINDOW_WIDTH // 2, 620))
        menu_display.blit(instruction, instruction_rect)
        
        pygame.display.flip()
        clock.tick(60)


def show_race_results(finish_positions, is_multiplayer=False):
    """Display race results as a visual page"""
    results_display = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    pygame.display.set_caption("RACE RESULTS - " + config.WINDOW_TITLE)
    
    # Create fonts
    title_font = pygame.font.Font(None, 80)
    position_font = pygame.font.Font(None, 64)
    name_font = pygame.font.Font(None, 48)
    
    clock = pygame.time.Clock()
    
    # Medal emojis and colors
    medals = {
        1: ("🥇", (255, 215, 0)),       # Gold
        2: ("🥈", (192, 192, 192)),     # Silver
        3: ("🥉", (205, 127, 50)),      # Bronze
    }
    
    waiting_for_close = True
    while waiting_for_close:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                waiting_for_close = False
        
        # Clear screen with dark blue background
        results_display.fill((20, 40, 80))
        
        # Draw title
        title = title_font.render("🏁 RACE FINISHED 🏁", True, (255, 215, 0))
        title_rect = title.get_rect(center=(config.WINDOW_WIDTH // 2, 60))
        results_display.blit(title, title_rect)
        
        # Draw divider
        pygame.draw.line(results_display, (100, 200, 255), (50, 140), (config.WINDOW_WIDTH - 50, 140), 3)
        
        # Draw top 3 results
        y_pos = 200
        for name, position in finish_positions[:3]:
            if position <= 3:
                medal_emoji, medal_color = medals[position]
                suffix = ['st', 'nd', 'rd'][position-1]
                
                # Position text
                pos_text = position_font.render(f"{position}{suffix} Place", True, medal_color)
                results_display.blit(pos_text, (100, y_pos))
                
                # Medal
                medal_text = name_font.render(medal_emoji, True, medal_color)
                results_display.blit(medal_text, (400, y_pos + 5))
                
                # Driver name
                name_text = name_font.render(name, True, (255, 255, 255))
                results_display.blit(name_text, (480, y_pos + 5))
                
                y_pos += 120
        
        # Draw exit instruction
        exit_font = pygame.font.Font(None, 36)
        exit_text = exit_font.render("Press ESC to Exit", True, (100, 200, 255))
        exit_rect = exit_text.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT - 50))
        results_display.blit(exit_text, exit_rect)
        
        pygame.display.flip()
        clock.tick(60)


def show_start_menu():
    """Display start menu and get game mode selection"""
    return show_start_menu_gui()


class Game:
    """Main game class"""
    
    def __init__(self, game_mode='singleplayer'):
        # Initialize Pygame
        pygame.init()
        
        # Set OpenGL attributes BEFORE creating window
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_COMPATIBILITY)
        
        pygame.display.set_mode(
            (config.WINDOW_WIDTH, config.WINDOW_HEIGHT),
            DOUBLEBUF | OPENGL
        )
        pygame.display.set_caption(config.WINDOW_TITLE)
        
        # Request focus for the window
        pygame.event.clear()
        
        # Small delay to ensure window is ready
        time.sleep(0.5)
        
        # Setup OpenGL context
        try:
            gl.glEnable(gl.GL_MULTISAMPLE)
        except Exception as e:
            print(f"Warning: Could not enable multisample: {e}")
        
        # Game mode (multiplayer or singleplayer)
        self.game_mode = game_mode
        self.is_multiplayer = (game_mode == 'multiplayer')
        
        # Create game objects
        self.renderer = SimpleRenderer(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        self.world = World()
        
        # Player 1 (HUMAN) - Red car
        self.car = Car('sports', start_pos=(0, 1, 100))
        self.car.color = [1.0, 0.0, 0.0]  # Red
        self.camera = Camera(self.car)
        
        # Player 2 (HUMAN in multiplayer or None in singleplayer) - Green car
        self.car2 = None
        self.camera2 = None
        
        if self.is_multiplayer:
            # Create second player car (green)
            self.car2 = Car('sports', start_pos=(10, 1, 100))  # Different lane from car1
            self.car2.color = [0.0, 1.0, 0.0]  # Green
            self.camera2 = Camera(self.car2)
        
        # Game state
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = config.TARGET_DELTA
        self.frame_count = 0
        self.fps_timer = time.time()
        self.current_fps = 0
        self.performance_monitor = PerformanceMonitor()
        
        # Race countdown timer (2 seconds)
        self.countdown_timer = 2.0
        self.race_started = False
        
        # Race finish tracking
        self.finish_positions = []  # List of cars that finished
        self.finish_line_z = 5900  # Finish line position
        self.race_ended = False  # Track if race is complete
        self.race_end_timer = 0  # Timer for race ending delay
        
        # Input state for Player 1
        self.key_map_p1 = {
            K_w: 'w',
            K_a: 'a',
            K_s: 's',
            K_d: 'd',
            K_LSHIFT: 'shift',
        }
        
        # Input state for Player 2 (arrow keys + right shift)
        self.key_map_p2 = {
            K_UP: 'w',
            K_DOWN: 's',
            K_LEFT: 'a',
            K_RIGHT: 'd',
            K_RSHIFT: 'shift',
        }
        
        print(f"Game initialized successfully!")
        print(f"OpenGL Version: {gl.glGetString(gl.GL_VERSION)}")
        print(f"GLSL Version: {gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION)}")
        print(f"Game Mode: {'🎮 MULTIPLAYER (2-Player)' if self.is_multiplayer else '🤖 SINGLEPLAYER (vs AI)'}")
    
    def handle_input(self):
        """Handle user input for both players - FIXED KEY MAPPING"""
        # Pump events to ensure they're processed
        pygame.event.pump()
        
        # Use pygame.key.get_pressed() for continuous key state checking
        keys = pygame.key.get_pressed()
        
        # Process events (for window close and escape key)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
        
        # Handle Player 1 input (W/A/S/D + Left Shift)
        # Use proper pygame key constants
        self.car.set_input('w', keys[pygame.K_w])  # W = forward
        self.car.set_input('s', keys[pygame.K_s])  # S = backward
        self.car.set_input('a', keys[pygame.K_a])  # A = left
        self.car.set_input('d', keys[pygame.K_d])  # D = right
        self.car.set_input('shift', keys[pygame.K_LSHIFT])  # Shift = nitro
        
        # Handle Player 2 input if in multiplayer mode (Arrow Keys + Right Shift)
        if self.is_multiplayer and self.car2:
            self.car2.set_input('w', keys[pygame.K_UP])      # UP = forward
            self.car2.set_input('s', keys[pygame.K_DOWN])    # DOWN = backward
            self.car2.set_input('a', keys[pygame.K_LEFT])    # LEFT = turn left
            self.car2.set_input('d', keys[pygame.K_RIGHT])   # RIGHT = turn right
            self.car2.set_input('shift', keys[pygame.K_RSHIFT])  # Right Shift = nitro
    
    def update(self, dt):
        """Update game state for both players"""
        # Update countdown timer
        if not self.race_started:
            self.countdown_timer -= dt
            if self.countdown_timer <= 0:
                self.race_started = True
                print("🏁 RACE STARTED!")
                self.countdown_timer = 0
            else:
                # Display countdown every 1 second
                remaining_int = int(self.countdown_timer) + 1
                if remaining_int > 0:
                    print(f"⏱️  Race starts in: {remaining_int}...", end='\r')
        
        # Update Player 1 car
        self.car.update(dt, self.world.get_terrain_at_position, self.world.environment_objects, 
                       allow_movement=self.race_started)
        
        # Display boost status if active
        if self.car.boost_active:
            print(f"🚀 BOOST: {self.car.boost_multiplier}x | {self.car.boost_timer:.1f}s remaining", end='\r')
        
        # Update Player 2 car if in multiplayer mode
        if self.is_multiplayer and self.car2:
            self.car2.update(dt, self.world.get_terrain_at_position, self.world.environment_objects, 
                           allow_movement=self.race_started)
        
        # Update AI cars (only if in singleplayer mode)
        if not self.is_multiplayer:
            for ai_car in self.world.ai_cars:
                ai_car.update(dt, self.world.environment_objects, allow_movement=self.race_started)
        
        # Update world
        # For multiplayer, center between both cars so they see same road
        if self.is_multiplayer and self.car2:
            center_pos = (self.car.position + self.car2.position) / 2
        else:
            center_pos = self.car.position
        self.world.update(center_pos)
        
        # Update cameras
        self.camera.update(dt, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        if self.car2 and self.camera2:
            self.camera2.update(dt, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        
        # Check for finish line crossing
        self.check_finish_line()
        
        # Check if race should end
        if self.finish_positions and not self.race_ended:
            # First car crossed finish line - start the timer
            self.race_end_timer += dt
            
            # Determine end conditions
            should_end_race = False
            
            if self.is_multiplayer:
                # Multiplayer: Race ends when both players finish or 5 seconds elapsed (whichever is sooner)
                if self.car.has_finished and self.car2.has_finished:
                    should_end_race = True
                elif self.race_end_timer > 5.0:
                    should_end_race = True
            else:
                # Singleplayer: Race ends when player finishes and 3 seconds elapsed
                # OR when player + all AI cars have finished
                if self.race_end_timer > 3.0:
                    should_end_race = True
                else:
                    # Check if player + all AI cars finished
                    if self.car.has_finished:
                        all_ai_finished = all(ai_car.has_finished for ai_car in self.world.ai_cars)
                        if all_ai_finished:
                            should_end_race = True
            
            if should_end_race:
                self.race_ended = True
                self.running = False  # Exit the main game loop
        
        # Display race positions
        if self.race_started:
            self.display_race_positions()
    
    def render(self):
        """Render the scene - split-screen for 2-player mode"""
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        
        if self.is_multiplayer:
            self.render_split_screen()
        else:
            gl.glViewport(0, 0, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
            self.render_singleplayer()
        
        pygame.display.flip()
    
    def render_split_screen(self):
        """Render split-screen view for 2 players - TOP and BOTTOM"""
        # Calculate shared parameters
        viewport_height = config.WINDOW_HEIGHT // 2
        aspect_ratio = config.WINDOW_WIDTH / viewport_height
        
        # Top side: Player 1 (Red) - camera follows RED car
        self.render_split_view(
            self.car,
            0,  # x_offset
            config.WINDOW_HEIGHT // 2,  # y_offset (top half)
            aspect_ratio,
            "🔴 PLAYER 1 (RED)"
        )
        
        # Bottom side: Player 2 (Green) - camera follows GREEN car
        if self.car2:
            self.render_split_view(
                self.car2,
                0,  # x_offset
                0,  # y_offset (bottom half)
                aspect_ratio,
                "🟢 PLAYER 2 (GREEN)"
            )
    
    def render_split_view(self, car, x_offset, y_offset, aspect_ratio, player_name):
        """Render one half of the split screen (top or bottom)"""
        viewport_width = config.WINDOW_WIDTH
        viewport_height = config.WINDOW_HEIGHT // 2
        
        # ============ SET VIEWPORT AND SCISSOR ============
        gl.glViewport(x_offset, y_offset, viewport_width, viewport_height)
        gl.glScissor(x_offset, y_offset, viewport_width, viewport_height)
        gl.glEnable(gl.GL_SCISSOR_TEST)
        
        # Clear depth buffer for this viewport only
        gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
        
        # ============ PROJECTION MATRIX ============
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        
        # Use passed aspect ratio (ensures both viewports are identical)
        gluPerspective(60.0, aspect_ratio, 0.1, 5000.0)
        
        # ============ MODEL-VIEW MATRIX ============
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        
        # Camera follows THIS player's car (not center between both)
        car_x = car.position[0]
        car_y = car.position[1]
        car_z = car.position[2]
        car_yaw = car.rotation[1]
        
        # Camera positioned behind and above car, rotated with car direction
        camera_distance = 12.0
        camera_height = 3.5
        
        camera_x = car_x - np.sin(car_yaw) * camera_distance
        camera_z = car_z - np.cos(car_yaw) * camera_distance
        camera_y = car_y + camera_height
        
        # Look ahead down the road
        lookahead_distance = 20.0
        lookat_x = car_x + np.sin(car_yaw) * lookahead_distance
        lookat_z = car_z + np.cos(car_yaw) * lookahead_distance
        lookat_y = car_y + 0.5
        
        gluLookAt(
            camera_x, camera_y, camera_z,
            lookat_x, lookat_y, lookat_z,
            0, 1, 0
        )
        
        # ============ RENDER WORLD ============
        self.renderer.render_ground(self.world.environment_objects)
        self.renderer.render_roads(self.world.road_segments)
        self.renderer.render_barriers(self.world.environment_objects)
        
        # ALWAYS render both cars so each player sees both (2-player mode - no AI)
        self.renderer.render_car(self.car)    # RED car
        if self.car2:
            self.renderer.render_car(self.car2)  # GREEN car
        
        # Disable scissor after rendering this viewport
        gl.glDisable(gl.GL_SCISSOR_TEST)
    
    def draw_center_divider(self):
        """Not used - kept for compatibility"""
        pass
    
    def render_singleplayer(self):
        """Render single player view with AI standings"""
        # Prepare race standings data for AI with bounds checking
        race_standings = {
            'player_pos': 1,
            'player_distance': self.car.position[2],
            'player_finished': self.car.has_finished,
        }
        
        # Safely add AI car data with bounds checking
        ai_names = ['ai1', 'ai2', 'ai3', 'ai4', 'ai5', 'ai6']
        for i, ai_name in enumerate(ai_names):
            if i < len(self.world.ai_cars):
                race_standings[f'{ai_name}_pos'] = i + 2
                race_standings[f'{ai_name}_distance'] = self.world.ai_cars[i].position[2]
                race_standings[f'{ai_name}_finished'] = self.world.ai_cars[i].has_finished
            else:
                race_standings[f'{ai_name}_pos'] = i + 2
                race_standings[f'{ai_name}_distance'] = 0
                race_standings[f'{ai_name}_finished'] = False
        
        self.renderer.render_scene(
            self.world,
            self.car,
            self.camera,
            config.WINDOW_WIDTH,
            config.WINDOW_HEIGHT,
            race_standings=race_standings
        )
    
    def run(self):
        """Main game loop"""
        print("Starting game loop...")
        print(f"Target FPS: {config.FPS}")
        print(f"Chunk Size: {config.CHUNK_SIZE}")
        print(f"Render Distance: {config.RENDER_DISTANCE}")
        print()
        
        while self.running:
            # Calculate delta time
            self.dt = self.clock.tick(config.FPS) / 1000.0
            self.dt = min(self.dt, 0.05)  # Cap delta time
            self.performance_monitor.record_frame_time(self.dt)
            
            # Update FPS counter
            self.frame_count += 1
            if time.time() - self.fps_timer > 1.0:
                self.current_fps = self.frame_count
                self.frame_count = 0
                self.fps_timer = time.time()
                print(f"FPS: {self.current_fps} | "
                      f"Car: ({self.car.position[0]:.1f}, {self.car.position[1]:.1f}, {self.car.position[2]:.1f}) | "
                      f"Speed: {self.car.velocity:.1f} | "
                      f"Yaw: {math.degrees(self.car.rotation[1]):.1f}° | "
                      f"Cam: ({self.camera.position[0]:.1f}, {self.camera.position[1]:.1f}, {self.camera.position[2]:.1f})")
            
            # Handle input
            self.handle_input()
            
            # Update
            self.update(self.dt)
            
            # Render
            self.render()
        
        # Show race results if anyone finished
        if self.finish_positions:
            show_race_results(self.finish_positions, self.is_multiplayer)
        
        self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        print("Cleaning up...")
        self.renderer.cleanup()
        pygame.quit()
        sys.exit()
    
    def display_race_positions(self):
        """Display current race positions"""
        if self.is_multiplayer:
            # Multiplayer: Show both players
            if int(self.fps_timer * 2) % 2 == 0:
                print("\n" + "="*60)
                print("🏁 2-PLAYER RACE - STANDINGS 🏁")
                print("="*60)
                if self.car.position[2] > self.car2.position[2]:
                    print(f"1st. 🔴 Player 1 (RED)  | Distance: {self.car.position[2]:.0f}m | Speed: {self.car.velocity:.1f}")
                    print(f"2nd. 🟢 Player 2 (GREEN) | Distance: {self.car2.position[2]:.0f}m | Speed: {self.car2.velocity:.1f}")
                else:
                    print(f"1st. 🟢 Player 2 (GREEN) | Distance: {self.car2.position[2]:.0f}m | Speed: {self.car2.velocity:.1f}")
                    print(f"2nd. 🔴 Player 1 (RED)  | Distance: {self.car.position[2]:.0f}m | Speed: {self.car.velocity:.1f}")
                print("="*60 + "\n")
        else:
            # Singleplayer: Show all cars
            # Collect all cars with their positions
            cars_data = [
                {'name': 'YOU', 'z': self.car.position[2], 'speed': self.car.velocity, 'color': '🔴'},
            ]
            ai_names = ['AI-1 (Blue)', 'AI-2 (Yellow)', 'AI-3 (Magenta)', 'AI-4 (Cyan)', 'AI-5 (Orange)', 'AI-6 (Purple)']
            ai_colors = ['🔵', '🟡', '🟣', '🟦', '🟠', '🟪']
            for i in range(min(len(self.world.ai_cars), 6)):
                cars_data.append({
                    'name': ai_names[i],
                    'z': self.world.ai_cars[i].position[2],
                    'speed': self.world.ai_cars[i].velocity,
                    'color': ai_colors[i]
                })
            
            # Sort by z position (highest z = furthest ahead = 1st place)
            cars_data.sort(key=lambda x: x['z'], reverse=True)
            
            # Print race standings every 2 seconds
            if int(self.fps_timer * 2) % 2 == 0:
                print("\n" + "="*60)
                print("🏁 RACE STANDINGS 🏁")
                print("="*60)
                for idx, car in enumerate(cars_data, 1):
                    print(f"{idx}. {car['color']} {car['name']:<20} | Distance: {car['z']:.0f}m | Speed: {car['speed']:.1f}")
                print("="*60 + "\n")
    
    def check_finish_line(self):
        """Check if any car has crossed the finish line"""
        if self.is_multiplayer:
            # 2-Player multiplayer mode
            # Check Player 1
            if self.car.position[2] > self.finish_line_z and not self.car.has_finished:
                self.car.has_finished = True
                finish_position = len(self.finish_positions) + 1
                self.finish_positions.append(('🔴 Player 1 (RED)', finish_position))
                print("\n" + "🏆" * 20)
                print(f"🏆 FINISHED! 🔴 Player 1 got position: #{finish_position} 🏆")
                print("🏆" * 20 + "\n")
            
            # Check Player 2
            if self.car2 and self.car2.position[2] > self.finish_line_z and not self.car2.has_finished:
                self.car2.has_finished = True
                finish_position = len(self.finish_positions) + 1
                self.finish_positions.append(('🟢 Player 2 (GREEN)', finish_position))
                print("\n" + "🏆" * 20)
                print(f"🏆 FINISHED! 🟢 Player 2 got position: #{finish_position} 🏆")
                print("🏆" * 20 + "\n")
        else:
            # Single player vs AI mode
            # Check player car
            if self.car.position[2] > self.finish_line_z and not self.car.has_finished:
                self.car.has_finished = True
                finish_position = len(self.finish_positions) + 1
                self.finish_positions.append(('YOU 🔴', finish_position))
                print("\n" + "🏆" * 20)
                print(f"🏆 FINISHED! YOU got position: #{finish_position} 🏆")
                print("🏆" * 20 + "\n")
            
            # Check AI cars
            for ai_car in self.world.ai_cars:
                if ai_car.position[2] > self.finish_line_z and not ai_car.has_finished:
                    ai_car.has_finished = True
                    finish_position = len(self.finish_positions) + 1
                    
                    ai_names = [
                        'AI-1 (Blue) 🔵',
                        'AI-2 (Yellow) 🟡',
                        'AI-3 (Magenta) 🟣',
                        'AI-4 (Cyan) 🟦',
                        'AI-5 (Orange) 🟠',
                        'AI-6 (Purple) 🟪',
                    ]
                    
                    ai_name = ai_names[ai_car.ai_id] if ai_car.ai_id < len(ai_names) else f'AI-{ai_car.ai_id}'
                    self.finish_positions.append((ai_name, finish_position))
                    
                    print("\n" + "🏆" * 20)
                    print(f"🏆 FINISHED! {ai_name} got position: #{finish_position} 🏆")
                    print("🏆" * 20 + "\n")


def main():
    """Entry point - show menu and start game"""
    try:
        # Show start menu and get game mode
        game_mode = show_start_menu()
        
        # Create and run game with selected mode
        game = Game(game_mode=game_mode)
        game.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)


if __name__ == '__main__':
    main()
