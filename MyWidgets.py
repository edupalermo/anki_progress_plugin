from aqt.qt import Qt, QRect, QWidget, QPainter, QColor, QFont, QBrush, QPen, QMainWindow, QVBoxLayout, QLabel, \
    QTextEdit, pyqtSignal


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Anki Plugin")
        self.setMinimumWidth(500)

        self.progresses = [QMyProgress(self) for i in range(4)]
        for progress in self.progresses:
            progress.setMinimumHeight(35)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Progress of the current deck", self))
        layout.addWidget(self.progresses[0])
        layout.addWidget(QLabel("Progress of the current deck + accumulated"))
        layout.addWidget(self.progresses[1])
        layout.addWidget(QLabel("Progress of all decks"))
        layout.addWidget(self.progresses[2])
        layout.addWidget(QLabel("Progress of all decks + accumulated"))
        layout.addWidget(self.progresses[3])
        layout.addWidget(QLabel("Achievements"))
        layout.addWidget(QTextEdit())

        container = QWidget()
        container.setLayout(layout)
        # Set the central widget of the Window.
        self.setCentralWidget(container)

        # self.progresses[0].update_state({"done": 5, "total": 10})
        self.progresses[1].update_state({"done": 6, "total": 10})
        self.progresses[2].update_state({"done": 7, "total": 10})
        self.progresses[3].update_state({"done": 7, "total": 10})

    def update_current_deck(self, data):
        self.progresses[0].update_state(data)

    def update_current_accumulated_deck(self, data):
        self.progresses[1].update_state(data)

    def update_all_decks(self, data):
        self.progresses[2].update_state(data)

    def update_all_accumulated_decks(self, data):
        self.progresses[3].update_state(data)


class QMyProgress(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = None

    def paintEvent(self, e):

        if self.data is None:
            return

        qp = QPainter()
        qp.begin(self)

        # Draw background bar
        pen = QPen()
        pen.setStyle(Qt.PenStyle.NoPen)
        qp.setPen(pen)

        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        qp.setBrush(brush)
        qp.drawRect(QRect(0, 0, self.geometry().width(), self.geometry().height()))

        # Draw progress bar
        if self.data["total"] > 0 and self.data["done"] > 0:
            pen = QPen()
            pen.setStyle(Qt.PenStyle.NoPen)
            qp.setPen(pen)

            brush = QBrush(QColor(255, 34, 3))
            brush.setStyle(Qt.BrushStyle.SolidPattern)
            qp.setBrush(brush)
            qp.drawRect(QRect(0, 0, round((self.data["done"] / self.data["total"]) * self.geometry().width()),
                              self.geometry().height()))

        # Draw the border
        pen = QPen()
        pen.setStyle(Qt.PenStyle.SolidLine)
        pen.setWidth(3)
        pen.setColor(QColor(0, 0, 0))
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        qp.setPen(pen)

        brush = QBrush()
        brush.setStyle(Qt.BrushStyle.NoBrush)
        qp.setBrush(brush)
        qp.drawRect(QRect(1, 1, self.geometry().width() - 3, self.geometry().height() - 3))

        # Draw text estimated final date
        rect = QRect(0, 0, self.geometry().width(), self.geometry().height())
        rect.adjust(0, 0, -10, 0)
        font = QFont()
        font.setFamily("Courier New")
        font.setBold(True)
        font.setPointSize(20)
        qp.setFont(font)
        qp.drawText(rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, "04/12/2021 21:14:00")

        # Draw progress
        rect = QRect(0, 0, self.geometry().width(), self.geometry().height())
        rect.adjust(10, 0, 0, 0)
        font = QFont()
        font.setFamily("Courier New")
        font.setBold(True)
        font.setPointSize(20)
        qp.setFont(font)
        qp.drawText(rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                    "{:0>2d}/{:0>2d}".format(self.data["done"], self.data["total"]))

        qp.end()

    def update_state(self, data):
        self.data = data
        self.update()
