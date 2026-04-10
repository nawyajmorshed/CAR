"""
Optimized renderer using display lists for performance
"""
import OpenGL.GL as gl
from OpenGL.GL import *
from OpenGL.GLU import gluLookAt
import numpy as np
import math
import config


class SimpleRenderer:
    """Optimized renderer using display lists for caching geometry"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.setup_opengl()
        
        # Create display lists for caching (MAJOR PERFORMANCE BOOST)
        self.cube_list = None
        self.sphere_list = None
        self.cylinder_list = None
        self.create_display_lists()
        print("✓ Optimized renderer initialized with cached geometry")
    
    def setup_opengl(self):
        """Setup basic OpenGL"""
        gl.glClearColor(*config.SKY_COLOR)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_LIGHT0)
        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glColorMaterial(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT_AND_DIFFUSE)
        
        # Setup light
        gl.glLight(gl.GL_LIGHT0, gl.GL_POSITION, (1, 1, 1, 0))
        gl.glLight(gl.GL_LIGHT0, gl.GL_AMBIENT, (0.4, 0.4, 0.4, 1))
        gl.glLight(gl.GL_LIGHT0, gl.GL_DIFFUSE, (0.8, 0.8, 0.8, 1))
    
    def clear(self):
        """Clear screen"""
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    
    def setup_matrices(self, view_matrix, proj_matrix, width, height):
        """Setup projection and view matrices"""
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        
        # Simple perspective
        aspect = width / height
        fov = 45.0
        near = 0.1
        far = 5000.0
        
        f = 1.0 / math.tan(math.radians(fov) / 2.0)
        gl.glFrustum(-near * aspect, near * aspect, -near, near, near, far)
        
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        
        # Apply camera view matrix using gluLookAt
        # Use simple third-person view - camera positioned behind and above the scene
        gluLookAt(
            0, 5, 30,      # Camera position (behind and above)
            0, 1, 0,       # Look at point
            0, 1, 0        # Up vector
        )
    
    def setup_matrices_with_camera(self, camera, width, height, car=None):
        """Setup projection and view matrices with actual camera"""
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        
        # Projection matrix
        aspect = width / height
        near = 0.1
        far = 5000.0
        
        # Base FOV is 60, but expand when using nitro (add FOV_BOOST)
        fov = 60.0
        if car:
            fov_boost = car.get_fov_boost()
            fov = min(90.0, fov + fov_boost)  # Cap at 90 degrees max
        
        f = 1.0 / math.tan(math.radians(fov) / 2.0)
        gl.glFrustum(-near * aspect, near * aspect, -near, near, near, far)
        
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        
        # Simple but effective camera: follow behind and above the car
        # This is the key - position camera properly relative to car
        car_x = camera.target_car.position[0]
        car_y = camera.target_car.position[1]
        car_z = camera.target_car.position[2]
        car_yaw = camera.target_car.rotation[1]
        
        # Position camera 15 units behind car and 4 units above
        cam_distance = 15.0
        cam_height = 4.0
        
        cam_x = car_x - math.sin(car_yaw) * cam_distance
        cam_z = car_z - math.cos(car_yaw) * cam_distance
        cam_y = car_y + cam_height
        
        # Look point slightly ahead of car
        look_ahead = 5.0
        look_x = car_x + math.sin(car_yaw) * look_ahead
        look_z = car_z + math.cos(car_yaw) * look_ahead
        look_y = car_y + 1.0
        
        gluLookAt(
            cam_x, cam_y, cam_z,           # Camera position
            look_x, look_y, look_z,         # Look at point
            0, 1, 0                         # Up vector
        )
    
    def draw_wheel(self, x, y, z):
        """Draw a wheel (cylinder) at position"""
        gl.glPushMatrix()
        gl.glTranslatef(x, y, z)
        gl.glRotatef(90, 0, 1, 0)  # Rotate to face correct direction
        self.draw_cylinder(0.5, 0.3, 16)  # radius, height, segments
        gl.glPopMatrix()
    
    def render_car(self, car):
        """Render car with premium sports car design - fully polished"""
        gl.glPushMatrix()
        gl.glTranslatef(car.position[0], car.position[1], car.position[2])
        
        # Rotate
        yaw_deg = math.degrees(car.rotation[1])
        pitch_deg = math.degrees(car.rotation[0])
        roll_deg = math.degrees(car.rotation[2])
        gl.glRotatef(yaw_deg, 0, 1, 0)
        gl.glRotatef(pitch_deg, 1, 0, 0)
        gl.glRotatef(roll_deg, 0, 0, 1)
        
        # Get car color
        if hasattr(car, 'color') and car.color:
            color = car.color
        else:
            color = [1.0, 0.2, 0.2]  # Default red
        
        # ===== UNDERCARRIAGE (DARK SHADOW) =====
        gl.glColor3f(0.1, 0.1, 0.1)
        gl.glPushMatrix()
        gl.glTranslatef(0, -0.5, 0)
        gl.glScalef(1.15, 0.15, 2.5)
        self.draw_cube()
        gl.glPopMatrix()
        
        # ===== MAIN CHASSIS (BODY) - SMOOTH ROUNDED =====
        gl.glColor3f(color[0], color[1], color[2])
        gl.glPushMatrix()
        gl.glTranslatef(0, -0.25, 0)
        gl.glScalef(1.1, 0.6, 2.4)
        self.draw_sphere(1.0, 20, 20)  # Smooth rounded sphere body
        gl.glPopMatrix()
        
        # ===== FRONT BUMPER (SMOOTH ROUNDED) =====
        gl.glColor3f(color[0] * 0.8, color[1] * 0.8, color[2] * 0.8)
        gl.glPushMatrix()
        gl.glTranslatef(0, -0.15, 1.5)
        gl.glScalef(1.15, 0.35, 0.3)
        self.draw_sphere(1.0, 12, 12)  # Smooth rounded bumper
        gl.glPopMatrix()
        
        # ===== FRONT GRILLE =====
        gl.glColor3f(0.2, 0.2, 0.2)
        gl.glPushMatrix()
        gl.glTranslatef(0, 0.05, 1.52)
        gl.glScalef(0.6, 0.35, 0.08)
        self.draw_cube()
        gl.glPopMatrix()
        
        # ===== HOOD (SMOOTH ROUNDED) =====
        gl.glColor3f(color[0] * 1.08, color[1] * 1.08, color[2] * 1.08)
        gl.glPushMatrix()
        gl.glTranslatef(0, 0.15, 1.2)
        gl.glScalef(0.95, 0.4, 0.8)
        self.draw_sphere(1.0, 18, 18)  # Smooth rounded hood
        gl.glPopMatrix()
        
        # ===== HOOD VENTS =====
        gl.glColor3f(0.25, 0.25, 0.25)
        gl.glPushMatrix()
        gl.glTranslatef(-0.25, 0.25, 1.0)
        gl.glScalef(0.18, 0.1, 0.25)
        self.draw_cube()
        gl.glPopMatrix()
        
        gl.glPushMatrix()
        gl.glTranslatef(0.25, 0.25, 1.0)
        gl.glScalef(0.18, 0.1, 0.25)
        self.draw_cube()
        gl.glPopMatrix()
        
        # ===== REAR CARGO AREA (SMOOTH ROUNDED) =====
        gl.glColor3f(color[0] * 0.82, color[1] * 0.82, color[2] * 0.82)
        gl.glPushMatrix()
        gl.glTranslatef(0, 0.2, -1.35)
        gl.glScalef(1.0, 0.55, 0.7)
        self.draw_sphere(1.0, 16, 16)  # Smooth rounded rear
        gl.glPopMatrix()
        
        # ===== REAR BUMPER (SMOOTH ROUNDED) =====
        gl.glColor3f(color[0] * 0.8, color[1] * 0.8, color[2] * 0.8)
        gl.glPushMatrix()
        gl.glTranslatef(0, -0.15, -1.55)
        gl.glScalef(1.15, 0.35, 0.25)
        self.draw_sphere(1.0, 12, 12)  # Smooth rounded bumper
        gl.glPopMatrix()
        
        # ===== REAR WING/SPOILER (CARBON) =====
        gl.glColor3f(0.15, 0.15, 0.15)
        gl.glPushMatrix()
        gl.glTranslatef(0, 0.65, -1.62)
        gl.glScalef(0.95, 0.55, 0.12)
        self.draw_cube()
        gl.glPopMatrix()
        
        # ===== WINDSHIELD (TINTED GLASS) =====
        gl.glColor3f(0.35, 0.55, 0.9)
        gl.glPushMatrix()
        gl.glTranslatef(0, 0.55, 0.8)
        gl.glScalef(0.82, 0.5, 0.15)
        self.draw_cube()
        gl.glPopMatrix()
        
        # ===== REAR WINDOW =====
        gl.glColor3f(0.35, 0.55, 0.9)
        gl.glPushMatrix()
        gl.glTranslatef(0, 0.5, -0.95)
        gl.glScalef(0.78, 0.45, 0.15)
        self.draw_cube()
        gl.glPopMatrix()
        
        # ===== LEFT SIDE WINDOWS (DOOR GLASS) =====
        gl.glColor3f(0.4, 0.6, 0.95)
        gl.glPushMatrix()
        gl.glTranslatef(-0.552, 0.45, 0.2)
        gl.glScalef(0.06, 0.55, 1.0)
        self.draw_cube()
        gl.glPopMatrix()
        
        # ===== RIGHT SIDE WINDOWS =====
        gl.glPushMatrix()
        gl.glTranslatef(0.552, 0.45, 0.2)
        gl.glScalef(0.06, 0.55, 1.0)
        self.draw_cube()
        gl.glPopMatrix()
        
        # ===== SIDE SKIRTS (AERODYNAMIC) =====
        gl.glColor3f(color[0] * 0.6, color[1] * 0.6, color[2] * 0.6)
        gl.glPushMatrix()
        gl.glTranslatef(-0.56, -0.2, 0)
        gl.glScalef(0.06, 0.35, 2.2)
        self.draw_cube()
        gl.glPopMatrix()
        
        gl.glPushMatrix()
        gl.glTranslatef(0.56, -0.2, 0)
        gl.glScalef(0.06, 0.35, 2.2)
        self.draw_cube()
        gl.glPopMatrix()
        
        # ===== FENDER FLARES =====
        gl.glColor3f(color[0] * 0.65, color[1] * 0.65, color[2] * 0.65)
        gl.glPushMatrix()
        gl.glTranslatef(-1.08, -0.15, 1.0)
        gl.glScalef(0.12, 0.4, 0.8)
        self.draw_cube()
        gl.glPopMatrix()
        
        gl.glPushMatrix()
        gl.glTranslatef(1.08, -0.15, 1.0)
        gl.glScalef(0.12, 0.4, 0.8)
        self.draw_cube()
        gl.glPopMatrix()
        
        # ===== LEFT MIRROR =====
        gl.glColor3f(0.25, 0.25, 0.25)
        gl.glPushMatrix()
        gl.glTranslatef(-0.63, 0.4, 0.35)
        gl.glScalef(0.18, 0.3, 0.15)
        self.draw_cube()
        gl.glPopMatrix()
        
        # ===== RIGHT MIRROR =====
        gl.glPushMatrix()
        gl.glTranslatef(0.63, 0.4, 0.35)
        gl.glScalef(0.18, 0.3, 0.15)
        self.draw_cube()
        gl.glPopMatrix()
        
        # ===== LEFT HEADLIGHT =====
        gl.glColor3f(0.95, 0.95, 0.75)
        gl.glPushMatrix()
        gl.glTranslatef(-0.3, 0.08, 1.53)
        gl.glScalef(0.2, 0.25, 0.15)
        self.draw_cube()
        gl.glPopMatrix()
        
        # ===== RIGHT HEADLIGHT =====
        gl.glPushMatrix()
        gl.glTranslatef(0.3, 0.08, 1.53)
        gl.glScalef(0.2, 0.25, 0.15)
        self.draw_cube()
        gl.glPopMatrix()
        
        # ===== LEFT TAILLIGHT (RED) =====
        gl.glColor3f(1.0, 0.15, 0.15)
        gl.glPushMatrix()
        gl.glTranslatef(-0.38, 0.1, -1.58)
        gl.glScalef(0.18, 0.25, 0.12)
        self.draw_cube()
        gl.glPopMatrix()
        
        # ===== RIGHT TAILLIGHT =====
        gl.glPushMatrix()
        gl.glTranslatef(0.38, 0.1, -1.58)
        gl.glScalef(0.18, 0.25, 0.12)
        self.draw_cube()
        gl.glPopMatrix()
        
        # ===== FRONT TURN SIGNALS (AMBER) =====
        gl.glColor3f(1.0, 0.8, 0.2)
        gl.glPushMatrix()
        gl.glTranslatef(-0.45, -0.05, 1.5)
        gl.glScalef(0.12, 0.15, 0.12)
        self.draw_cube()
        gl.glPopMatrix()
        
        gl.glPushMatrix()
        gl.glTranslatef(0.45, -0.05, 1.5)
        gl.glScalef(0.12, 0.15, 0.12)
        self.draw_cube()
        gl.glPopMatrix()
        
        # ===== REAR TURN SIGNALS (AMBER) =====
        gl.glPushMatrix()
        gl.glTranslatef(-0.48, 0.05, -1.55)
        gl.glScalef(0.12, 0.15, 0.12)
        self.draw_cube()
        gl.glPopMatrix()
        
        gl.glPushMatrix()
        gl.glTranslatef(0.48, 0.05, -1.55)
        gl.glScalef(0.12, 0.15, 0.12)
        self.draw_cube()
        gl.glPopMatrix()
        
        # ===== WHEELS (PREMIUM RUBBER) =====
        gl.glColor3f(0.12, 0.12, 0.12)
        
        # Front left wheel
        self.draw_wheel(-1.02, -0.68, 0.95)
        # Front right wheel
        self.draw_wheel(1.02, -0.68, 0.95)
        # Back left wheel
        self.draw_wheel(-1.02, -0.68, -1.25)
        # Back right wheel
        self.draw_wheel(1.02, -0.68, -1.25)
        
        # ===== PREMIUM RIMS (POLISHED ALUMINUM) =====
        gl.glColor3f(0.85, 0.85, 0.85)
        
        # Front left rim
        gl.glPushMatrix()
        gl.glTranslatef(-1.02, -0.68, 0.95)
        gl.glRotatef(90, 0, 1, 0)
        self.draw_cylinder(0.38, 0.28, 16)
        gl.glPopMatrix()
        
        # Front right rim
        gl.glPushMatrix()
        gl.glTranslatef(1.02, -0.68, 0.95)
        gl.glRotatef(90, 0, 1, 0)
        self.draw_cylinder(0.38, 0.28, 16)
        gl.glPopMatrix()
        
        # Back left rim
        gl.glPushMatrix()
        gl.glTranslatef(-1.02, -0.68, -1.25)
        gl.glRotatef(90, 0, 1, 0)
        self.draw_cylinder(0.38, 0.28, 16)
        gl.glPopMatrix()
        
        # Back right rim
        gl.glPushMatrix()
        gl.glTranslatef(1.02, -0.68, -1.25)
        gl.glRotatef(90, 0, 1, 0)
        self.draw_cylinder(0.38, 0.28, 16)
        gl.glPopMatrix()
        
        # ===== CENTER CAP (SHINY) =====
        gl.glColor3f(0.9, 0.9, 0.9)
        
        # Front left center cap
        gl.glPushMatrix()
        gl.glTranslatef(-1.02, -0.68, 0.95)
        self.draw_sphere(0.15, 8, 8)
        gl.glPopMatrix()
        
        # Front right center cap
        gl.glPushMatrix()
        gl.glTranslatef(1.02, -0.68, 0.95)
        self.draw_sphere(0.15, 8, 8)
        gl.glPopMatrix()
        
        # Back left center cap
        gl.glPushMatrix()
        gl.glTranslatef(-1.02, -0.68, -1.25)
        self.draw_sphere(0.15, 8, 8)
        gl.glPopMatrix()
        
        # Back right center cap
        gl.glPushMatrix()
        gl.glTranslatef(1.02, -0.68, -1.25)
        self.draw_sphere(0.15, 8, 8)
        gl.glPopMatrix()
        
        gl.glPopMatrix()
    
    def render_roads(self, roads):
        """Render all roads with lane markings"""
        # Draw road surface (dark gray)
        gl.glColor3f(0.2, 0.2, 0.2)  # Dark gray road
        
        for road in roads:
            gl.glBegin(gl.GL_TRIANGLES)
            for i in range(0, len(road.indices), 3):
                if i + 2 < len(road.indices):
                    for j in range(3):
                        idx = road.indices[i + j]
                        if idx < len(road.vertices):
                            v = road.vertices[idx]
                            gl.glVertex3f(v[0], v[1], v[2])
            gl.glEnd()
        
        # Draw lane markings (white center lines)
        gl.glColor3f(1.0, 1.0, 1.0)  # White
        gl.glLineWidth(3.0)
        
        for road in roads:
            if road.road_type == 'highway':
                # Calculate direction and length
                start = road.start_pos
                end = road.end_pos
                direction = end - start
                length = np.linalg.norm(direction)
                
                if length > 0.1:
                    direction = direction / length
                    
                    # Draw dashed line along road center
                    gl.glBegin(gl.GL_LINES)
                    for i in range(0, int(length), 20):
                        if i % 40 < 10:  # Dashed pattern
                            p1 = start + direction * i
                            p2 = start + direction * min(i + 8, length)
                            gl.glVertex3f(p1[0], p1[1] + 0.05, p1[2])
                            gl.glVertex3f(p2[0], p2[1] + 0.05, p2[2])
                    gl.glEnd()
        
        gl.glLineWidth(1.0)
    
    def render_environment(self, objects):
        """Render environment objects"""
        for obj in objects:
            gl.glPushMatrix()
            gl.glTranslatef(obj.position[0], obj.position[1], obj.position[2])
            
            # Color by type
            if obj.type == 'building':
                gl.glColor3f(0.7, 0.7, 0.7)  # Gray
            elif obj.type == 'ground':
                gl.glColor3f(0.4, 0.3, 0.2)  # Brown ground
            elif obj.type == 'barrier':
                # Ash color for barriers (light gray) - disable lighting for solid color
                gl.glDisable(gl.GL_LIGHTING)
                gl.glColor3f(0.7, 0.7, 0.7)  # Ash gray
            elif obj.type == 'tree':
                # Draw tree with trunk and foliage
                # Trunk (brown cylinder at bottom)
                gl.glPushMatrix()
                gl.glColor3f(0.6, 0.3, 0.1)  # Brown trunk
                gl.glScalef(obj.scale[0] * 0.3, obj.scale[1] * 0.3, obj.scale[2] * 0.3)
                self.draw_cylinder()
                gl.glPopMatrix()
                
                # Foliage (green sphere/rounded top)
                gl.glPushMatrix()
                gl.glColor3f(0.1, 0.6, 0.1)  # Green foliage
                gl.glTranslatef(0, obj.scale[1] * 0.5, 0)
                gl.glScalef(obj.scale[0] * 0.8, obj.scale[1] * 0.6, obj.scale[2] * 0.8)
                self.draw_sphere()
                gl.glPopMatrix()
            elif obj.type == 'streetlight':
                gl.glColor3f(0.8, 0.8, 0.3)  # Yellow
            else:
                gl.glColor3f(0.7, 0.7, 0.7)  # Ash gray default
            
            if obj.type != 'tree':
                gl.glScalef(obj.scale[0], obj.scale[1], obj.scale[2])
                
                # Draw simple shapes
                if obj.type == 'streetlight':
                    self.draw_cube()
                else:
                    self.draw_cube()
                
                # Re-enable lighting after barrier if it was disabled
                if obj.type == 'barrier':
                    gl.glEnable(gl.GL_LIGHTING)
            
            gl.glPopMatrix()
    
    def render_ground(self, objects):
        """Render only ground objects"""
        for obj in objects:
            if obj.type == 'ground':
                gl.glPushMatrix()
                gl.glTranslatef(obj.position[0], obj.position[1], obj.position[2])
                gl.glColor3f(0.4, 0.3, 0.2)  # Brown ground
                gl.glScalef(obj.scale[0], obj.scale[1], obj.scale[2])
                self.draw_cube()
                gl.glPopMatrix()
    
    def render_barriers(self, objects):
        """Render barriers and other non-ground environment"""
        for obj in objects:
            if obj.type != 'ground':
                # Skip collected balls
                if hasattr(obj, 'collected') and obj.collected:
                    continue
                
                # Handle special cases that don't need the standard transform
                if obj.type == 'start_line':
                    gl.glPushMatrix()
                    gl.glTranslatef(obj.position[0], obj.position[1], obj.position[2])
                    gl.glColor3f(1.0, 1.0, 1.0)  # White start line
                    gl.glScalef(obj.scale[0], obj.scale[1], obj.scale[2])
                    self.draw_cube()
                    gl.glPopMatrix()
                    continue
                
                elif obj.type == 'finish_line':
                    gl.glPushMatrix()
                    gl.glTranslatef(obj.position[0], obj.position[1], obj.position[2])
                    gl.glColor3f(1.0, 0.0, 0.0)  # Red finish line
                    gl.glScalef(obj.scale[0], obj.scale[1], obj.scale[2])
                    self.draw_cube()
                    gl.glPopMatrix()
                    continue
                    
                # Standard rendering for other objects
                gl.glPushMatrix()
                gl.glTranslatef(obj.position[0], obj.position[1], obj.position[2])
                
                # Skip collected balls
                if hasattr(obj, 'collected') and obj.collected:
                    gl.glPopMatrix()
                    continue
                
                # Color by type
                if obj.type == 'building':
                    gl.glColor3f(0.7, 0.7, 0.7)  # Gray
                elif obj.type == 'barrier':
                    # Ash color for barriers (light gray) - disable lighting for solid color
                    gl.glDisable(gl.GL_LIGHTING)
                    gl.glColor3f(0.7, 0.7, 0.7)  # Ash gray
                elif obj.type == 'pole':
                    gl.glColor3f(0.6, 0.4, 0.2)  # Brown wooden poles
                elif obj.type == 'green_ball':
                    gl.glColor3f(0.0, 1.0, 0.0)  # Bright green ball (4x speed)
                    gl.glScalef(obj.scale[0], obj.scale[1], obj.scale[2])
                    self.draw_sphere()
                    gl.glPopMatrix()
                    continue
                elif obj.type == 'red_ball':
                    gl.glColor3f(1.0, 0.0, 0.0)  # Bright red ball (slow down 4x)
                    gl.glScalef(obj.scale[0], obj.scale[1], obj.scale[2])
                    self.draw_sphere()
                    gl.glPopMatrix()
                    continue
                elif obj.type == 'yellow_ball':
                    gl.glColor3f(1.0, 1.0, 0.0)  # Bright yellow ball (4x speed)
                    gl.glScalef(obj.scale[0], obj.scale[1], obj.scale[2])
                    self.draw_sphere()
                    gl.glPopMatrix()
                    continue
                elif obj.type == 'booster':
                    gl.glColor3f(1.0, 1.0, 0.0)  # Yellow boost pads
                elif obj.type == 'tree':
                    # Draw tree with trunk and foliage
                    gl.glPushMatrix()
                    gl.glColor3f(0.6, 0.3, 0.1)  # Brown trunk
                    gl.glScalef(obj.scale[0] * 0.3, obj.scale[1] * 0.3, obj.scale[2] * 0.3)
                    self.draw_cylinder()
                    gl.glPopMatrix()
                    
                    gl.glPushMatrix()
                    gl.glColor3f(0.1, 0.6, 0.1)  # Green foliage
                    gl.glTranslatef(0, obj.scale[1] * 0.5, 0)
                    gl.glScalef(obj.scale[0] * 0.8, obj.scale[1] * 0.6, obj.scale[2] * 0.8)
                    self.draw_sphere()
                    gl.glPopMatrix()
                elif obj.type == 'streetlight':
                    gl.glColor3f(0.8, 0.8, 0.3)  # Yellow
                else:
                    gl.glColor3f(0.7, 0.7, 0.7)  # Ash gray default
                
                if obj.type != 'tree':
                    gl.glScalef(obj.scale[0], obj.scale[1], obj.scale[2])
                    self.draw_cube()
                    # Re-enable lighting after barrier if it was disabled
                    if obj.type == 'barrier':
                        gl.glEnable(gl.GL_LIGHTING)
                
                gl.glPopMatrix()
    
    def render_ai_cars(self, ai_cars):
        """Render AI cars with same design as player cars"""
        colors = [
            [0.2, 0.5, 1.0],    # Blue
            [1.0, 1.0, 0.2],    # Yellow
            [1.0, 0.5, 1.0],    # Magenta
            [0.2, 1.0, 1.0],    # Cyan
            [1.0, 0.6, 0.2],    # Orange
            [0.7, 0.2, 1.0],    # Purple
        ]
        
        for idx, ai_car in enumerate(ai_cars):
            gl.glPushMatrix()
            gl.glTranslatef(ai_car.position[0], ai_car.position[1], ai_car.position[2])
            
            # Rotate
            yaw_deg = math.degrees(ai_car.rotation[1])
            pitch_deg = math.degrees(ai_car.rotation[0])
            roll_deg = math.degrees(ai_car.rotation[2])
            gl.glRotatef(yaw_deg, 0, 1, 0)
            gl.glRotatef(pitch_deg, 1, 0, 0)
            gl.glRotatef(roll_deg, 0, 0, 1)
            
            # Get AI car color
            color = colors[idx % len(colors)]
            
            # ===== UNDERCARRIAGE =====
            gl.glColor3f(0.1, 0.1, 0.1)
            gl.glPushMatrix()
            gl.glTranslatef(0, -0.5, 0)
            gl.glScalef(1.15, 0.15, 2.5)
            self.draw_cube()
            gl.glPopMatrix()
            
            # ===== MAIN CHASSIS (BODY) - SMOOTH ROUNDED =====
            gl.glColor3f(color[0], color[1], color[2])
            gl.glPushMatrix()
            gl.glTranslatef(0, -0.25, 0)
            gl.glScalef(1.1, 0.6, 2.4)
            self.draw_sphere(1.0, 20, 20)
            gl.glPopMatrix()
            
            # ===== FRONT BUMPER =====
            gl.glColor3f(color[0] * 0.8, color[1] * 0.8, color[2] * 0.8)
            gl.glPushMatrix()
            gl.glTranslatef(0, -0.15, 1.5)
            gl.glScalef(1.15, 0.35, 0.3)
            self.draw_sphere(1.0, 12, 12)
            gl.glPopMatrix()
            
            # ===== FRONT GRILLE =====
            gl.glColor3f(0.2, 0.2, 0.2)
            gl.glPushMatrix()
            gl.glTranslatef(0, 0.05, 1.52)
            gl.glScalef(0.6, 0.35, 0.08)
            self.draw_cube()
            gl.glPopMatrix()
            
            # ===== HOOD =====
            gl.glColor3f(color[0] * 1.08, color[1] * 1.08, color[2] * 1.08)
            gl.glPushMatrix()
            gl.glTranslatef(0, 0.15, 1.2)
            gl.glScalef(0.95, 0.4, 0.8)
            self.draw_sphere(1.0, 18, 18)
            gl.glPopMatrix()
            
            # ===== HOOD VENTS =====
            gl.glColor3f(0.25, 0.25, 0.25)
            gl.glPushMatrix()
            gl.glTranslatef(-0.25, 0.25, 1.0)
            gl.glScalef(0.18, 0.1, 0.25)
            self.draw_cube()
            gl.glPopMatrix()
            gl.glPushMatrix()
            gl.glTranslatef(0.25, 0.25, 1.0)
            gl.glScalef(0.18, 0.1, 0.25)
            self.draw_cube()
            gl.glPopMatrix()
            
            # ===== REAR CARGO AREA =====
            gl.glColor3f(color[0] * 0.82, color[1] * 0.82, color[2] * 0.82)
            gl.glPushMatrix()
            gl.glTranslatef(0, 0.2, -1.35)
            gl.glScalef(1.0, 0.55, 0.7)
            self.draw_sphere(1.0, 16, 16)
            gl.glPopMatrix()
            
            # ===== REAR BUMPER =====
            gl.glColor3f(color[0] * 0.8, color[1] * 0.8, color[2] * 0.8)
            gl.glPushMatrix()
            gl.glTranslatef(0, -0.15, -1.55)
            gl.glScalef(1.15, 0.35, 0.25)
            self.draw_sphere(1.0, 12, 12)
            gl.glPopMatrix()
            
            # ===== REAR WING/SPOILER =====
            gl.glColor3f(0.15, 0.15, 0.15)
            gl.glPushMatrix()
            gl.glTranslatef(0, 0.65, -1.62)
            gl.glScalef(0.95, 0.55, 0.12)
            self.draw_cube()
            gl.glPopMatrix()
            
            # ===== WINDSHIELD =====
            gl.glColor3f(0.35, 0.55, 0.9)
            gl.glPushMatrix()
            gl.glTranslatef(0, 0.55, 0.8)
            gl.glScalef(0.82, 0.5, 0.15)
            self.draw_cube()
            gl.glPopMatrix()
            
            # ===== REAR WINDOW =====
            gl.glColor3f(0.35, 0.55, 0.9)
            gl.glPushMatrix()
            gl.glTranslatef(0, 0.5, -0.95)
            gl.glScalef(0.78, 0.45, 0.15)
            self.draw_cube()
            gl.glPopMatrix()
            
            # ===== SIDE WINDOWS =====
            gl.glColor3f(0.4, 0.6, 0.95)
            gl.glPushMatrix()
            gl.glTranslatef(-0.552, 0.45, 0.2)
            gl.glScalef(0.06, 0.55, 1.0)
            self.draw_cube()
            gl.glPopMatrix()
            gl.glPushMatrix()
            gl.glTranslatef(0.552, 0.45, 0.2)
            gl.glScalef(0.06, 0.55, 1.0)
            self.draw_cube()
            gl.glPopMatrix()
            
            # ===== SIDE SKIRTS =====
            gl.glColor3f(color[0] * 0.6, color[1] * 0.6, color[2] * 0.6)
            gl.glPushMatrix()
            gl.glTranslatef(-0.56, -0.2, 0)
            gl.glScalef(0.06, 0.35, 2.2)
            self.draw_cube()
            gl.glPopMatrix()
            gl.glPushMatrix()
            gl.glTranslatef(0.56, -0.2, 0)
            gl.glScalef(0.06, 0.35, 2.2)
            self.draw_cube()
            gl.glPopMatrix()
            
            # ===== FENDER FLARES =====
            gl.glColor3f(color[0] * 0.65, color[1] * 0.65, color[2] * 0.65)
            gl.glPushMatrix()
            gl.glTranslatef(-1.08, -0.15, 1.0)
            gl.glScalef(0.12, 0.4, 0.8)
            self.draw_cube()
            gl.glPopMatrix()
            gl.glPushMatrix()
            gl.glTranslatef(1.08, -0.15, 1.0)
            gl.glScalef(0.12, 0.4, 0.8)
            self.draw_cube()
            gl.glPopMatrix()
            
            # ===== MIRRORS =====
            gl.glColor3f(0.25, 0.25, 0.25)
            gl.glPushMatrix()
            gl.glTranslatef(-0.63, 0.4, 0.35)
            gl.glScalef(0.18, 0.3, 0.15)
            self.draw_cube()
            gl.glPopMatrix()
            gl.glPushMatrix()
            gl.glTranslatef(0.63, 0.4, 0.35)
            gl.glScalef(0.18, 0.3, 0.15)
            self.draw_cube()
            gl.glPopMatrix()
            
            # ===== HEADLIGHTS =====
            gl.glColor3f(0.95, 0.95, 0.75)
            gl.glPushMatrix()
            gl.glTranslatef(-0.3, 0.08, 1.53)
            gl.glScalef(0.2, 0.25, 0.15)
            self.draw_cube()
            gl.glPopMatrix()
            gl.glPushMatrix()
            gl.glTranslatef(0.3, 0.08, 1.53)
            gl.glScalef(0.2, 0.25, 0.15)
            self.draw_cube()
            gl.glPopMatrix()
            
            # ===== TAILLIGHTS =====
            gl.glColor3f(1.0, 0.15, 0.15)
            gl.glPushMatrix()
            gl.glTranslatef(-0.38, 0.1, -1.58)
            gl.glScalef(0.18, 0.25, 0.12)
            self.draw_cube()
            gl.glPopMatrix()
            gl.glPushMatrix()
            gl.glTranslatef(0.38, 0.1, -1.58)
            gl.glScalef(0.18, 0.25, 0.12)
            self.draw_cube()
            gl.glPopMatrix()
            
            # ===== FRONT TURN SIGNALS =====
            gl.glColor3f(1.0, 0.8, 0.2)
            gl.glPushMatrix()
            gl.glTranslatef(-0.45, -0.05, 1.5)
            gl.glScalef(0.12, 0.15, 0.12)
            self.draw_cube()
            gl.glPopMatrix()
            gl.glPushMatrix()
            gl.glTranslatef(0.45, -0.05, 1.5)
            gl.glScalef(0.12, 0.15, 0.12)
            self.draw_cube()
            gl.glPopMatrix()
            
            # ===== REAR TURN SIGNALS =====
            gl.glPushMatrix()
            gl.glTranslatef(-0.48, 0.05, -1.55)
            gl.glScalef(0.12, 0.15, 0.12)
            self.draw_cube()
            gl.glPopMatrix()
            gl.glPushMatrix()
            gl.glTranslatef(0.48, 0.05, -1.55)
            gl.glScalef(0.12, 0.15, 0.12)
            self.draw_cube()
            gl.glPopMatrix()
            
            # ===== WHEELS =====
            gl.glColor3f(0.12, 0.12, 0.12)
            self.draw_wheel(-1.02, -0.68, 0.95)
            self.draw_wheel(1.02, -0.68, 0.95)
            self.draw_wheel(-1.02, -0.68, -1.25)
            self.draw_wheel(1.02, -0.68, -1.25)
            
            # ===== RIMS =====
            gl.glColor3f(0.85, 0.85, 0.85)
            gl.glPushMatrix()
            gl.glTranslatef(-1.02, -0.68, 0.95)
            gl.glRotatef(90, 0, 1, 0)
            self.draw_cylinder(0.38, 0.28, 16)
            gl.glPopMatrix()
            
            gl.glPushMatrix()
            gl.glTranslatef(1.02, -0.68, 0.95)
            gl.glRotatef(90, 0, 1, 0)
            self.draw_cylinder(0.38, 0.28, 16)
            gl.glPopMatrix()
            
            gl.glPushMatrix()
            gl.glTranslatef(-1.02, -0.68, -1.25)
            gl.glRotatef(90, 0, 1, 0)
            self.draw_cylinder(0.38, 0.28, 16)
            gl.glPopMatrix()
            
            gl.glPushMatrix()
            gl.glTranslatef(1.02, -0.68, -1.25)
            gl.glRotatef(90, 0, 1, 0)
            self.draw_cylinder(0.38, 0.28, 16)
            gl.glPopMatrix()
            
            # ===== CENTER CAPS =====
            gl.glColor3f(0.9, 0.9, 0.9)
            gl.glPushMatrix()
            gl.glTranslatef(-1.02, -0.68, 0.95)
            self.draw_sphere(0.15, 8, 8)
            gl.glPopMatrix()
            
            gl.glPushMatrix()
            gl.glTranslatef(1.02, -0.68, 0.95)
            self.draw_sphere(0.15, 8, 8)
            gl.glPopMatrix()
            
            gl.glPushMatrix()
            gl.glTranslatef(-1.02, -0.68, -1.25)
            self.draw_sphere(0.15, 8, 8)
            gl.glPopMatrix()
            
            gl.glPushMatrix()
            gl.glTranslatef(1.02, -0.68, -1.25)
            self.draw_sphere(0.15, 8, 8)
            gl.glPopMatrix()
            
            gl.glPopMatrix()
    
    @staticmethod
    def draw_cube():
        """Draw a unit cube"""
        gl.glBegin(gl.GL_QUADS)
        
        # Front face
        gl.glNormal3f(0, 0, 1)
        gl.glVertex3f(-1, -1, 1)
        gl.glVertex3f(1, -1, 1)
        gl.glVertex3f(1, 1, 1)
        gl.glVertex3f(-1, 1, 1)
        
        # Back face
        gl.glNormal3f(0, 0, -1)
        gl.glVertex3f(-1, -1, -1)
        gl.glVertex3f(-1, 1, -1)
        gl.glVertex3f(1, 1, -1)
        gl.glVertex3f(1, -1, -1)
        
        # Top face
        gl.glNormal3f(0, 1, 0)
        gl.glVertex3f(-1, 1, -1)
        gl.glVertex3f(-1, 1, 1)
        gl.glVertex3f(1, 1, 1)
        gl.glVertex3f(1, 1, -1)
        
        # Bottom face
        gl.glNormal3f(0, -1, 0)
        gl.glVertex3f(-1, -1, -1)
        gl.glVertex3f(1, -1, -1)
        gl.glVertex3f(1, -1, 1)
        gl.glVertex3f(-1, -1, 1)
        
        # Right face
        gl.glNormal3f(1, 0, 0)
        gl.glVertex3f(1, -1, -1)
        gl.glVertex3f(1, 1, -1)
        gl.glVertex3f(1, 1, 1)
        gl.glVertex3f(1, -1, 1)
        
        # Left face
        gl.glNormal3f(-1, 0, 0)
        gl.glVertex3f(-1, -1, -1)
        gl.glVertex3f(-1, -1, 1)
        gl.glVertex3f(-1, 1, 1)
        gl.glVertex3f(-1, 1, -1)
        
        gl.glEnd()
    
    @staticmethod
    def draw_cylinder(radius=1.0, height=1.0, segments=16):
        """Draw a cylinder"""
        gl.glBegin(gl.GL_TRIANGLE_STRIP)
        
        for i in range(segments + 1):
            angle = 2 * math.pi * i / segments
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            
            # Top
            gl.glNormal3f(x, 0, z)
            gl.glVertex3f(x, height, z)
            
            # Bottom
            gl.glVertex3f(x, 0, z)
        
        gl.glEnd()
        
        # Top cap
        gl.glBegin(gl.GL_TRIANGLE_FAN)
        gl.glNormal3f(0, 1, 0)
        gl.glVertex3f(0, height, 0)
        for i in range(segments + 1):
            angle = 2 * math.pi * i / segments
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            gl.glVertex3f(x, height, z)
        gl.glEnd()
        
        # Bottom cap
        gl.glBegin(gl.GL_TRIANGLE_FAN)
        gl.glNormal3f(0, -1, 0)
        gl.glVertex3f(0, 0, 0)
        for i in range(segments + 1):
            angle = 2 * math.pi * i / segments
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            gl.glVertex3f(x, 0, z)
        gl.glEnd()
    
    @staticmethod
    def draw_sphere(radius=1.0, sectors=16, stacks=16):
        """Draw a sphere for tree foliage"""
        for i in range(stacks):
            lat0 = math.pi * (-0.5 + float(i) / stacks)
            lat1 = math.pi * (-0.5 + float(i + 1) / stacks)
            
            gl.glBegin(gl.GL_TRIANGLE_STRIP)
            for j in range(sectors + 1):
                lng = 2 * math.pi * float(j) / sectors
                
                x0 = math.cos(lat0) * math.cos(lng) * radius
                y0 = math.sin(lat0) * radius
                z0 = math.cos(lat0) * math.sin(lng) * radius
                
                x1 = math.cos(lat1) * math.cos(lng) * radius
                y1 = math.sin(lat1) * radius
                z1 = math.cos(lat1) * math.sin(lng) * radius
                
                gl.glVertex3f(x0, y0, z0)
                gl.glVertex3f(x1, y1, z1)
            
            gl.glEnd()
    
    def create_display_lists(self):
        """Create display lists for cached geometry (PERFORMANCE CRITICAL)"""
        try:
            # Create cube display list
            self.cube_list = gl.glGenLists(1)
            gl.glNewList(self.cube_list, gl.GL_COMPILE)
            self.draw_cube()
            gl.glEndList()
            
            # Create sphere display list
            self.sphere_list = gl.glGenLists(1)
            gl.glNewList(self.sphere_list, gl.GL_COMPILE)
            self.draw_sphere(radius=1.0, sectors=8, stacks=8)  # Lower poly for speed
            gl.glEndList()
            
            # Create cylinder display list
            self.cylinder_list = gl.glGenLists(1)
            gl.glNewList(self.cylinder_list, gl.GL_COMPILE)
            self.draw_cylinder(radius=1.0, height=1.0, segments=8)  # Lower poly for speed
            gl.glEndList()
        except Exception as e:
            print(f"Warning: Could not create display lists: {e}")
    
    def cleanup(self):
        """Cleanup resources"""
        if self.cube_list is not None:
            gl.glDeleteLists(self.cube_list, 1)
        if self.sphere_list is not None:
            gl.glDeleteLists(self.sphere_list, 1)
        if self.cylinder_list is not None:
            gl.glDeleteLists(self.cylinder_list, 1)
    
    def render_scene(self, world, car, camera, width, height, race_standings=None):
        """Complete rendering pipeline - called from main game loop"""
        self.clear()
        self.setup_matrices_with_camera(camera, width, height, car)
        
        # Draw ground plane (grass background) - REMOVED
        # gl.glColor3f(0.2, 0.6, 0.2)  # Green grass
        # gl.glBegin(gl.GL_QUADS)
        # size = 2000
        # gl.glVertex3f(-size, -0.1, -size)
        # gl.glVertex3f(size, -0.1, -size)
        # gl.glVertex3f(size, -0.1, size)
        # gl.glVertex3f(-size, -0.1, size)
        # gl.glEnd()
        
        # Draw ground first (underneath everything)
        self.render_ground(world.environment_objects)
        
        # Draw roads
        self.render_roads(world.road_segments)
        
        # Draw barriers and other environment
        self.render_barriers(world.environment_objects)
        
        # Draw car (red cube)
        self.render_car(car)
        
        # Draw AI cars
        self.render_ai_cars(world.ai_cars)
        
        # Draw 2D race standings overlay (DISABLED)
        # if race_standings:
        #     self.render_race_standings_2d(race_standings, width, height)
    
    def render_race_standings_2d(self, race_standings, width, height):
        """Render race standings as 2D overlay in top-right corner"""
        # Switch to 2D rendering
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPushMatrix()
        gl.glLoadIdentity()
        gl.glOrtho(0, width, height, 0, -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()
        gl.glLoadIdentity()
        
        # Disable depth test and lighting for 2D rendering
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glDisable(gl.GL_LIGHTING)
        
        # Check if race is finished
        all_finished = (race_standings.get('player_finished', False) and 
                       race_standings.get('ai1_finished', False) and
                       race_standings.get('ai2_finished', False) and
                       race_standings.get('ai3_finished', False))
        
        # Draw semi-transparent background box
        padding = 20
        box_width = 280
        box_height = 200
        x_pos = width - box_width - padding
        y_pos = padding
        
        # Semi-transparent black background
        gl.glColor4f(0, 0, 0, 0.8)
        gl.glBegin(gl.GL_QUADS)
        gl.glVertex2f(x_pos, y_pos)
        gl.glVertex2f(x_pos + box_width, y_pos)
        gl.glVertex2f(x_pos + box_width, y_pos + box_height)
        gl.glVertex2f(x_pos, y_pos + box_height)
        gl.glEnd()
        
        # Draw border
        gl.glColor3f(0.2, 0.8, 0.2)
        gl.glLineWidth(2.0)
        gl.glBegin(gl.GL_LINE_LOOP)
        gl.glVertex2f(x_pos, y_pos)
        gl.glVertex2f(x_pos + box_width, y_pos)
        gl.glVertex2f(x_pos + box_width, y_pos + box_height)
        gl.glVertex2f(x_pos, y_pos + box_height)
        gl.glEnd()
        gl.glLineWidth(1.0)
        
        # Draw standings (using colored squares as placeholders)
        standings_data = [
            {'name': 'YOU 🔴', 'distance': race_standings['player_distance'], 'color': (1, 0.2, 0.2), 'finished': race_standings.get('player_finished', False)},
            {'name': 'AI-1 🔵', 'distance': race_standings['ai1_distance'], 'color': (0.2, 0.5, 1), 'finished': race_standings.get('ai1_finished', False)},
            {'name': 'AI-2 🟡', 'distance': race_standings['ai2_distance'], 'color': (1, 1, 0.2), 'finished': race_standings.get('ai2_finished', False)},
            {'name': 'AI-3 🟣', 'distance': race_standings['ai3_distance'], 'color': (1, 0.5, 1), 'finished': race_standings.get('ai3_finished', False)},
        ]
        
        # Sort by distance (highest = 1st)
        standings_data.sort(key=lambda x: x['distance'], reverse=True)
        
        # Title
        title_y = y_pos + 15
        gl.glColor3f(0.2, 1, 0.2)
        self.draw_text_simple("STANDINGS", x_pos + 95, title_y)
        
        # Standings items
        y_offset = 50
        for idx, data in enumerate(standings_data, 1):
            item_y = y_pos + y_offset
            
            # Draw place number (gold for 1st, silver for others)
            if idx == 1:
                gl.glColor3f(1, 0.84, 0)  # Gold
                rank_num = "1"
            elif idx == 2:
                gl.glColor3f(0.75, 0.75, 0.75)  # Silver
                rank_num = "2"
            elif idx == 3:
                gl.glColor3f(0.7, 0.4, 0)  # Bronze
                rank_num = "3"
            else:
                gl.glColor3f(0.5, 0.5, 0.5)
                rank_num = "4"
            
            # Draw colored rectangle for car
            box_x = x_pos + 15
            rect_size = 20
            gl.glBegin(gl.GL_QUADS)
            gl.glColor3f(data['color'][0], data['color'][1], data['color'][2])
            gl.glVertex2f(box_x, item_y)
            gl.glVertex2f(box_x + rect_size, item_y)
            gl.glVertex2f(box_x + rect_size, item_y + rect_size)
            gl.glVertex2f(box_x, item_y + rect_size)
            gl.glEnd()
            
            # Draw position number inside box
            gl.glColor3f(0, 0, 0)
            self.draw_text_simple(rank_num, box_x + 6, item_y + 2)
            
            # Draw text (distance)
            gl.glColor3f(1, 1, 1)
            distance_text = f"{data['distance']:.0f}m"
            finish_mark = " ✓" if data['finished'] else ""
            self.draw_text_simple(f"{distance_text}{finish_mark}", x_pos + 70, item_y + 5)
            
            y_offset += 35
        
        # Draw VICTORY message if all finished
        if all_finished:
            victory_box_height = 60
            victory_box_width = 280
            victory_box_y = height // 2 - victory_box_height // 2
            victory_box_x = width // 2 - victory_box_width // 2
            
            # Draw semi-transparent background
            gl.glColor4f(0.2, 0.8, 0.2, 0.9)
            gl.glBegin(gl.GL_QUADS)
            gl.glVertex2f(victory_box_x, victory_box_y)
            gl.glVertex2f(victory_box_x + victory_box_width, victory_box_y)
            gl.glVertex2f(victory_box_x + victory_box_width, victory_box_y + victory_box_height)
            gl.glVertex2f(victory_box_x, victory_box_y + victory_box_height)
            gl.glEnd()
            
            # Draw yellow border
            gl.glColor3f(1, 1, 0)
            gl.glLineWidth(3.0)
            gl.glBegin(gl.GL_LINE_LOOP)
            gl.glVertex2f(victory_box_x, victory_box_y)
            gl.glVertex2f(victory_box_x + victory_box_width, victory_box_y)
            gl.glVertex2f(victory_box_x + victory_box_width, victory_box_y + victory_box_height)
            gl.glVertex2f(victory_box_x, victory_box_y + victory_box_height)
            gl.glEnd()
            gl.glLineWidth(1.0)
            
            # Draw VICTORY text
            gl.glColor3f(0, 0, 0)
            self.draw_text_simple("🏆 RACE COMPLETE 🏆", victory_box_x + 60, victory_box_y + 20)
        
        # Re-enable rendering
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_LIGHTING)
        
        # Restore 3D rendering
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPopMatrix()
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPopMatrix()
    
    def render_split_scene(self, world, car, camera, screen_width, screen_height, x_offset, 
                          player_name="Player", player_distance=0, opponent_distance=0):
        """Render one half of split-screen for 2-player multiplayer"""
        # Set up viewport for this half of screen
        gl.glViewport(x_offset, 0, screen_width, screen_height)
        
        # Setup matrices for this viewport (DO NOT CLEAR - cleared once per frame)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        
        # Projection matrix
        aspect = screen_width / screen_height
        near = 0.1
        far = 5000.0
        fov = 60.0
        f = 1.0 / math.tan(math.radians(fov) / 2.0)
        gl.glFrustum(-near * aspect, near * aspect, -near, near, near, far)
        
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        
        # Simple but effective camera: follow behind and above the car
        car_x = camera.target_car.position[0]
        car_y = camera.target_car.position[1]
        car_z = camera.target_car.position[2]
        car_yaw = camera.target_car.rotation[1]
        
        # Position camera 15 units behind car and 4 units above
        cam_distance = 15.0
        cam_height = 4.0
        
        cam_x = car_x - math.sin(car_yaw) * cam_distance
        cam_z = car_z - math.cos(car_yaw) * cam_distance
        cam_y = car_y + cam_height
        
        # Look point slightly ahead of car
        look_ahead = 5.0
        look_x = car_x + math.sin(car_yaw) * look_ahead
        look_z = car_z + math.cos(car_yaw) * look_ahead
        look_y = car_y + 1.0
        
        gluLookAt(
            cam_x, cam_y, cam_z,           # Camera position
            look_x, look_y, look_z,         # Look at point
            0, 1, 0                         # Up vector
        )
        
        # Draw ground
        self.render_ground(world.environment_objects)
        
        # Draw roads
        self.render_roads(world.road_segments)
        
        # Draw barriers
        self.render_barriers(world.environment_objects)
        
        # Draw this car
        self.render_car(car)
        
        # Draw 2D overlay for this player
        self.render_split_screen_overlay(screen_width, screen_height, x_offset, player_name, 
                                         player_distance, opponent_distance)
    
    def render_split_screen_overlay(self, screen_width, screen_height, x_offset, player_name, 
                                   player_distance, opponent_distance):
        """Render 2D overlay for split-screen player info"""
        # Switch to 2D rendering
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPushMatrix()
        gl.glLoadIdentity()
        gl.glOrtho(x_offset, x_offset + screen_width, screen_height, 0, -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()
        gl.glLoadIdentity()
        
        # Disable depth test and lighting for 2D rendering
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glDisable(gl.GL_LIGHTING)
        
        # Draw player info box in top-left corner of this viewport
        padding = 20
        box_width = 250
        box_height = 100
        box_x = x_offset + padding
        box_y = padding
        
        # Semi-transparent background
        gl.glColor4f(0, 0, 0, 0.7)
        gl.glBegin(gl.GL_QUADS)
        gl.glVertex2f(box_x, box_y)
        gl.glVertex2f(box_x + box_width, box_y)
        gl.glVertex2f(box_x + box_width, box_y + box_height)
        gl.glVertex2f(box_x, box_y + box_height)
        gl.glEnd()
        
        # Draw border (player colored)
        if "RED" in player_name:
            border_color = (1, 0, 0)
        elif "GREEN" in player_name:
            border_color = (0, 1, 0)
        else:
            border_color = (0.5, 0.5, 1)
        
        gl.glColor3f(border_color[0], border_color[1], border_color[2])
        gl.glLineWidth(2.0)
        gl.glBegin(gl.GL_LINE_LOOP)
        gl.glVertex2f(box_x, box_y)
        gl.glVertex2f(box_x + box_width, box_y)
        gl.glVertex2f(box_x + box_width, box_y + box_height)
        gl.glVertex2f(box_x, box_y + box_height)
        gl.glEnd()
        gl.glLineWidth(1.0)
        
        # Draw player name
        gl.glColor3f(1, 1, 1)
        self.draw_text_simple(player_name, box_x + 10, box_y + 15)
        
        # Draw distance info
        gl.glColor3f(1, 1, 0)
        dist_text = f"Distance: {player_distance:.0f}m"
        self.draw_text_simple(dist_text, box_x + 10, box_y + 40)
        
        # Draw opponent info
        gl.glColor3f(0.7, 0.7, 0.7)
        gap = player_distance - opponent_distance
        gap_text = f"Gap: {abs(gap):.0f}m"
        self.draw_text_simple(gap_text, box_x + 10, box_y + 60)
        
        # Re-enable rendering
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_LIGHTING)
        
        # Restore 3D rendering
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPopMatrix()
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPopMatrix()
    
    def draw_text_simple(self, text, x, y):
        """Draw simple text using OpenGL (placeholder - just draws a background)"""
        # This is a simple visual indicator
        # Real text rendering would require font support
        gl.glRasterPos2f(x, y)
        # Note: Proper text rendering requires pygame font or FreeType
    
    def cleanup(self):
        """Cleanup resources"""
        pass
