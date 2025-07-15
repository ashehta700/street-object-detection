import streamlit as st
from inference_sdk import InferenceHTTPClient
import cv2, tempfile, os
from collections import defaultdict
from shapely.geometry import box, Point
import geopandas as gpd
import pandas as pd
import math

# ── CONFIG ───────────────────────────────────────────────────────────────────
MODEL_ID       = "YOUR Model ID "
API_KEY        = "Your API Key "
META_CSV       = "image_metadata.csv"      # must live next to this script
BBOX_THICKNESS = 20                        # pixels
LABEL_SCALE    = 3                         # font size (increase if you want)
INSIDE_THRESH  = 0.50                      # 50 % of area must overlap

COLOURS = {                                 # BGR
    "building":        (255,   0,   0),
    "window":          (  0, 255,   0),
    "door":            (  0, 165, 255),
    "car":             (128,   0, 128),
    "car with camera": (255,   0, 255),
}

# ── Roboflow client ──────────────────────────────────────────────────────────
CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key=API_KEY
)

# ── Load metadata CSV once ───────────────────────────────────────────────────
try:
    META_DF = pd.read_csv(META_CSV)
    META_DF.rename(columns={META_DF.columns[0]: "image_name"}, inplace=True)
except FileNotFoundError:
    st.warning(f"⚠️ Metadata file “{META_CSV}” not found – output GeoJSON will "
               "contain pixel‑space coordinates only.")
    META_DF = pd.DataFrame()

# ── Streamlit UI ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Street‑Object Detection", layout="wide")
st.title("🏙️ Street‑Object Detection")

conf_th = st.sidebar.slider("Confidence threshold", 0.05, 1.0, 0.30, 0.05)
iou_th  = st.sidebar.slider("Overlap (NMS) threshold", 0.1, 1.0, 0.45, 0.05)

uploaded = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])
if not uploaded:
    st.stop()

# ── Save to temp, run inference ──────────────────────────────────────────────
with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
    tmp.write(uploaded.read())
    img_path = tmp.name
    
    
    
# ── Helper: Choice between models  ────────────────────────────────
model_choice = st.sidebar.selectbox(
    "Choose detection model",
    options=[
        ("V3  – current",  "x1-ve1ly-d7yt7/3"),
        ("V4  – higher‑precision", "x1-ve1ly-d7yt7/4"),
        ("V7  – Street Object Detection", "streetobjectdetection/7"),
    ],
    format_func=lambda x: x[0]
)
SELECTED_MODEL_ID = model_choice[1]
    

query_model = f"{SELECTED_MODEL_ID}?confidence={conf_th}&overlap={iou_th}"
preds = CLIENT.infer(img_path, model_id=query_model)["predictions"]

# ── Load image to get size ────────────────────────────────────────────────────
img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
img_h, img_w = img.shape[:2]

counts, buildings, others = defaultdict(int), [], []

for p in preds:
    counts[p["class"]] += 1
    (buildings if p["class"] == "building" else others).append(p)

    # box coordinates for drawing on image
    x1, y1 = int(p["x"] - p["width"]/2), int(p["y"] - p["height"]/2)
    x2, y2 = int(p["x"] + p["width"]/2), int(p["y"] + p["height"]/2)
    colour = COLOURS.get(p["class"], (255, 255, 255))

    cv2.rectangle(img, (x1, y1), (x2, y2), colour, thickness=BBOX_THICKNESS)

    label = f'{p["class"]} ({p["confidence"]:.2f})'
    font = cv2.FONT_HERSHEY_SIMPLEX
    ((tw, th), _) = cv2.getTextSize(label, font, LABEL_SCALE, 2)
    y_lab = max(y1 - 15, th + 15)

    # black bg rectangle behind text
    cv2.rectangle(img,
                  (x1, y_lab - th - 12),
                  (x1 + tw + 12, y_lab),
                  (0, 0, 0), -1)
    # outline + fill text
    cv2.putText(img, label, (x1 + 6, y_lab - 4),
                font, LABEL_SCALE, (0, 0, 0), 4, cv2.LINE_AA)
    cv2.putText(img, label, (x1 + 6, y_lab - 4),
                font, LABEL_SCALE, (255, 255, 255), 2, cv2.LINE_AA)

st.image(img, caption="Detections", use_container_width=True)

# ── Object counts ────────────────────────────────────────────────────────────
st.subheader("📊 Object counts")
for cls, n in counts.items():
    st.write(f"- **{cls}**: {n}")

def point_inside(building, obj):
    bx1 = building["x"] - building["width"]/2
    by1 = building["y"] - building["height"]/2
    bx2 = building["x"] + building["width"]/2
    by2 = building["y"] + building["height"]/2
    ox, oy = obj["x"], obj["y"]
    return bx1 <= ox <= bx2 and by1 <= oy <= by2


