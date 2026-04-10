"""
Debugging and profiling utilities
"""
import time


class PerformanceMonitor:
    """Monitor performance metrics"""
    
    def __init__(self):
        self.timers = {}
        self.frame_times = []
        self.max_frames_history = 120
    
    def start_timer(self, name):
        """Start a timer"""
        self.timers[name] = time.time()
    
    def end_timer(self, name):
        """End a timer and return elapsed time"""
        if name in self.timers:
            elapsed = time.time() - self.timers[name]
            del self.timers[name]
            return elapsed
        return 0.0
    
    def record_frame_time(self, frame_time):
        """Record a frame time"""
        self.frame_times.append(frame_time)
        if len(self.frame_times) > self.max_frames_history:
            self.frame_times.pop(0)
    
    def get_average_frame_time(self):
        """Get average frame time"""
        if not self.frame_times:
            return 0.0
        return sum(self.frame_times) / len(self.frame_times)
    
    def get_fps(self):
        """Get average FPS"""
        avg_time = self.get_average_frame_time()
        if avg_time == 0:
            return 0
        return 1.0 / avg_time
    
    def get_min_frame_time(self):
        """Get minimum frame time"""
        return min(self.frame_times) if self.frame_times else 0.0
    
    def get_max_frame_time(self):
        """Get maximum frame time"""
        return max(self.frame_times) if self.frame_times else 0.0
    
    def print_stats(self):
        """Print performance statistics"""
        print(f"=== Performance Stats ===")
        print(f"Average FPS: {self.get_fps():.2f}")
        print(f"Average Frame Time: {self.get_average_frame_time() * 1000:.2f}ms")
        print(f"Min Frame Time: {self.get_min_frame_time() * 1000:.2f}ms")
        print(f"Max Frame Time: {self.get_max_frame_time() * 1000:.2f}ms")
        print(f"Frame History: {len(self.frame_times)} frames")


class DebugRenderer:
    """Render debug information"""
    
    @staticmethod
    def print_car_info(car):
        """Print car information"""
        print(f"\n=== Car Information ===")
        print(f"Position: ({car.position[0]:.1f}, {car.position[1]:.1f}, {car.position[2]:.1f})")
        print(f"Velocity: {car.velocity:.2f} units/sec")
        print(f"Rotation: ({car.rotation[0]:.2f}, {car.rotation[1]:.2f}, {car.rotation[2]:.2f})")
        print(f"Steering: {car.steering_angle:.2f}°")
        print(f"Car Type: {car.car_type.name}")
        print(f"Nitro: {car.nitro_amount:.1f}/{car.nitro_amount:.1f}")
        print(f"Nitro Active: {car.nitro_active}")
        print(f"Current Terrain: {car.current_terrain}")
    
    @staticmethod
    def print_camera_info(camera):
        """Print camera information"""
        print(f"\n=== Camera Information ===")
        print(f"Position: ({camera.position[0]:.1f}, {camera.position[1]:.1f}, {camera.position[2]:.1f})")
        print(f"Lookat: ({camera.lookat[0]:.1f}, {camera.lookat[1]:.1f}, {camera.lookat[2]:.1f})")
        print(f"Distance: {camera.distance:.2f}")
        print(f"Height: {camera.height:.2f}")
        print(f"FOV: {camera.fov:.2f}°")
    
    @staticmethod
    def print_world_info(world):
        """Print world information"""
        print(f"\n=== World Information ===")
        print(f"Loaded Chunks: {len(world.chunk_manager.chunks)}")
        print(f"Current Chunk: {world.chunk_manager.current_chunk}")
        print(f"Road Segments: {len(world.road_segments)}")
        print(f"Environment Objects: {len(world.environment_objects)}")


class DebugLogger:
    """Log debug messages"""
    
    def __init__(self, filename='debug.log'):
        self.filename = filename
        self.log_file = None
        self.open_log()
    
    def open_log(self):
        """Open log file"""
        try:
            self.log_file = open(self.filename, 'w')
        except IOError:
            print(f"Could not open log file: {self.filename}")
    
    def log(self, message):
        """Write message to log"""
        if self.log_file:
            timestamp = time.strftime("%H:%M:%S")
            log_message = f"[{timestamp}] {message}\n"
            self.log_file.write(log_message)
            self.log_file.flush()
    
    def close(self):
        """Close log file"""
        if self.log_file:
            self.log_file.close()
