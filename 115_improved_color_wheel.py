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
    QHBoxLayout,
)
from PySide6.QtCore import Qt, QTimer

DELAY_MS = 25  # Delay in milliseconds
IP = "192.168.1.92"


client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_sock.settimeout(DELAY_MS / 1000)  # Set timeout for socket operations
server_address = (IP, 54321)


num_points = 200
freq = 2

# Amplitude and phase shifts
A = 255 / 2  # 255 / 2
offset = A


class ColorPlotsController:
    def __init__(self, num_points, freq, A, offset, verbose=False):
        self.num_points = num_points
        self.freq = freq
        self.x_start = 0
        self.x_stop = 4 * np.pi
        self.inc = 2 * np.pi / self.num_points
        self.A = A
        self.offset = offset
        self.phase_R = 0
        self.phase_G = 2 / 3 * np.pi
        self.phase_B = 4 / 3 * np.pi
        self.chase_mode = False
        self.verbose = verbose
        self.kR = 1
        self.kG = 1
        self.kB = 1

    def update_points(self):
        self.x_start += self.inc
        self.x_stop += self.inc
        self.x = np.linspace(self.x_start, self.x_stop, self.num_points)
        self.red = self.kR * (
            self.A * np.sin(self.freq * self.x + self.phase_R) + self.offset
        )
        self.green = self.kG * (
            self.A * np.sin(self.freq * self.x + self.phase_G) + self.offset
        )
        self.blue = self.kB * (
            self.A * np.sin(self.freq * self.x + self.phase_B) + self.offset
        )

    def update_phase(self):
        if self.chase_mode:
            self.phase_G += 0.015
            self.phase_B += 0.03 * self.freq

        if self.phase_G > 2 * np.pi:
            self.phase_G -= 2 * np.pi
        if self.phase_B > 2 * np.pi:
            self.phase_B -= 2 * np.pi

    def update_plot(self):
        self.update_phase()
        self.update_points()
        sin_R.setData(self.x, self.red)
        sin_G.setData(self.x, self.green)
        sin_B.setData(self.x, self.blue)
        self.send_color()

    def send_color(self):
        my_color = f"{int(self.red[-1])},{int(self.green[-1])},{int(self.blue[-1])}"
        try:
            client_sock.sendto(my_color.encode(), server_address)
            data, addr = client_sock.recvfrom(1024)
            if self.verbose:
                print(f"received data: {data.decode()}")
        except socket.timeout:
            if self.verbose:
                print("Socket timeout, no response from server")
        except Exception as e:
            print(f"Error: {e}")

    def update_freq(self, val):
        self.freq = val / 10
        slider_label.setText(f"Frequency: {self.freq} Hz")

    def update_weights(self, val):
        for k, slider in zip([self.kR, self.kG, self.kB], sliders):
            k = slider.value() / 100
            if not self.verbose:
                print(f"{slider.objectName()} value: {k}")

        print(self.kR, self.kG, self.kB, "\n")

        # kR = slider_r.value() / 100
        # self.kG = slider_g.value() / 100
        # self.kB = slider_b.value() / 100

    def toggle_chase(self, state):
        if state:
            self.chase_mode = True
            print("chase mode enabled")
        else:
            self.chase_mode = False
            print("chase mode disabled")

    def reset_phases(self):
        self.phase_R = 0
        self.phase_G = 2 / 3 * np.pi
        self.phase_B = 4 / 3 * np.pi
        toggle_chase_chkbox.setChecked(False)
        print("phases reset:", not self.chase_mode)


# initialize plot controller object
plot_controller = ColorPlotsController(num_points, freq, A, offset)

# Initialize PyQtGraph and create the GUI
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Sine waves")
window.setGeometry(100, 100, 800, 600)
main_layout = QHBoxLayout(window)
main_layout.setContentsMargins(5, 5, 5, 5)
left_layout = QVBoxLayout(window)

slider_label = QLabel("Frequency: 1 Hz")
left_layout.addWidget(slider_label)

slider_f = QSlider(Qt.Horizontal)
slider_f.setMinimum(1)
slider_f.setMaximum(40)
slider_f.setValue(10)
slider_f.valueChanged.connect(plot_controller.update_freq)
left_layout.addWidget(slider_f)

graph = pg.PlotWidget()
left_layout.addWidget(graph)
graph.setYRange(-1.25 * A + offset, 1.25 * A + offset)
graph.showGrid(True, True)

sin_R = graph.plot([0], [0], pen=pg.mkPen("r", width=3))
sin_G = graph.plot([0], [0], pen=pg.mkPen("g", width=3))
sin_B = graph.plot([0], [0], pen=pg.mkPen("b", width=3))

toggle_chase_chkbox = QCheckBox("Chase Mode")
toggle_chase_chkbox.stateChanged.connect(plot_controller.toggle_chase)
left_layout.addWidget(toggle_chase_chkbox)

rst_button = QPushButton("Reset")
rst_button.setMaximumWidth(100)
rst_button.clicked.connect(plot_controller.reset_phases)
left_layout.addWidget(rst_button)

timer = QTimer()
timer.timeout.connect(plot_controller.update_plot)
timer.start(DELAY_MS)


right_layout = QVBoxLayout(window)
right_layout.setContentsMargins(5, 10, 5, 50)

header_layout = QHBoxLayout(window)
sliders_layout = QHBoxLayout(window)
sliders_layout.setContentsMargins(0, 15, 0, 0)


sliders = []
for color, label in zip(["red", "green", "blue"], ["  Red", "Green", " Blue"]):
    label_widget = QLabel(label)
    label_widget.setStyleSheet(f"color: {color}; font-size: 15px;")
    header_layout.addWidget(label_widget)

    slider = QSlider(Qt.Vertical)
    sliders.append(slider)
    slider.setMinimum(0)
    slider.setMaximum(100)
    slider.setValue(100)
    slider.setMinimumWidth(50)
    slider.setObjectName("slider_" + color)
    slider.valueChanged.connect(plot_controller.update_weights)
    sliders_layout.addWidget(slider)


# slider_r = QSlider(Qt.Vertical)
# slider_r.setMinimum(0)
# slider_r.setMaximum(100)
# slider_r.setValue(100)
# slider_r.setMinimumWidth(50)
# slider_r.valueChanged.connect(plot_controller.update_weights)
# slider_r


# slider_g = QSlider(Qt.Vertical)
# slider_g.setMinimum(0)
# slider_g.setMaximum(100)
# slider_g.setValue(100)
# slider_g.setMinimumWidth(50)
# slider_g.valueChanged.connect(plot_controller.update_weights)

# slider_b = QSlider(Qt.Vertical)
# slider_b.setMinimum(0)
# slider_b.setMaximum(100)
# slider_b.setValue(100)
# slider_b.setMinimumWidth(50)
# slider_b.valueChanged.connect(plot_controller.update_weights)

# sliders_layout.addWidget(slider_r)
# sliders_layout.addWidget(slider_g)
# sliders_layout.addWidget(slider_b)

right_layout.addLayout(header_layout)
right_layout.addLayout(sliders_layout)

main_layout.addLayout(left_layout)
main_layout.addLayout(right_layout)

window.setLayout(main_layout)
window.show()
sys.exit(app.exec())
