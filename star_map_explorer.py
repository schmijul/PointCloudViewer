import numpy as np
from point_cloud_viewer import PointCloudViewer

def generate_star_map(num_stars=10000, spread=1000):
    """Generate a procedurally generated star map."""
    # Generate random positions within a cubic space
    x = np.random.uniform(-spread, spread, num_stars)
    y = np.random.uniform(-spread, spread, num_stars)
    z = np.random.uniform(-spread, spread, num_stars)

    # Optionally, assign random colors to stars
    colors = np.random.uniform(0.5, 1.0, (num_stars, 3))  # Slightly bright stars

    points = np.vstack((x, y, z, colors[:, 0], colors[:, 1], colors[:, 2])).T
    return points

if __name__ == "__main__":
    # Generate a procedurally generated star map
    star_map = generate_star_map(num_stars=20000, spread=5000)

    # Initialize the PointCloudViewer with the generated star data
    viewer = PointCloudViewer(points=star_map)

    # Set up mouse and keyboard interaction callbacks
    viewer.setup_callbacks()

    # Start rendering the star map
    viewer.render()

    # Optionally: Save the point cloud to a file after rendering
    viewer.save_to_ply("star_map.ply")
    viewer.save_to_csv("star_map.csv")

