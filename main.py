#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main script to generate and visualize a complex point cloud scene.
"""
import numpy as np
from pointcloud_data import PointCloudData
from simple_opengl_viewer import Simple3DViewer
import generate_point_cloud  # Ensure this is executed to create the data

def main():
    # Step 1: Generate and save the complex point cloud data
    generate_point_cloud.main()

    # Step 2: Load the generated point cloud data
    pc = PointCloudData("complex_pointcloud.bin", mode='r+')
    all_points = pc.get_points()
    print(f"Loaded {len(all_points)} points from 'complex_pointcloud.bin'.")

    # Step 3: Initialize the viewer and load points
    viewer = Simple3DViewer(width=1280, height=720, title="Complex Point Cloud Viewer")
    viewer.load_points(all_points)

    # Step 4: Run the viewer
    viewer.run()

    # Step 5: Clean up
    pc.close()

if __name__ == "__main__":
    main()

