#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates complex synthetic point cloud data with multiple 3D shapes.
"""

import numpy as np
from pointcloud_data import PointCloudData
import math

def generate_sphere(center, radius, num_points, intensity_range=(0.5, 1.0)):
    """
    Generates points on the surface of a sphere.

    Parameters:
    - center: Tuple of (x, y, z) coordinates.
    - radius: Radius of the sphere.
    - num_points: Number of points to generate.
    - intensity_range: Tuple indicating the range of intensity values.

    Returns:
    - points: Nx4 numpy array of points.
    """
    phi = np.random.uniform(0, 2 * np.pi, num_points)
    costheta = np.random.uniform(-1, 1, num_points)
    theta = np.arccos(costheta)

    x = center[0] + radius * np.sin(theta) * np.cos(phi)
    y = center[1] + radius * np.sin(theta) * np.sin(phi)
    z = center[2] + radius * costheta

    intensity = np.random.uniform(intensity_range[0], intensity_range[1], num_points)

    points = np.vstack((x, y, z, intensity)).T.astype(np.float32)
    return points

def generate_cube(center, side_length, num_points, intensity_range=(0.0, 0.5)):
    """
    Generates points within a cube.

    Parameters:
    - center: Tuple of (x, y, z) coordinates.
    - side_length: Length of the cube's sides.
    - num_points: Number of points to generate.
    - intensity_range: Tuple indicating the range of intensity values.

    Returns:
    - points: Nx4 numpy array of points.
    """
    half_side = side_length / 2.0
    x = np.random.uniform(center[0] - half_side, center[0] + half_side, num_points)
    y = np.random.uniform(center[1] - half_side, center[1] + half_side, num_points)
    z = np.random.uniform(center[2] - half_side, center[2] + half_side, num_points)

    intensity = np.random.uniform(intensity_range[0], intensity_range[1], num_points)

    points = np.vstack((x, y, z, intensity)).T.astype(np.float32)
    return points

def generate_torus(center, major_radius, minor_radius, num_points, intensity_range=(0.2, 0.8)):
    """
    Generates points on the surface of a torus.

    Parameters:
    - center: Tuple of (x, y, z) coordinates.
    - major_radius: Distance from the center of the tube to the center of the torus.
    - minor_radius: Radius of the tube.
    - num_points: Number of points to generate.
    - intensity_range: Tuple indicating the range of intensity values.

    Returns:
    - points: Nx4 numpy array of points.
    """
    u = np.random.uniform(0, 2 * np.pi, num_points)
    v = np.random.uniform(0, 2 * np.pi, num_points)

    x = center[0] + (major_radius + minor_radius * np.cos(v)) * np.cos(u)
    y = center[1] + (major_radius + minor_radius * np.cos(v)) * np.sin(u)
    z = center[2] + minor_radius * np.sin(v)

    intensity = np.random.uniform(intensity_range[0], intensity_range[1], num_points)

    points = np.vstack((x, y, z, intensity)).T.astype(np.float32)
    return points

def generate_combined_scene():
    """
    Generates a combined point cloud scene with multiple shapes.

    Returns:
    - combined_points: Nx4 numpy array of points.
    """
    np.random.seed(42)  # For reproducibility

    # Generate different shapes
    sphere = generate_sphere(center=(0, 0, 0), radius=1.0, num_points=10000, intensity_range=(0.7, 1.0))
    cube = generate_cube(center=(3, 3, 3), side_length=2.0, num_points=8000, intensity_range=(0.0, 0.5))
    torus = generate_torus(center=(-3, -3, -3), major_radius=1.5, minor_radius=0.5, num_points=12000, intensity_range=(0.2, 0.8))

    # Combine all points
    combined_points = np.vstack((sphere, cube, torus))
    
    # Optionally, add some noise
    noise = np.random.normal(0, 0.05, combined_points.shape).astype(np.float32)
    #combined_points += noise

    return combined_points

def main():
    # Initialize PointCloudData
    pc = PointCloudData("complex_pointcloud.bin", mode='w+', initial_capacity=32000)  # Total points: 10k + 8k + 12k = 30k

    # Generate combined scene
    combined_points = generate_combined_scene()
    print(f"Generated point cloud with {len(combined_points)} points.")

    # Append points to the point cloud data
    pc.append_points(combined_points)
    pc.flush()
    pc.close()
    print("Point cloud data saved to 'complex_pointcloud.bin'.")

if __name__ == "__main__":
    main()