# ── Helper: Add Ground Sider To handle the Size of building  ────────────────────────────────
# ground_w_slider = st.sidebar.slider(
#     "Ground width covered by the photo (metres)",
#     min_value=100, max_value=5000, value=800, step=50
# )








# ── Helper: Drop-in Function: Estimate Building World Location  From Angel ────────────────────────────────
def estimate_building_position(cam_x, cam_y, cam_z, heading_deg, pitch_deg):
    """
    Estimate building ground location in UTM coords using:
    - camera (x, y, z)
    - heading (0=N, 90=E)
    - pitch (looking down = –90)
    """
    angle_deg = 90 + pitch_deg
    if angle_deg <= 0:
        ground_offset = 0
    else:
        ground_offset = cam_z * math.tan(math.radians(angle_deg))

    h = math.radians(heading_deg)
    dx = ground_offset * math.sin(h)
    dy = ground_offset * math.cos(h)

    return cam_x + dx, cam_y + dy




# ── Helper: pixel to world coordinates approx ────────────────────────────────
import math


def pixel_to_world(cam_x, cam_y, heading_deg,
                   img_w, img_h, px, py,
                   ground_w_m=50):          # 🔸 fixed 50 m width
    """
    Simple linear mapping:
    - whole image width represents `ground_w_m` metres on the ground.
    - camera is assumed nearly nadir.
    """
    m_per_px = ground_w_m / img_w

    dx_px = px - img_w / 2
    dy_px = img_h / 2 - py            # +ve = forward/North

    x_cam = dx_px * m_per_px          # right/East
    y_cam = dy_px * m_per_px          # forward/North

    h = math.radians(heading_deg)
    world_dx =  x_cam * math.cos(h) + y_cam * math.sin(h)
    world_dy = -x_cam * math.sin(h) + y_cam * math.cos(h)

    return cam_x + world_dx, cam_y + world_dy






# ── Per-building stats & GeoJSON features ────────────────────────────────────
st.subheader("🏢 Per‑building stats")
features = []

# Find metadata row for this image
row = META_DF.loc[META_DF["image_name"].str.lower() == uploaded.name.lower()]
if row.empty:
    st.info("No matching metadata row – GeoJSON will contain pixel coordinates only.")
    meta_dict = None
else:
    meta_dict = row.iloc[0].to_dict()

for i, b in enumerate(buildings, 1):
    win = sum(1 for o in others if o["class"] == "Window" and point_inside(b, o))
    dor = sum(1 for o in others if o["class"] == "door"   and point_inside(b, o))
    st.write(f"**Building {i}** – 🪟 {win} windows, 🚪 {dor} doors")

    if not row.empty:
        world_x, world_y = pixel_to_world(
            meta_dict["cam_x"], meta_dict["cam_y"], meta_dict["heading"],
            img_w, img_h, b["x"], b["y"]
        )

        # 🔸 make a tiny 5 m × 5 m square
        HALF = 4        # half‑size in metres
        geom = box(world_x - HALF, world_y - HALF,
                   world_x + HALF, world_y + HALF)
    else:
        # fallback: pixel square 10×10 px
        HALF = 5
        geom = box(b["x"] - HALF, b["y"] - HALF,
                   b["x"] + HALF, b["y"] + HALF)

    feat = {
        "geometry":   geom,
        "class":      "building",
        "windows":    win,
        "doors":      dor,
        "confidence": b["confidence"],
        **meta_dict
    }

    features.append(feat)


if meta_dict:
    # Add camera location point feature in world coords
    pt = {
        "geometry": Point(meta_dict["cam_x"], meta_dict["cam_y"]),
        "class":    "camera",
        **meta_dict
    }
    features.append(pt)

# Create GeoDataFrame
gdf = gpd.GeoDataFrame(features, geometry="geometry", crs=None)

# ── Write GeoJSON safely (Windows) ───────────────────────────────────────────
fd, geo_path = tempfile.mkstemp(suffix=".geojson")
UTM36N = 32638
# Set CRS for UTM zone 36N (your cam_x, cam_y coords are in metres)
gdf.set_crs(epsg=32638, inplace=True)

# Convert to lat/lon for GeoJSON output (optional but common)
gdf = gdf.to_crs(epsg=32638)
os.close(fd)
gdf.to_file(geo_path, driver="GeoJSON")






with open(geo_path, "rb") as fh:
    st.download_button("📥 Download GeoJSON", fh,
                       file_name="detections.geojson",
                       mime="application/geo+json")

try:
    os.remove(geo_path)
except OSError:
    pass
