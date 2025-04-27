import sys
import pyqtgraph as pg
import numpy as np
import socket
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QWidget,
    QVBoxLayout,
    QLabel,
    QSlider,
    QHBoxLayout,
    QPushButton,
)

DELAY_MS = 80  # Delay in milliseconds
IP = "192.168.1.92"

client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_sock.settimeout(DELAY_MS / 1000)  # Set timeout for socket operations
server_address = (IP, 54321)


class MainWindow(QWidget):
    def __init__(self, A=255 / 2, freq=2, num_points=200, verbose=False):
        super().__init__()
        self.A = A
        self.freq = freq
        self.offset = A
        self.phase_R = 0
        self.phase_G = 2 / 3 * np.pi
        self.phase_B = 4 / 3 * np.pi
        self.kR = 1
        self.kG = 1
        self.kB = 1
        self.verbose = verbose
        self.num_points = num_points
        self.x_start = 0
        self.x_stop = 4 * np.pi
        self.inc = 2 * np.pi / self.num_points
        self.chase_mode = False
        delay_ms = DELAY_MS

        self.setWindowTitle("Sine Waves")
        self.setGeometry(100, 100, 800, 600)
        self.setContentsMargins(5, 5, 5, 5)

        h = QHBoxLayout(self)
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(5, 5, 5, 5)
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(5, 10, 5, 50)

        h.addLayout(left_layout)
        h.addLayout(right_layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(delay_ms)

        # LEFT SIDE LAYOUT
        self.slider_label = QLabel("Frequency: 1 Hz")
        left_layout.addWidget(self.slider_label)
        self.slider_f = QSlider(Qt.Horizontal)
        self.slider_f.setMinimum(1)
        self.slider_f.setMaximum(40)
        self.slider_f.setValue(self.freq * 10)
        self.slider_f.valueChanged.connect(self.update_freq)
        left_layout.addWidget(self.slider_f)

        self.graph = pg.PlotWidget()
        left_layout.addWidget(self.graph)
        range = (-1.25 * self.A + self.offset, 1.25 * self.A + self.offset)
        self.graph.setYRange(*range)
        self.graph.showGrid(True, True)

        self.sin_R = self.graph.plot([0], [0], pen=pg.mkPen("r", width=3))
        self.sin_G = self.graph.plot([0], [0], pen=pg.mkPen("g", width=3))
        self.sin_B = self.graph.plot([0], [0], pen=pg.mkPen("b", width=3))

        self.toggle_chase_chkbox = QCheckBox("Chase Mode")
        self.toggle_chase_chkbox.stateChanged.connect(self.toggle_chase)
        left_layout.addWidget(self.toggle_chase_chkbox)

        self.rst_button = QPushButton("Reset")
        self.rst_button.setMaximumWidth(100)
        self.rst_button.clicked.connect(self.reset_phases)
        left_layout.addWidget(self.rst_button)

        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(5, 5, 5, 5)
        left_layout.addLayout(footer_layout)

        self.button_bar = {}
        for btn_name in ["RGB", "Red", "Green", "Blue"]:
            self.button_bar[btn_name] = QPushButton(btn_name)
            self.button_bar[btn_name].setFixedSize(50, 40)
            footer_layout.addWidget(self.button_bar[btn_name])

        # RIGHT SIDE LAYOUT
        header_layout = QHBoxLayout(self)
        sliders_layout = QHBoxLayout(self)
        sliders_layout.setContentsMargins(0, 15, 0, 60)
        right_layout.addLayout(header_layout)
        right_layout.addLayout(sliders_layout)

        self.sliders = {}
        for color, label in zip(["red", "green", "blue"], ["  Red", "Green", " Blue"]):
            label_widget = QLabel(label)
            label_widget.setStyleSheet(f"color: {color}; font-size: 15px;")
            header_layout.addWidget(label_widget)

            self.sliders[color] = QSlider(Qt.Vertical)
            self.sliders[color].setMinimum(0)
            self.sliders[color].setMaximum(100)
            self.sliders[color].setValue(100)
            self.sliders[color].setMinimumWidth(50)
            self.sliders[color].setObjectName("slider_" + color)
            self.sliders[color].valueChanged.connect(self.update_weights)
            self.sliders[color].setStyleSheet(
                f"QSlider::handle:vertical {{background: {color};}}"
            )
            sliders_layout.addWidget(self.sliders[color])

    def update_points(self):
        self.x_start += self.inc
        self.x_stop += self.inc

        self.x = np.linspace(self.x_start, self.x_stop, self.num_points)
        self.y1 = self.A * np.sin(self.freq * self.x + self.phase_R) + self.offset
        self.y2 = self.A * np.sin(self.freq * self.x + self.phase_G) + self.offset
        self.y3 = self.A * np.sin(self.freq * self.x + self.phase_B) + self.offset

        self.my_color = QColor(self.y1[-1], self.y2[-1], self.y3[-1])

        self.y1 *= self.kR
        self.y2 *= self.kG
        self.y3 *= self.kB

    def update_phase(self):
        if self.chase_mode:
            self.phase_G += 0.02 * self.freq
            self.phase_B += 0.04 * self.freq

        if self.phase_R > 2 * np.pi:
            self.phase_R -= 2 * np.pi
        if self.phase_B > 2 * np.pi:
            self.phase_B -= 2 * np.pi
        if self.phase_G > 2 * np.pi:
            self.phase_G -= 2 * np.pi

    def update_plot(self):
        self.update_phase()
        self.update_points()
        self.sin_R.setData(self.x, self.y1)
        self.sin_G.setData(self.x, self.y2)
        self.sin_B.setData(self.x, self.y3)
        self.send_color()

    def update_freq(self, val):
        self.freq = val / 10
        self.slider_label.setText(f"Frequency: {self.freq} Hz")

    def toggle_chase(self, state):
        if state:
            self.chase_mode = True
            print("Chase mode ON")
        else:
            self.chase_mode = False
            print("Chase mode OFF")

    def reset_phases(self):
        self.phase_R = 0
        self.phase_G = 2 / 3 * np.pi
        self.phase_B = 4 / 3 * np.pi
        self.toggle_chase_chkbox.setChecked(False)
        print("phases reset")

    def update_weights(self):
        self.kR = self.sliders["red"].value() / 100
        self.kG = self.sliders["green"].value() / 100
        self.kB = self.sliders["blue"].value() / 100

    def send_color(self):
        my_color = self.my_color
        color_str = (
            f"{int(my_color.red())},{int(my_color.green())},{int(my_color.blue())}"
        )

        colors = [
            my_color,
            QColor(my_color.red(), 0, 0),
            QColor(0, my_color.green(), 0),
            QColor(0, 0, my_color.blue()),
        ]
        for btn, color in zip(self.button_bar.values(), colors):
            style_str = f"background-color: {color.name()}; border-radius: 16px; min-width: 50px; min-height: 40px; font-size: 15px; color: white;"
            btn.setStyleSheet(style_str)

        try:
            if self.verbose:
                print(f"Sending color: {color_str}")
            client_sock.sendto(color_str.encode(), server_address)
            data, addr = client_sock.recvfrom(1024)
            if self.verbose:
                print(f"received data: {data.decode()}")
        except socket.timeout:
            if self.verbose:
                print("Socket timeout, no response from server")
        except Exception as e:
            print(f"Error: {e}")


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
