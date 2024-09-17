import numpy as np
from point_cloud_viewer import PointCloudViewer

if __name__ == "__main__":
    # Generate example 3D point data (replace with actual data)
    x = np.random.uniform(-5, 5, 1000)
    y = np.random.uniform(-5, 5, 1000)
    z = np.random.uniform(-5, 5, 1000)
    points = np.vstack((x, y, z)).T  # Combine into Nx3 array
    
    # Initialize the PointCloudViewer with the generated point data
    viewer = PointCloudViewer(points=points)
    
    # Set up mouse interaction callbacks
    viewer.setup_callbacks()

    # Start rendering the point cloud
    viewer.render()

    # Optionally: Save the point cloud to a file after rendering
    viewer.save_to_ply("point_cloud.ply")
    viewer.save_to_csv("point_cloud.csv")

