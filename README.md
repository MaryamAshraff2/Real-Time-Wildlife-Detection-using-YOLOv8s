# Wildlife Detection System using YOLOv8 and Streamlit

This project is a real-time wildlife detection application that uses a custom-trained YOLOv8s model to identify and classify six animal species: Bear, Zebra, Giraffe, Elephant, Lion, and Tiger. It features a Streamlit-based web interface that allows users to upload images, videos, or use a webcam for wildlife detection. This application is designed to assist in wildlife research, conservation, and education.

---

## Features

- Real-time object detection using YOLOv8s
- Custom training on Lion and Tiger datasets from Roboflow
- User-friendly interface developed with Streamlit
- Accepts image, video, and webcam input
- Outputs labeled bounding boxes for detected animals
- Detection results are saved for review
- Optimized for environments with limited computational resources

---

## Technologies Used

- YOLOv8s (Ultralytics) - lightweight and efficient object detection model
- Roboflow - dataset source for Lion and Tiger images
- Google Colab - cloud-based model training with GPU support
- Streamlit - front-end framework for interactive UI
- Python - core programming language
- Visual Studio Code - local development environment

---

## Dataset and Preprocessing

- Total Images: 951 (custom dataset for Lion and Tiger)
- Pre-trained classes included: Bear, Zebra, Giraffe, Elephant
- Total Classes: 6 (Bear, Zebra, Giraffe, Elephant, Lion, Tiger)
- Format: YOLOv8
- Preprocessing steps:
  - All images resized to 640x640 pixels
  - EXIF metadata removed for correct orientation
  - Augmentation techniques:
    - Random rotation within ±11° and 90° turns
    - Horizontal flipping with 50% probability
    - Salt-and-pepper noise added to 0.12% of pixels

---

## Model Training

- Model: YOLOv8s (`yolov8s.pt`) with 11.2 million parameters
- Training conducted on Google Colab using a T4 GPU
- Dataset Split:
  - Training: 690 images
  - Validation: 100 images
  - Testing: 190 images
- Key Hyperparameters:
  - Image Size: 640x640
  - Batch Size: 8
  - Epochs: 40
  - Device: GPU (CUDA) with CPU fallback support

---

## Deployment

The application is deployed as a web interface using Streamlit. Users can perform wildlife detection using the following input types:

- Uploaded images
- Uploaded videos
- Webcam feed

The system performs inference using a model trained on Google Colab (`best.pt`) and displays detection results with bounding boxes and class labels.

---

## Setup Instructions

### Prerequisites

- Python 3.8 or above
- pip package manager

### Installation

1. Extract the ZIP file containing the project.
2. Open a terminal or command prompt.
3. Navigate to the project directory:

   ```bash
   cd wildlife_project  # or the folder name after unzipping
   ```

4. Activate the virtual environment:

   - On Linux/Mac:

     ```bash
     source wildlife/bin/activate
     ```

   - On Windows:

     ```bash
     wildlife\Scripts\activate
     ```

5. Install the project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Launch the application:

   ```bash
   streamlit run app.py
   ```

---

## Project Structure

```
wildlife_project/
├── app.py                  # Main Streamlit application
├── detection/              # YOLOv8 model loading and inference
├── ui/                     # User interface logic and styling
├── history/                # Stored detection result files
├── wildlife/               # Python virtual environment (excluded from version control)
├── requirements.txt        # Required Python packages
└── README.md               # Project documentation
```

---

## Use Cases

- Wildlife research and behavioral documentation
- Conservation fieldwork and tracking
- Real-time monitoring in reserves and zoos
- Educational use cases for AI in environmental science

---

## Future Enhancements

- Apply model pruning or quantization techniques to further reduce model size and improve inference speed.
- Extend detection to more animal species and rare wildlife.
- Deploy the system to the cloud (e.g., AWS, GCP) for global accessibility.
- Create a mobile-friendly version of the application using Streamlit Mobile or Flutter integration.
- Use Artificial Neural Networks (ANNs) to classify animal behavior or detect specific postures (e.g., sleeping, walking, aggressive).
- Integrate object tracking to monitor individual animal movement over time in video feeds.
- Add multilingual voice support to make the app more inclusive for diverse field researchers.
- Implement geolocation tagging for detections to assist with mapping and tracking species distribution.
- Enable offline functionality using TensorFlow Lite or ONNX for field researchers in remote areas.
- Provide analytics dashboards (via Plotly, Dash, or Streamlit Charts) to visualize detection trends and history.
- Set up alert/notification systems for rare or endangered species sightings.

---

## Contact

For feedback, questions, or contributions, please contact the project maintainers or open an issue or pull request on the repository.

---
