import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk

# Define color ranges for different colors
colors = {
    "Red": ([136, 87, 111], [180, 255, 255], (0, 0, 255)),
    "Green": ([25, 52, 72], [102, 255, 255], (0, 255, 0)),
    "Blue": ([94, 80, 2], [120, 255, 255], (255, 0, 0)),
    "Yellow": ([22, 93, 0], [45, 255, 255], (0, 255, 217)),
    "Orange": ([10, 100, 20], [25, 255, 255], (0, 165, 255)),
    "Purple": ([130, 50, 50], [160, 255, 255], (128, 0, 128)),
    "Pink": ([160, 100, 100], [180, 255, 255], (147, 20, 255))
}

selected_colors = []

def select_colors():
    global selected_colors
    selected_colors = [color for color, var in color_vars.items() if var.get()]
    if not selected_colors:
        tk.messagebox.showerror("Error", "Please select at least one color to detect.")
        return
    if len(selected_colors) > 2:
        tk.messagebox.showerror("Error", "Please select no more than two colors.")
        return
    root.destroy()

def update_hsv(color_name):
    global colors
    lower_h = hsv_scales[color_name]['lower_h'].get()
    lower_s = hsv_scales[color_name]['lower_s'].get()
    lower_v = hsv_scales[color_name]['lower_v'].get()
    upper_h = hsv_scales[color_name]['upper_h'].get()
    upper_s = hsv_scales[color_name]['upper_s'].get()
    upper_v = hsv_scales[color_name]['upper_v'].get()
    colors[color_name] = ([lower_h, lower_s, lower_v], [upper_h, upper_s, upper_v], colors[color_name][2])

# Create the main window
root = tk.Tk()
root.title("Color Detection Settings")

# Create and pack the widgets
tk.Label(root, text="Select Colors to Detect (Up to 2):", font=("Helvetica", 14)).pack(pady=10)
color_vars = {color: tk.BooleanVar() for color in colors}
for color, var in color_vars.items():
    tk.Checkbutton(root, text=color, variable=var, font=("Helvetica", 12)).pack(anchor=tk.W)

ttk.Button(root, text="Start Detection", command=select_colors).pack(pady=20)
root.mainloop()

if not selected_colors:
    exit()

# Create a new Tkinter window for HSV adjustment
hsv_window = tk.Tk()
hsv_window.title("HSV Adjustments")

hsv_scales = {}
for color in selected_colors:
    frame = ttk.LabelFrame(hsv_window, text=color, padding=(10, 5))
    frame.pack(padx=10, pady=5, fill="x")
    scales = {}
    for (scale_name, from_, to, initial) in [
        ('lower_h', 0, 180, colors[color][0][0]),
        ('lower_s', 0, 255, colors[color][0][1]),
        ('lower_v', 0, 255, colors[color][0][2]),
        ('upper_h', 0, 180, colors[color][1][0]),
        ('upper_s', 0, 255, colors[color][1][1]),
        ('upper_v', 0, 255, colors[color][1][2])
    ]:
        scale = ttk.Scale(frame, from_=from_, to=to, orient='horizontal', length=300)
        scale.set(initial)
        scale.pack(fill="x", padx=10, pady=2)
        ttk.Label(frame, text=scale_name).pack()
        scales[scale_name] = scale
    hsv_scales[color] = scales

def update_all_hsv():
    for color in selected_colors:
        update_hsv(color)

ttk.Button(hsv_window, text="Update HSV Values", command=update_all_hsv).pack(pady=20)

# Start capturing video through webcam
cap = cv2.VideoCapture(0)

def create_color_mask(hsv_frame, lower_bound, upper_bound):
    mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)
    kernal = np.ones((5, 5), "uint8")
    mask = cv2.dilate(mask, kernal)
    return mask

def detect_and_draw_contours(image_frame, mask, color_name, color_bgr):
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 300:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(image_frame, (x, y), (x + w, y + h), color_bgr, 2)
            cv2.putText(image_frame, f"{color_name} Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color_bgr)

while True:
    _, image_frame = cap.read()
    hsv_frame = cv2.cvtColor(image_frame, cv2.COLOR_BGR2HSV)

    for color_name in selected_colors:
        lower, upper, bgr = colors[color_name]
        lower_bound = np.array(lower, np.uint8)
        upper_bound = np.array(upper, np.uint8)
        mask = create_color_mask(hsv_frame, lower_bound, upper_bound)
        detect_and_draw_contours(image_frame, mask, color_name, bgr)

    cv2.imshow("Multiple Color Detection in Real-Time", image_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
hsv_window.destroy()
