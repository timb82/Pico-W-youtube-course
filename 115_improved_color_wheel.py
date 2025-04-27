import sys
import numpy as np
import pyqtgraph as pg
import socket
from PySide6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QWidget,
    QSlider,
    QLabel,
    QCheckBox,
    QPushButton,
)
from PySide6.QtCore import Qt, QTimer

DELAY_MS = 50  # Delay in milliseconds
IP = "192.168.1.92"

client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_sock.settimeout(DELAY_MS / 1000)  # Set timeout for socket operations
server_address = (IP, 54321)


num_points = 200
freq = 2
inc = 2 * np.pi / num_points


x_start = 0
x_stop = 4 * np.pi

chase_mode = False

# Amplitude and phase shifts
A = 255 / 2  # 255 / 2
offset = A
phase_R = 0
phase_G = 2 / 3 * np.pi
phase_B = 4 / 3 * np.pi


def update_points():
    global x_start, x_stop
    x_start += inc
    x_stop += inc
    x = np.linspace(x_start, x_stop, num_points)
    y1 = A * np.sin(freq * x + phase_R) + offset
    y2 = A * np.sin(freq * x + phase_G) + offset
    y3 = A * np.sin(freq * x + phase_B) + offset
    return x, y1, y2, y3


def update_plot():
    global phase_R, phase_G, phase_B
    if chase_mode:
        phase_G += 0.02
        phase_B += 0.04 * freq

    if phase_G > 2 * np.pi:
        phase_G -= 2 * np.pi
    if phase_B > 2 * np.pi:
        phase_B -= 2 * np.pi

    print(f"phase_R: {phase_R*180/np.pi:.3f}", end="\t\t")
    print(f"phase_G: {phase_G*180/np.pi:.3f}", end="\t")
    print(f"phase_B: {phase_B*180/np.pi:.3f}")
    x, y1, y2, y3 = update_points()
    sin_R.setData(x, y1)
    sin_G.setData(x, y2)
    sin_B.setData(x, y3)
    my_color = f"{int(y1[-1])},{int(y2[-1])},{int(y3[-1])}"
    try:
        client_sock.sendto(my_color.encode(), server_address)
        data, addr = client_sock.recvfrom(1024)
        print(f"received data: {data.decode()}")
    except socket.timeout:
        # print("Socket timeout, no response from server")
        pass
    except Exception as e:
        print(f"Error: {e}")


def update_freq(val):
    global freq
    freq = val / 10
    slider_label.setText(f"Frequency: {freq} Hz")


def toggle_chase(state):
    global chase_mode
    if state:
        chase_mode = True
        print("chase mode enabled")
    else:
        chase_mode = False
        print("chase mode disabled")


def reset_phases():
    global phase_R, phase_G, phase_B, chase_mode
    phase_R = 0
    phase_G = 2 / 3 * np.pi
    phase_B = 4 / 3 * np.pi
    toggle_chase_chkbox.setChecked(False)
    # chase_mode = False
    print("phases reset:", not chase_mode)


app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Sine waves")
window.setGeometry(100, 100, 800, 600)
layout = QVBoxLayout(window)

slider_label = QLabel("Frequency: 1 Hz")
layout.addWidget(slider_label)

slider = QSlider(Qt.Horizontal)
slider.setMinimum(1)
slider.setMaximum(40)
slider.setValue(10)
slider.valueChanged.connect(update_freq)
layout.addWidget(slider)

graph = pg.PlotWidget()
layout.addWidget(graph)
graph.setYRange(-1.25 * A + offset, 1.25 * A + offset)
graph.showGrid(True, True)
toggle_chase_chkbox = QCheckBox("Chase Mode")
toggle_chase_chkbox.stateChanged.connect(toggle_chase)
layout.addWidget(toggle_chase_chkbox)

rst_button = QPushButton("Reset")
rst_button.clicked.connect(lambda: reset_phases())
layout.addWidget(rst_button)


x, y1, y2, y3 = update_points()
sin_R = graph.plot(x, y1, pen=pg.mkPen("r", width=3))
sin_G = graph.plot(x, y2, pen=pg.mkPen("g", width=3))
sin_B = graph.plot(x, y3, pen=pg.mkPen("b", width=3))

timer = QTimer()
timer.timeout.connect(update_plot)
timer.start(DELAY_MS)

window.setLayout(layout)
window.show()
sys.exit(app.exec())
