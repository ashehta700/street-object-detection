# 🏙️ Street Object Detection and GeoMapping App

This project is a smart object detection system that identifies **buildings, doors, and windows** from **panoramic street images** and maps them to **accurate real-world coordinates** using camera metadata.

Built with:  
- 🧠 [Roboflow](https://roboflow.com/) for object detection  
- 🖥️ [Streamlit](https://streamlit.io/) for the web interface  
- 🌍 [GeoPandas](https://geopandas.org/) for exporting GeoJSON  
- 📷 Camera metadata (pitch, heading, GPS) to calculate real UTM positions  

---

## 🚀 Features

- ✅ Detects buildings, doors, windows from street view images  
- ✅ Displays bounding boxes with confidence scores  
- ✅ Calculates approximate **real-world locations** (UTM projection)  
- ✅ Exports results as downloadable **GeoJSON**  
- ✅ Supports multiple detection models (e.g., precision 60%+ version)  
- ✅ Visual and interactive web interface with Streamlit  

---

## 📷 Demo & Screenshots

Below are some screenshots from the app showcasing detections and GeoJSON output:

### Main Detection Interface  
![Detection Interface](screenshots/detection_interface.png)

### GeoJSON Export Example in QGIS  
![GeoJSON in QGIS](screenshots/geojson_qgis.png)

### Download Button & Model Selection UI  
![Download & Model Selection](screenshots/download_model_ui.png)

---

🎥 **Watch the demo video on YouTube:**  
[![YouTube Demo](screenshots/youtube_thumbnail.png)](https://youtu.be/YOUR_YOUTUBE_VIDEO_ID)

Or click here to watch:  
https://youtu.be/YOUR_YOUTUBE_VIDEO_ID

---

## 🛠️ How to Run

1. **Clone the repository**

```bash
git clone https://github.com/ahmedshehta/street-object-detection.git
cd street-object-detection
```

2. **Install required packages**

pip install -r requirements.txt


3. **Place your camera metadata CSV**

Add your image_metadata.csv file with columns:
image_name,timestamp,cam_x,cam_y,cam_z,heading,pitch,roll
Image001.jpg,1746800048,234528.817,2016450.6,2266.498,-103.176,-86.824,-18.445


4. **Run the app**

streamlit run app.py


4. **Upload your panoramic images via the web interface, then download the generated GeoJSON files for GIS use**

street-object-detection/
│
├── app.py                  # Main Streamlit app code
├── image_metadata.csv      # Camera metadata CSV file (must be added by user)
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── LICENSE                 # MIT License file
└── screenshots/            # Folder for screenshot images



.** Models **

Two Roboflow models are supported:

Model 1: x1-ve1ly-d7yt7/3 (default)

Model 2: x1-ve1ly-d7yt7/4 (higher precision)

You can switch models in the UI or code to test detection performance.


🗺️ Output Example
Each detected building is exported as a polygon with attributes like confidence, window count, door count, etc. This GeoJSON can be opened in GIS software such as QGIS, Mapbox, or Leaflet.


📫 Contact
Ahmed Shehta
LinkedIn
Email: ashehta700@gmail.com


📄 License
This project is licensed under the MIT License — see the LICENSE file for details.