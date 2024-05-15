Sure, here's a comprehensive README file for the real-time color detection project using Tkinter and OpenCV.

---

# Real-Time Color Detection

This project is a real-time color detection application using Python, OpenCV, and Tkinter. The application captures video from your webcam and detects specified colors in real-time. Users can dynamically adjust HSV values for accurate color detection.

## Features

- **Real-Time Detection**: Captures and processes video in real-time.
- **Color Selection**: Allows users to select up to two colors for detection.
- **Dynamic HSV Adjustment**: Users can adjust HSV ranges for selected colors in real-time using sliders.
- **Interactive UI**: Built with Tkinter for a user-friendly interface.

## Prerequisites

Before running this project, ensure you have the following libraries installed:

```bash
pip install opencv-python numpy
```

## Usage

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/yourusername/real-time-color-detection.git
    cd real-time-color-detection
    ```

2. **Run the Script**:

    ```bash
    python color_detection_tkinter.py
    ```

3. **Select Colors**:
    - A Tkinter window will open where you can select up to two colors for detection.
    - Click "Start Detection" after making your selection.

4. **Adjust HSV Values**:
    - Another Tkinter window will open with sliders to adjust the HSV values for the selected colors.
    - Adjust the sliders to fine-tune the color detection.

5. **View Detection**:
    - The detection results will be displayed in real-time in an OpenCV window.
    - Press 'q' to exit the application.

## Code Overview

### Main Script

The main script (`color_detection_tkinter.py`) consists of the following sections:

- **Imports and Color Definitions**:
    ```python
    import cv2
    import numpy as np
    import tkinter as tk
    from tkinter import ttk
    ```

- **Color Ranges**:
    - Define HSV ranges for different colors.
    ```python
    colors = {
        "Red": ([136, 87, 111], [180, 255, 255], (0, 0, 255)),
        "Green": ([25, 52, 72], [102, 255, 255], (0, 255, 0)),
        "Blue": ([94, 80, 2], [120, 255, 255], (255, 0, 0)),
        "Yellow": ([22, 93, 0], [45, 255, 255], (0, 255, 217)),
        "Orange": ([10, 100, 20], [25, 255, 255], (0, 165, 255)),
        "Purple": ([130, 50, 50], [160, 255, 255], (128, 0, 128)),
        "Pink": ([160, 100, 100], [180, 255, 255], (147, 20, 255))
    }
    ```

- **Color Selection UI**:
    - Tkinter UI for selecting colors to detect.
    ```python
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
    ```

- **HSV Adjustment UI**:
    - Tkinter UI for adjusting HSV values dynamically.
    ```python
    def update_hsv(color_name):
        global colors
        lower_h = hsv_scales[color_name]['lower_h'].get()
        lower_s = hsv_scales[color_name]['lower_s'].get()
        lower_v = hsv_scales[color_name]['lower_v'].get()
        upper_h = hsv_scales[color_name]['upper_h'].get()
        upper_s = hsv_scales[color_name]['upper_s'].get()
        upper_v = hsv_scales[color_name]['upper_v'].get()
        colors[color_name] = ([lower_h, lower_s, lower_v], [upper_h, upper_s, upper_v], colors[color_name][2])
    ```

- **Real-Time Detection**:
    - OpenCV video capture and color detection logic.
    ```python
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
    ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the MIT file for details.

## Contact

For any questions or feedback, please contact darshananand004@gmail.com.

---

This README provides a comprehensive overview of the project, including setup instructions, usage, and code overview. You can customize the contact information and repository URL as needed.
