import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import csv

class PointCloudViewer:
    """
    A general-purpose 3D point cloud viewer using OpenGL and GLFW.
    
    Attributes:
    -----------
    window : object
        The GLFW window object.
    points : np.ndarray
        The 3D point cloud data (Nx3 array of x, y, z coordinates).
    cam_distance : float
        Distance of the camera from the point cloud.
    cam_angle_x : float
        Camera's horizontal rotation angle.
    cam_angle_y : float
        Camera's vertical rotation angle.
    """
    
    def __init__(self, width=800, height=600, title="3D Point Cloud Viewer", points=None):
        """Initialize the PointCloudViewer with a window and point cloud data."""
        self.width = width
        self.height = height
        self.title = title
        self.points = points if points is not None else np.array([])
        
        self.cam_distance = 50.0
        self.cam_angle_x = 0
        self.cam_angle_y = 0
        self.last_x = width // 2
        self.last_y = height // 2
        self.mouse_left_pressed = False
        
        # Initialize GLFW and OpenGL
        self.window = self.init_window()
        self.init_opengl()

    def init_window(self):
        """Initialize the GLFW window."""
        if not glfw.init():
            raise Exception("GLFW initialization failed!")
        window = glfw.create_window(self.width, self.height, self.title, None, None)
        if not window:
            glfw.terminate()
            raise Exception("GLFW window creation failed!")
        glfw.make_context_current(window)
        return window

    def init_opengl(self):
        """Set up the OpenGL context and projection."""
        glEnable(GL_DEPTH_TEST)  # Enable depth testing for 3D rendering
        glPointSize(5)  # Set point size for point cloud
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Background color
        
        # Set up projection matrix
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, self.width / self.height, 0.1, 1000)  # Set perspective
        
        # Set up model view matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def mouse_callback(self, window, xpos, ypos):
        """Handle mouse movements for camera rotation."""
        if self.mouse_left_pressed:
            dx = xpos - self.last_x
            dy = ypos - self.last_y
            self.cam_angle_x += dx * 0.1
            self.cam_angle_y += dy * 0.1
        self.last_x, self.last_y = xpos, ypos

    def mouse_button_callback(self, window, button, action, mods):
        """Handle mouse button presses."""
        if button == glfw.MOUSE_BUTTON_LEFT:
            self.mouse_left_pressed = (action == glfw.PRESS)

    def scroll_callback(self, window, xoffset, yoffset):
        """Handle scroll wheel for zoom."""
        self.cam_distance -= yoffset * 2

    def apply_camera_transformations(self):
        """Apply camera transformations for rotating and zooming the view."""
        glTranslatef(0.0, 0.0, -self.cam_distance)  # Move camera backwards
        glRotatef(self.cam_angle_y, 1.0, 0.0, 0.0)  # Rotate vertically
        glRotatef(self.cam_angle_x, 0.0, 1.0, 0.0)  # Rotate horizontally

    def render(self):
        """Main rendering loop to display the point cloud."""
        while not glfw.window_should_close(self.window):
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()

            self.apply_camera_transformations()  # Apply the camera view

            # Render the point cloud
            glBegin(GL_POINTS)
            for x, y, z in self.points:
                glVertex3f(x, y, z)
            glEnd()

            glfw.swap_buffers(self.window)
            glfw.poll_events()

        glfw.terminate()

    def save_to_ply(self, filename):
        """Save the point cloud to a .ply file."""
        with open(filename, 'w') as f:
            f.write(f"ply\nformat ascii 1.0\n")
            f.write(f"element vertex {len(self.points)}\n")
            f.write(f"property float x\nproperty float y\nproperty float z\n")
            f.write(f"end_header\n")
            for point in self.points:
                f.write(f"{point[0]} {point[1]} {point[2]}\n")
        print(f"Point cloud saved to {filename}")

    def save_to_csv(self, filename):
        """Save the point cloud to a .csv file."""
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["x", "y", "z"])
            writer.writerows(self.points)
        print(f"Point cloud saved to {filename}")

    def setup_callbacks(self):
        """Set up GLFW callbacks for mouse interaction."""
        glfw.set_cursor_pos_callback(self.window, self.mouse_callback)
        glfw.set_mouse_button_callback(self.window, self.mouse_button_callback)
        glfw.set_scroll_callback(self.window, self.scroll_callback)

