

/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick
import QtQuick.Controls
import LED_control_gui

Rectangle {
    id: rectangle
    width: Constants.width
    height: Constants.height

    color: Constants.backgroundColor

    Text {
        text: qsTr("Hello LED_control_gui") + " 01"
        anchors.top: parent.top
        anchors.topMargin: 80
        font.family: Constants.largeFont.family
        font.pixelSize: Constants.largeFont.pixelSize
        anchors.horizontalCenter: parent.horizontalCenter
    }

    Column {
        id: column
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.leftMargin: 10
        anchors.rightMargin: 10
        anchors.topMargin: 10
        anchors.bottomMargin: 10

        Row {
            id: row_top
            height: 300
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.leftMargin: 0
            anchors.rightMargin: 0
            anchors.topMargin: 150
        }

        Row {
            id: row_mid
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: row_top2.bottom
            anchors.bottom: row_bottom.top
            anchors.leftMargin: 0
            anchors.rightMargin: 0
            anchors.topMargin: 0
            anchors.bottomMargin: 0

            Dial {
                id: dial
                width: 300
                height: 300
            }
        }

        Row {
            id: row_bottom
            height: 100
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.leftMargin: 0
            anchors.rightMargin: 0
            anchors.bottomMargin: 0
        }

        Row {
            id: row_top2
            height: 300
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: row_top.bottom
            anchors.leftMargin: 0
            anchors.rightMargin: 0
            anchors.topMargin: 0
            spacing: 50
            layoutDirection: Qt.LeftToRight

            Button {
                id: button
                text: qsTr("Button")
            }

            Button {
                id: button1
                text: qsTr("Button")
            }

            Button {
                id: button2
                text: qsTr("Button")
            }
        }
    }
}
