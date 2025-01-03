import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial import ConvexHull
import open3d as o3d
import json
from sklearn.decomposition import PCA

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False)

# Step 1: Extract Landmarks from Video
def extract_landmarks_from_video(video_path):
    cap = cv2.VideoCapture(video_path)
    all_landmarks = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # End of video

        # Convert frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process frame with MediaPipe
        results = face_mesh.process(rgb_frame)
        if results.multi_face_landmarks:
            # Extract landmarks from the first detected face
            landmarks = [(lm.x, lm.y, lm.z) for lm in results.multi_face_landmarks[0].landmark]
            all_landmarks.append(landmarks)
        else:
            print("No landmarks detected for this frame.")

    cap.release()
    print(f"Extracted landmarks from {len(all_landmarks)} frames.")
    return np.array(all_landmarks)

# Step 2: Align and Combine Landmarks Across Frames
def align_and_combine_landmarks(all_landmarks):
    combined_points = []
    reference_landmarks = all_landmarks[0]  # Use the first frame as reference

    # Align each frame's landmarks to the reference
    for landmarks in all_landmarks:
        landmarks = np.array(landmarks)

        # Center landmarks using the nose (index 1)
        center = landmarks[1]
        aligned_landmarks = landmarks - center

        # Align using PCA (optional)
        pca = PCA(n_components=3)
        aligned_landmarks = pca.fit_transform(aligned_landmarks)

        combined_points.extend(aligned_landmarks)

    # Convert to NumPy array
    combined_points = np.array(combined_points)
    print(f"Combined {len(combined_points)} points from all frames.")
    return combined_points

# Step 3: Add Synthetic Points to Complete the Head
def add_synthetic_points(points):
    # Add synthetic points for the back of the head
    synthetic_points = np.random.uniform(-0.5, 0.5, (100, 3))
    synthetic_points[:, 2] -= 1.0  # Push points backward

    # Combine with the original points
    complete_points = np.vstack((points, synthetic_points))
    print(f"Added synthetic points. Total points: {len(complete_points)}.")
    return complete_points

# Step 4: Generate and Save 3D Mesh
def generate_3d_mesh(points, output_file):
    # Create a convex hull to form the mesh
    hull = ConvexHull(points)

    # Create Open3D mesh
    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(points)
    mesh.triangles = o3d.utility.Vector3iVector(hull.simplices)
    mesh.compute_vertex_normals()

    # Save the mesh
    o3d.io.write_triangle_mesh(output_file, mesh)
    print(f"3D head mesh saved to {output_file}")

# Full Pipeline Execution
video_path = "sample_video.mp4"  # Path to your video
output_mesh = "reconstructed_head.obj"  # Output file for the 3D head model

# Execute the steps
all_landmarks = extract_landmarks_from_video(video_path)
combined_points = align_and_combine_landmarks(all_landmarks)
complete_points = add_synthetic_points(combined_points)
generate_3d_mesh(complete_points, output_mesh)
