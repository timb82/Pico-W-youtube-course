import sys
import socket
import time

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
    QSpacerItem,
    QSizePolicy,
    QDial,
    QGridLayout,
)
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        layout = QVBoxLayout()

        # Add a label at the top
        title_label = QLabel("LED control")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; padding: 20px")
        layout.addWidget(title_label)

        # Add spacers to center the title_label
        layout.addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        )

        # Create a grid layout for labels and buttons
        grid_layout = QGridLayout()

        # Add labels with circular borders
        self.lab_green = QLabel("G")
        self.lab_green.setStyleSheet(
            "border: 4px solid green; border-radius: 15px; padding: 10px; background-color: lightgray; color: black;"
        )
        self.lab_green.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(self.lab_green, 0, 0, Qt.AlignCenter)

        self.lab_yellow = QLabel("Y")
        self.lab_yellow.setStyleSheet(
            "border: 4px solid yellow; border-radius: 15px; padding: 10px; background-color: lightgray; color: black;"
        )
        self.lab_yellow.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(self.lab_yellow, 0, 1, Qt.AlignCenter)

        self.lab_red = QLabel("R")
        self.lab_red.setStyleSheet(
            "border: 4px solid red; border-radius: 15px; padding: 10px; background-color: lightgray; color: black;"
        )
        self.lab_red.setAlignment(Qt.AlignCenter)
        grid_layout.addWidget(self.lab_red, 0, 2, Qt.AlignCenter)

        # Add space between rows
        grid_layout.setVerticalSpacing(20)

        # Add toggle buttons
        self.button_green = QPushButton("Green")
        self.button_green.setCheckable(True)
        self.button_green.setFixedHeight(self.button_green.sizeHint().height() * 2)
        self.button_green.clicked.connect(self.pick_green)
        grid_layout.addWidget(self.button_green, 1, 0)

        self.button_yellow = QPushButton("Yellow")
        self.button_yellow.setCheckable(True)
        self.button_yellow.setFixedHeight(self.button_yellow.sizeHint().height() * 2)
        self.button_yellow.clicked.connect(self.pick_yellow)
        grid_layout.addWidget(self.button_yellow, 1, 1)

        self.button_red = QPushButton("Red")
        self.button_red.setCheckable(True)
        self.button_red.setFixedHeight(self.button_red.sizeHint().height() * 2)
        self.button_red.clicked.connect(self.pick_red)
        grid_layout.addWidget(self.button_red, 1, 2)

        layout.addLayout(grid_layout)

        # Add dial
        self.dial_layout = QVBoxLayout()
        self.dial_layout.addSpacerItem(
            QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)
        )  # Add space above the frequency label
        self.dial_label = QLabel("Frequency:")
        self.dial_label.setStyleSheet("font-size: 16px; padding: 20px")
        self.dial_label.setAlignment(Qt.AlignCenter)
        self.dial_layout.addWidget(self.dial_label)
        self.dial = QDial()
        self.dial_layout.addWidget(self.dial, alignment=Qt.AlignCenter)
        self.dial.setRange(0, 40)
        self.dial.valueChanged.connect(self.change_freq)
        layout.addLayout(self.dial_layout)

        # Add spacer to leave bottom empty
        layout.addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        # Add OFF button
        self.off_button = QPushButton("OFF")
        self.off_button.setStyleSheet("background-color: black; color: white;")
        self.off_button.setFixedHeight(self.button_green.sizeHint().height() * 2)
        self.off_button.clicked.connect(self.pick_off)
        layout.addWidget(self.off_button, alignment=Qt.AlignCenter)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.resizeEvent(None)  # Initial resize to set dial size

    def resizeEvent(self, event):
        super().resizeEvent(event)
        new_size = int(self.width() * 0.6)
        self.dial.setFixedSize(new_size, new_size)

    def toggle_color(self, label, color):
        current_color = label.styleSheet().split("background-color: ")[1].split(";")[0]
        new_color = color if current_color == "lightgray" else "lightgray"
        label.setStyleSheet(
            f"border: 4px solid {color}; border-radius: 15px; color: black; padding: 10px; background-color: {new_color};"
        )

    def pick_color(self, label):
        labels = [self.lab_red, self.lab_yellow, self.lab_green]
        buttons = [self.button_red, self.button_yellow, self.button_green]
        colors = ["red", "yellow", "green"]
        for lab, col, btn in zip(labels, colors, buttons):
            if lab == label:
                lab.setStyleSheet(
                    f"border: 4px solid {col}; border-radius: 15px; color: black; padding: 10px; background-color: {col};"
                )
                btn.setChecked(True)
            else:
                lab.setStyleSheet(
                    f"border: 4px solid {col}; border-radius: 15px; color: black; padding: 10px; background-color: lightgray;"
                )
                btn.setChecked(False)

    def pick_red(self):
        client_sock.sendto("red".encode(), srv_addr)
        # data, addr = client_sock.recvfrom(1024)
        # self.toggle_color(self.lab_red, "red")
        self.pick_color(self.lab_red)
        # print(f"received data: {data.decode()}")

    def pick_yellow(self):
        client_sock.sendto("yellow".encode(), srv_addr)
        # data, addr = client_sock.recvfrom(1024)
        # self.toggle_color(self.lab_yellow, "yellow")
        self.pick_color(self.lab_yellow)
        # print(f"received data: {data.decode()}")

    def pick_green(self):
        client_sock.sendto("green".encode(), srv_addr)
        # data, addr = client_sock.recvfrom(1024)
        # self.toggle_color(self.lab_green, "green")
        self.pick_color(self.lab_green)
        # print(f"received data: {data.decode()}")

    def pick_off(self):
        client_sock.sendto("off".encode(), srv_addr)
        self.pick_color(None)

    def change_freq(self):
        val = self.dial.value() / 10
        self.dial_label.setText(f"Frequency: {val}")

        client_sock.sendto(f"freq={val}".encode(), srv_addr)
        # data, addr = client_sock.recvfrom(1024)
        # print(f"received data: {data.decode()}")


client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
srv_addr = ("192.168.1.92", 12345)

# while True:
#     request_msg = input("pick color (red, green, yellow, off): ")
#     client_sock.sendto(request_msg.encode(), srv_addr)
#     # data, addr = client_sock.recvfrom(1024)
#     print(f"received data: {data.decode()}")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
