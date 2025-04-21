import sys
import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QSlider, QLabel
from PySide6.QtCore import Qt, QTimer

num_points = 200
freq = 2
inc = 2 * np.pi / num_points
x_start = 0
x_stop = 4 * np.pi

x = np.linspace(x_start, x_stop, num_points)
y1 = np.sin(freq * x)
y2 = np.sin(freq * x + 2 / 3 * np.pi)
y3 = np.sin(freq * x + 4 / 3 * np.pi)


def update_plot():
    global x_start, x_stop, x, y1, y2, y3
    x_start += inc
    x_stop += inc
    x = np.linspace(x_start, x_stop, num_points)
    y1 = np.sin(freq * x)
    y2 = np.sin(freq * x + 2 / 3 * np.pi)
    y3 = np.sin(freq * x + 4 / 3 * np.pi)
    sin1.setData(x, y1)
    sin2.setData(x, y2)
    sin3.setData(x, y3)


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

graph.setYRange(-1.25, 1.25)
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
