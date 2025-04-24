import sys
import numpy as np
import pyqtgraph as pg
import socket
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QSlider, QLabel
from PySide6.QtCore import Qt, QTimer

client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ("192.168.1.92", 54321)


num_points = 200
freq = 2
inc = 2 * np.pi / num_points
x_start = 0
x_stop = 4 * np.pi

count = 0
INC_R = 1
INC_G = 2
A = 255 / 2
m = 1

x = np.linspace(x_start, x_stop, num_points)
y1 = A * (np.sin(freq * x) + m)
y2 = A * (np.sin(freq * x + 2 / 3 * np.pi) + m)
y3 = A * (np.sin(freq * x + 4 / 3 * np.pi) + m)


def update_plot():
    global x_start, x_stop, x, y1, y2, y3, count
    x_start += inc
    x_stop += inc
    x = np.linspace(x_start, x_stop, num_points)
    y1 = A * (np.sin(freq * x + count * INC_R / 100 * freq) + m)
    y2 = A * (np.sin(freq * x + 2 / 3 * np.pi + count * INC_G / 100 * freq) + m)
    y3 = A * (np.sin(freq * x + 4 / 3 * np.pi) + m)
    sin1.setData(x, y1)
    sin2.setData(x, y2)
    sin3.setData(x, y3)
    my_color = f"{int(y1[-1])},{int(y2[-1])},{int(y3[-1])}"
    client_sock.sendto(my_color.encode(), server_address)
    data, addr = client_sock.recvfrom(1024)
    print(f"received data: {data.decode()}")

    count += 1


def update_freq(val):
    global freq
    freq = val / 10
    slider_label.setText(f"Frequency: {freq} Hz")


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

graph.setYRange(-0.25 * A, 2.25 * A)
graph.showGrid(True, True)

sin1 = graph.plot(x, y1, pen=pg.mkPen("r", width=3))
sin2 = graph.plot(x, y2, pen=pg.mkPen("g", width=3))
sin3 = graph.plot(x, y3, pen=pg.mkPen("b", width=3))


timer = QTimer()
timer.timeout.connect(update_plot)
timer.start(50)

window.setLayout(layout)
window.show()
sys.exit(app.exec())
