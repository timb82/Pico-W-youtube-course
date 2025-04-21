import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtWidgets import QSlider, QLabel
from PyQt5.QtCore import Qt
import time

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("My App")
window.setGeometry(100, 100, 800, 400)

wdg_box = QVBoxLayout(window)
btn_box = QHBoxLayout()
btn_box.setContentsMargins(30, 10, 10, 10)  # Add padding around buttons
btn_box.setSpacing(30)  # Add spacing between buttons


def green_button_pressed():
    print("Green Button clicked")
    time.sleep(2)
    print("Green Button finished")


def slider_changed(value):
    freq = value / 10
    slider_label.setText(f"Frequency: {freq} Hz")
    # print(f"Frequency: {freq} Hz")


green_btn = QPushButton("Green Button")
green_btn.setStyleSheet("background-color: green; color: white")
green_btn.clicked.connect(green_button_pressed)
btn_box.addWidget(green_btn)

red_btn = QPushButton("Red Button")
red_btn.setStyleSheet("background-color: red; color: white")
red_btn.clicked.connect(lambda: print("Red Button clicked"))
btn_box.addWidget(red_btn)


yellow_btn = QPushButton("Yellow Button")
yellow_btn.setStyleSheet("background-color: yellow; color: black")
yellow_btn.clicked.connect(lambda: print("Yellow Button clicked"))
btn_box.addWidget(yellow_btn)

off_btn = QPushButton("Yellow Button")
off_btn.setStyleSheet("background-color: black; color: white")
off_btn.clicked.connect(lambda: print("Off Button clicked"))
btn_box.addWidget(off_btn)

slider = QSlider(Qt.Horizontal)
slider.setMinimum(0)
slider.setMaximum(40)
slider.setValue(20)
slider.setTickInterval(5)
slider.setTickPosition(QSlider.TicksBelow)
slider_label = QLabel("Frequency: 2 Hz")
slider_label.setAlignment(Qt.AlignCenter)
slider_label.setStyleSheet("font-size: 20px; padding: 10px;")
slider.valueChanged.connect(slider_changed)

wdg_box.addLayout(btn_box)
wdg_box.addStretch()
wdg_box.addWidget(slider_label)
wdg_box.addWidget(slider)
window.setLayout(wdg_box)
window.show()
sys.exit(app.exec_())
