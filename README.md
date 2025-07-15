# 🌉 Street Object Detection and GeoMapping App

This project is a smart object detection system that identifies **buildings, doors, and windows** from **panoramic street images** and maps them to **accurate real-world coordinates** using camera metadata.

Built with:

* 🧠 [Roboflow](https://roboflow.com/) for object detection
* 🖥️ [Streamlit](https://streamlit.io/) for the web interface
* 🌍 [GeoPandas](https://geopandas.org/) for exporting GeoJSON
* 📷 Camera metadata (pitch, heading, GPS) to calculate real UTM positions

---

## 🚀 Features

* ✅ Detects buildings, doors, windows from street view images
* ✅ Displays bounding boxes with confidence scores
* ✅ Calculates approximate **real-world locations** (UTM projection)
* ✅ Exports results as downloadable **GeoJSON**
* ✅ Supports multiple detection models (e.g., precision 60%+ version)
* ✅ Visual and interactive web interface with Streamlit

---

## 📷 Demo & Screenshots

Below are some screenshots from the app showcasing detections and GeoJSON output:

### Main Detection Interface

![Detection Interface](https://github.com/ashehta700/street-object-detection/blob/main/screeen1.jpg)


### Output of Model Detection on Building and Select the version of Model and Download the geojson file

![Download & Model Selection](https://github.com/ashehta700/street-object-detection/blob/main/screen2.jpg)


### GeoJSON Export Example in QGIS

![GeoJSON in QGIS](https://github.com/ashehta700/street-object-detection/blob/main/screen3.jpg)

---

🎥 **Watch the demo video on YouTube:**
[![YouTube Demo]](https://www.youtube.com/watch?v=ufp4L9oTiP8)

Or click here to watch:
[https://youtu.be/YOUR\_YOUTUBE\_VIDEO\_ID](https://www.youtube.com/watch?v=ufp4L9oTiP8)

---

## 🛠️ How to Run

1. **Clone the repository**

```bash
git clone https://github.com/ahmedshehta/street-object-detection.git
cd street-object-detection
```

2. **Install required packages**

```bash
pip install -r requirements.txt
```

3. **Place your camera metadata CSV**

Create a file named `image_metadata.csv` with the following format:

```csv
image_name,timestamp,cam_x,cam_y,cam_z,heading,pitch,roll
Image001.jpg,1746800048,234528.817,2016450.6,2266.498,-103.176,-86.824,-18.445
```

4. **Run the app**

```bash
streamlit run app.py
```

5. **Upload your panoramic images via the web interface**

Then download the generated GeoJSON files for GIS use.

---

## 📁 Project Structure

```
street-object-detection/
│
├── app.py                  # Main Streamlit app code
├── image_metadata.csv      # Camera metadata CSV file (must be added by user)
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── LICENSE                 # MIT License file
└── screenshots/            # Folder for screenshot images
```

---

## 🧠 Models

Two Roboflow models are supported:

* **Model 1:** `x1-ve1ly-d7yt7/3` (default)
* **Model 2:** `x1-ve1ly-d7yt7/4` (higher precision)

You can switch between models in the UI or change the model ID in the code to compare performance.

---

## 🗚️ Output Example

Each detected building is exported as a polygon with attributes like:

* Confidence
* Number of windows
* Number of doors

The output is in **GeoJSON format**, and can be opened in GIS tools like **QGIS**, **Mapbox**, or **Leaflet**.

---

## 📢 Contact

**Ahmed Shehta**
📧 Email: [ashehta700@gmail.com](mailto:ashehta700@gmail.com)
🔗 [LinkedIn](https://www.linkedin.com/in/ahmed-shehta)
🔗 [Website](https://www.ahmed-shehta.netlify.app)

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](https://www.ahmed-shehta.netlify.app) file for details.
