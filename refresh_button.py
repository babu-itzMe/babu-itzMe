from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QIcon, QPixmap, QTransform, QPainter
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import QPropertyAnimation, Qt, QByteArray, pyqtProperty

class RefreshButton(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        svg_data = '''
            <svg xmlns="http://www.w3.org/2000/svg" fill="white" viewBox="0 0 32 32" width="32" height="32" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink">
                <path d="M24.144 10H21c-1.106 0 -2 0.894 -2 2s0.894 2 2 2h8c1.106 0 2 -0.894 2 -2V4c0 -1.106 -0.894 -2 -2 -2s-2 0.894 -2 2v3.2l-1.1 -1.1c-5.469 -5.469 -14.331 -5.469 -19.8 0s-5.469 14.331 0 19.8 14.331 5.469 19.8 0c0.781 -0.781 0.781 -2.05 0 -2.831s-2.05 -0.781 -2.831 0c-3.906 3.906 -10.238 3.906 -14.144 0s-3.906 -10.238 0 -14.144 10.238 -3.906 14.144 0z"></path>
            </svg>
        '''
        # Load the SVG from the string using QByteArray
        self.svg_renderer = QSvgRenderer(QByteArray(svg_data.encode()))

        # Create a QPixmap to render the SVG into a square icon
        self.icon_size = 18  # Size of the icon (square)
        self.icon_pixmap = QPixmap(self.icon_size, self.icon_size)
        self.icon_pixmap.fill(Qt.GlobalColor.transparent)  # Transparent background

        # Create a QPainter to paint the SVG onto the QPixmap
        painter = QPainter(self.icon_pixmap)
        self.svg_renderer.render(painter)
        painter.end()

        # Create the button with the icon
        self.button = QPushButton("  Refresh Data  ",self)
        self.button.setIcon(QIcon(self.icon_pixmap))
        self.button.setIconSize(self.icon_pixmap.rect().size())
        # self.button.setStyleSheet("padding: 10px;")
        self.apply_button_style(self.button, bg_color="#9641e5", hr_color="#8a2be2")
        self.button.clicked.connect(self.on_button_clicked)

        # Initialize the rotation angle
        self._rotation_angle = 0

        # Create the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def apply_button_style(self, button, bg_color, hr_color):
        """Apply a consistent style to the given button."""
        button.setStyleSheet(f"""
            QPushButton {{
                color: white;           /* Text color */
                background-color: {bg_color} ; /* Background color */
                font-size: 14px;        /* Font size */
                font-weight: bold;      /* Font weight */
                font-family: Arial;     /* Font family */
                border-radius: 10px;    /* Rounded corners */
                padding: 10px 20px;     /* Padding */
            }}
            QPushButton:hover {{
                background-color: {hr_color}; /* Background color on hover */
            }}
            QPushButton:pressed {{
                background-color: navy; /* Background color when pressed */
                color: white;
            }}
        """)
    @pyqtProperty(float)
    def rotation_angle(self):
        return self._rotation_angle

    @rotation_angle.setter
    def rotation_angle(self, angle):
        self._rotation_angle = angle
        self.rotate_icon(self._rotation_angle)

    def on_button_clicked(self):
        # Perform the spin animation
        self.animate_icon_spin()
        self.refresh_excel_data()

    def animate_icon_spin(self):
        # Create a QPropertyAnimation to rotate the icon
        self.animation = QPropertyAnimation(self, b"rotation_angle")
        self.animation.setDuration(1000)  # Duration of 1 second
        self.animation.setStartValue(0)
        self.animation.setEndValue(360)
        self.animation.setLoopCount(1)  # Only spin once
        self.animation.start()

    def rotate_icon(self, angle):
        # Rotate the icon using the specified angle
        rotated_pixmap = QPixmap(self.icon_size, self.icon_size)
        rotated_pixmap.fill(Qt.GlobalColor.transparent)  # Transparent background

        transform = QTransform().translate(self.icon_size / 2, self.icon_size / 2).rotate(angle).translate(-self.icon_size / 2, -self.icon_size / 2)
        
        painter = QPainter(rotated_pixmap)
        painter.setTransform(transform)
        painter.drawPixmap(0, 0, self.icon_pixmap)
        painter.end()

        self.button.setIcon(QIcon(rotated_pixmap))

    def refresh_excel_data(self):
        # Implement this method in the main application class
        print("Refreshing Excel data...")

if __name__ == '__main__':
    app = QApplication([])
    widget = RefreshButton()
    widget.show()
    app.exec()
