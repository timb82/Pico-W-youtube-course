import sys
import numpy as np
import pyqtgraph as pg
import socket
from PySide6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QMainWindow,
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

    def update_weights(self, sliders, val):
        self.kR = sliders["red"].value() / 100
        self.kG = sliders["green"].value() / 100
        self.kB = sliders["blue"].value() / 100

        if self.verbose:
            print(self.kR, self.kG, self.kB, "\n")

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


class MainWindow(QMainWindow):
    def __init__(self, ctrl, delay_ms=DELAY_MS):
        super().__init__()
        self.setWindowTitle("Sine Waves")
        self.setGeometry(100, 100, 800, 600)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5)

        self.left_layout = QVBoxLayout(self)
        self.slider_label = QLabel("Frequency: 1 Hz")
        self.left_layout.addWidget(self.slider_label)

        self.slider_f = QSlider(Qt.Horizontal)
        self.slider_f.setMinimum(1)
        self.slider_f.setMaximum(40)
        self.slider_f.setValue(10)
        self.slider_f.valueChanged.connect(ctrl.update_freq)
        self.left_layout.addWidget(self.slider_f)

        self.graph = pg.PlotWidget()
        self.left_layout.addWidget(self.graph)
        self.graph.setYRange(-1.25 * ctrl.A + ctrl.offset, 1.25 * ctrl.A + ctrl.offset)
        self.graph.showGrid(True, True)

        self.sin_R = self.graph.plot([0], [0], pen=pg.mkPen("r", width=3))
        self.sin_G = self.graph.plot([0], [0], pen=pg.mkPen("g", width=3))
        self.sin_B = self.graph.plot([0], [0], pen=pg.mkPen("b", width=3))

        self.toggle_chase_chkbox = QCheckBox("Chase Mode")
        self.toggle_chase_chkbox.stateChanged.connect(ctrl.toggle_chase)
        self.left_layout.addWidget(self.toggle_chase_chkbox)

        self.rst_button = QPushButton("Reset")
        self.rst_button.setMaximumWidth(100)
        self.rst_button.clicked.connect(ctrl.reset_phases)
        self.left_layout.addWidget(self.rst_button)

        self.timer = QTimer()
        self.timer.timeout.connect(ctrl.update_plot)
        self.timer.start(delay_ms)

        self.right_layout = QVBoxLayout(self)
        self.right_layout.setContentsMargins(5, 10, 5, 50)

        self.header_layout = QHBoxLayout(self)
        self.sliders_layout = QHBoxLayout(self)
        self.sliders_layout.setContentsMargins(0, 15, 0, 0)

        self.sliders = {}

    for color, label in zip(["red", "green", "blue"], ["  Red", "Green", " Blue"]):
        label_widget = QLabel(label)
        label_widget.setStyleSheet(f"color: {color}; font-size: 15px;")
        header_layout.addWidget(label_widget)

        sliders[color] = QSlider(Qt.Vertical)
        sliders[color].setMinimum(0)
        sliders[color].setMaximum(100)
        sliders[color].setValue(100)
        sliders[color].setMinimumWidth(50)
        sliders[color].setObjectName("slider_" + color)
        sliders[color].valueChanged.connect(plot_controller.update_weights)
        sliders[color].setStyleSheet(
            f"QSlider::handle:vertical {{background: {color};}}"
        )
        sliders_layout.addWidget(sliders[color])


right_layout.addLayout(header_layout)
right_layout.addLayout(sliders_layout)

main_layout.addLayout(left_layout)
main_layout.addLayout(right_layout)

window.setLayout(main_layout)
window.show()
sys.exit(app.exec())
