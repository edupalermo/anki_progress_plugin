from aqt.qt import Qt, QRect, QWidget, QPainter, QColor, QFont, QBrush, QPen, QLinearGradient


class GradientProgressBar(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = None

    def paintEvent(self, e):

        if self.data is None:
            return

        qp = QPainter()
        qp.begin(self)

        # Draw gradient
        pen = QPen()
        pen.setStyle(Qt.PenStyle.NoPen)
        qp.setPen(pen)

        gradient = QLinearGradient(0.0, 0.0, self.width(), 0)
        gradient.setColorAt(0, QColor(116, 169, 207))
        gradient.setColorAt(1, QColor(255, 0, 0))

        brush = QBrush(gradient)
        qp.setBrush(brush)
        qp.drawRect(QRect(0, 0, self.geometry().width(), self.geometry().height()))

        # Draw progress bar
        if self.data["total"] > 0:
            pen = QPen()
            pen.setStyle(Qt.PenStyle.NoPen)
            qp.setPen(pen)

            brush = QBrush(QColor(255, 255, 255))
            brush.setStyle(Qt.BrushStyle.SolidPattern)
            qp.setBrush(brush)
            print(round((self.data["done"] / self.data["total"]) * self.geometry().width()))
            qp.drawRect(QRect(round((self.data["done"] / self.data["total"]) * self.geometry().width()), 0,
                              self.width(), self.height()))

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
        # rect = QRect(0, 0, self.geometry().width(), self.geometry().height())
        # rect.adjust(0, 0, -10, 0)
        # font = QFont()
        # font.setFamily("Courier New")
        # font.setBold(True)
        # font.setPointSize(20)
        # qp.setFont(font)
        # qp.drawText(rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, "04/12/2021 21:14:00")

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
