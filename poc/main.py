import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import open3d as o3d

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)

# Path to the input image
image_path = "sample_image.png"  # Replace with your image file

# Step 1: Extract Landmarks from Image
def extract_landmarks_from_image(image_path):
    # Load the image
    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image with MediaPipe
    results = face_mesh.process(rgb_image)
    if results.multi_face_landmarks:
        # Extract landmarks from the first detected face
        landmarks = [(lm.x, lm.y, lm.z) for lm in results.multi_face_landmarks[0].landmark]
        return np.array(landmarks), image
    else:
        print("No landmarks detected.")
        return None, image

# Step 2: Generate 2D Visualization of Landmarks
def save_2d_landmarks_image(landmarks, image, output_file):
    # Convert landmarks to pixel coordinates
    h, w, _ = image.shape
    pixel_landmarks = [(int(lm[0] * w), int(lm[1] * h)) for lm in landmarks]

    # Plot the image with landmarks
    plt.figure(figsize=(8, 8))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    for x, y in pixel_landmarks:
        plt.scatter(x, y, c='red', s=10)
    plt.title("2D Landmarks - Front Facing")
    plt.axis("off")
    plt.savefig(output_file)
    plt.close()
    print(f"2D landmarks image saved to {output_file}")

# Step 3: Generate 3D Mesh
def generate_3d_mesh(landmarks, output_file):
    # Flip y-axis and normalize landmarks
    landmarks[:, 1] = 1 - landmarks[:, 1]  # Flip y-axis
    center = np.mean(landmarks, axis=0)  # Center points
    landmarks -= center

    # Perform Delaunay triangulation
    tri = Delaunay(landmarks[:, :2])  # Use x, y for triangulation

    # Create Open3D mesh
    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(landmarks)
    mesh.triangles = o3d.utility.Vector3iVector(tri.simplices)
    mesh.compute_vertex_normals()

    # Save the mesh
    o3d.io.write_triangle_mesh(output_file, mesh)
    print(f"3D mesh saved to {output_file}")

# Run the pipeline
landmarks, original_image = extract_landmarks_from_image(image_path)
if landmarks is not None:
    # Save 2D landmarks image
    save_2d_landmarks_image(landmarks, original_image, "landmarks_image.jpg")
    # Generate 3D mesh
    generate_3d_mesh(landmarks, "face_mesh.obj")
else:
    print("Failed to generate landmarks.")
