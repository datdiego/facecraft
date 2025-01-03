# 3D Head Reconstruction Project

## Overview
This project reconstructs a 3D volumetric representation of a human head using landmarks extracted from a video. It processes the video to aggregate facial landmarks, extrapolates missing points for the back of the head, and generates a volumetric mesh suitable for visualization or further applications.

## Features
- Extracts 3D facial landmarks from video frames using MediaPipe.
- Aligns and combines landmarks from multiple frames to handle head rotation.
- Adds synthetic points to approximate the back of the head and occluded areas.
- Generates a volumetric 3D mesh of the head.
- Exports the reconstructed head as an `.obj` file for use in 3D modeling software.

## Dependencies
Ensure you have the following Python libraries installed:
```bash
pip install mediapipe opencv-python numpy open3d scipy sklearn
```

## Pipeline
### 1. Extract Landmarks from Video
The script extracts 3D landmarks from each frame of the video using MediaPipe Face Mesh. These landmarks are saved into a JSON file.

### 2. Align and Combine Landmarks
Aggregates landmarks from all frames, aligns them to a consistent reference frame, and removes duplicates using clustering techniques.

### 3. Add Synthetic Points
Generates synthetic points to approximate the back of the head and occluded areas to complete the volumetric representation.

### 4. Generate 3D Mesh
Creates a convex hull from the aggregated points and saves the result as a `.obj` file for visualization.

## File Structure
```
project-root/
|-- sample_video.mp4        # Input video file
|-- combined_landmarks.json # JSON file with extracted landmarks
|-- reconstructed_head.obj  # Output 3D head model
|-- main.py                 # Main pipeline script
|-- README.md               # Project documentation
```

## Usage
### Step 1: Run the Pipeline
1. Place your video file (e.g., `sample_video.mp4`) in the project directory.
2. Execute the following script to run the pipeline:
   ```bash
   python main.py
   ```

### Step 2: Output Files
- **Landmarks JSON:** A file named `combined_landmarks.json` will contain the aggregated landmarks.
- **3D Head Model:** The reconstructed head will be saved as `reconstructed_head.obj`.

### Step 3: Visualize the Output
- Open the `.obj` file in 3D modeling software like Blender, MeshLab, or Open3D to inspect the reconstructed head.

## Next Steps
- **Enhance Missing Regions:** Improve synthetic point generation for more accurate reconstruction of occluded areas.
- **Apply Textures:** Use original video frames to map textures onto the 3D mesh.
- **Refine Alignment:** Use more robust methods like ICP (Iterative Closest Point) for precise alignment of landmarks across frames.

## Acknowledgments
This project utilizes:
- [MediaPipe Face Mesh](https://mediapipe.dev/) for facial landmark extraction.
- [Open3D](http://www.open3d.org/) for 3D mesh generation and manipulation.
- [Scipy](https://scipy.org/) for Delaunay triangulation and convex hull computation.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

