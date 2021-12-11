import math
from datetime import datetime

from aqt.qt import Qt, QRect, QWidget, QPainter, QColor, QFont, QFontMetrics, QBrush, QPen, QTimer


class VerticalBarChart(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = None
        self.transition = {}

        self.timer = QTimer()
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.recurring_timer)


    def paintEvent(self, e):

        if self.data is None:
            return

        qp = QPainter()
        qp.begin(self)

        # Draw white background
        pen = QPen()
        pen.setStyle(Qt.PenStyle.NoPen)
        qp.setPen(pen)

        brush = QBrush(QColor(255, 255, 255))
        #brush = QBrush(QColor(200, 200, 200))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        qp.setBrush(brush)
        qp.drawRect(QRect(0, 0, self.geometry().width(), self.geometry().height()))

        font = QFont()
        font.setFamily("arial")
        font.setBold(True)
        font.setPointSize(20)
        fm = QFontMetrics(font)

        general_padding = 5
        top_padding = round((fm.height() / 2) + general_padding)
        max_y = self.get_max_y()

        a = ((top_padding + 2 * general_padding) + fm.height() - self.height()) / max_y
        b = self.height() - (2 * general_padding) - fm.height()

        delta_y = self.calculate_delta_y(a, b, max_y, fm.height())
        largest_label_y = self.calculate_largest_label_y(delta_y, max_y, fm)

        # Este menos dois representa a distancia dos eixos
        bar_width = int((self.width() - (general_padding * 3) - largest_label_y - 2) / len(self.data))

        # Draw y labels
        i = 0
        while i <= max_y:
            pen = QPen()
            pen.setStyle(Qt.PenStyle.SolidLine)
            pen.setColor(QColor(0, 0, 0))
            qp.setPen(pen)

            formatted_label = self.format_numeric_label(delta_y, i)
            pos_y = round((a * i) + b)
            rect = QRect(general_padding, round(pos_y - (fm.height() / 2)), largest_label_y, fm.height())
            # qp.drawRect(rect)
            qp.drawText(rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, formatted_label)
            qp.drawLine(2 * general_padding + largest_label_y, pos_y, 2 * general_padding + largest_label_y - 3, pos_y)
            i = i + delta_y

            pen = QPen()
            pen.setStyle(Qt.PenStyle.DashLine)
            pen.setColor(QColor(195, 195, 195))
            qp.setPen(pen)
            qp.drawLine(2 * general_padding + largest_label_y, pos_y, self.width() - general_padding, pos_y)

        # Draw x labels
        pen = QPen()
        pen.setStyle(Qt.PenStyle.SolidLine)
        pen.setColor(QColor(0, 0, 0))
        qp.setPen(pen)

        i = 0
        while i < len(self.data):
            formatted_label = self.format_numeric_label(1, i)
            rect_x = 2 * general_padding + largest_label_y + (i * bar_width) + 1
            rect_y = int((self.data[i] * a) + b)
            rect_width = bar_width - 2
            rect = QRect(rect_x, self.height() - general_padding - fm.height(), rect_width, fm.height())
            # qp.drawRect(rect)
            qp.drawText(rect, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop, formatted_label)
            pos_x = round(rect_x + (bar_width / 2) - 1)
            pos_y = self.height() - fm.height() - 2 * general_padding
            qp.drawLine(pos_x, pos_y, pos_x, pos_y + 3)
            i = i + 1

        # Draw Rectangular
        pen = QPen()
        pen.setStyle(Qt.PenStyle.SolidLine)
        pen.setColor(QColor(0, 0, 0))
        qp.setPen(pen)

        qp.drawLine(2 * general_padding + largest_label_y, top_padding, self.width() - general_padding, top_padding)
        qp.drawLine(2 * general_padding + largest_label_y, self.height() - 2 * general_padding - fm.height(),
                    self.width() - general_padding, self.height() - 2 * general_padding - fm.height())
        qp.drawLine(2 * general_padding + largest_label_y, top_padding, 2 * general_padding + largest_label_y,
                    self.height() - 2 * general_padding - fm.height())
        qp.drawLine(self.width() - general_padding, top_padding, self.width() - general_padding,
                    self.height() - 2 * general_padding - fm.height())

        # Draw Bars
        for i in range(len(self.data)):
            pen = QPen()
            pen.setStyle(Qt.PenStyle.SolidLine)
            pen.setColor(QColor(0, 0, 0))
            qp.setPen(pen)

            brush = QBrush(self.get_color(i))
            brush.setStyle(Qt.BrushStyle.SolidPattern)
            qp.setBrush(brush)
            rect_x = 2 * general_padding + largest_label_y + (i * bar_width) + 2
            rect_y = int((self.data[i] * a) + b)
            rect_width = bar_width - 2
            rect_height = b - rect_y
            qp.drawRect(QRect(rect_x, rect_y, rect_width, rect_height))


        # Draw auxiliary lines
        '''
        pen = QPen()
        pen.setStyle(Qt.PenStyle.SolidLine)
        pen.setColor(QColor(0, 0, 0))
        qp.setPen(pen)

        qp.drawLine(padding, 0, padding, self.height())
        qp.drawLine(padding + largest_label_y, 0, padding + largest_label_y, self.height())
        qp.drawLine(2*padding + largest_label_y, 0, 2*padding + largest_label_y, self.height())
        qp.drawLine(self.width() - padding, 0, self.width() - padding, self.height())

        qp.drawLine(0, padding, self.width(), padding)
        qp.drawLine(0, self.height() - padding, self.width(), self.height() - padding)
        qp.drawLine(0, self.height() - padding - fm.height(), self.width(), self.height() - padding - fm.height())

        print("LargestLabel %d" % largest_label_y)
        '''
        qp.end()

    def get_color(self, i):
        transaction_time = 60 * math.pow(10, 3)  # seconds
        if i in self.transition:
            milliseconds = (datetime.now().timestamp() - self.transition[i].timestamp()) * 1000
            if milliseconds < transaction_time:
                progress = min(milliseconds / transaction_time, 1)
                return QColor(self.get_proportion(255, 116, progress),
                              self.get_proportion(0, 169, progress),
                              self.get_proportion(0, 207, progress))
            else:
                self.transition.pop(i, None)
                if len(self.transition) == 0:
                    self.timer.stop()
                return QColor(116, 169, 207)
        else:
            return QColor(116, 169, 207)

    def get_proportion(self, initial, final, progress):
        return round(progress * (final - initial) + initial)

    def get_max_y(self) :
        max_y = 0
        for i in self.data:
            max_y = max(max_y, i)
        return max_y

    def format_numeric_label(self, delta_y, value):
        if math.log10(delta_y) >= 0:
            return "%d" % int(value)
        else:
            raise ValueError('Not implemented')

    def calculate_largest_label_y(self, delta_y, max_y, fm):
        largest = 0
        i = 0
        while i <= max_y:
            largest = max(largest, fm.boundingRect(self.format_numeric_label(delta_y, i)).width())
            i = i + delta_y
        return largest

    def update_state(self, data):
        if self.data is not None:
            for i in range(min(len(data), len(self.data))):
                if self.data[i] != data[i]:
                    self.transition[i] = datetime.now()
                    if not self.timer.isActive():
                        self.timer.start()

        self.data = [None] * len(data)
        for i in range(len(data)):
            self.data[i] = data[i]
        self.update()

    def calculate_delta_y(self, a, b, max_y, font_height):
        exponent = int(math.log10((font_height - b) / a))
        while (a * math.pow(10, exponent) + b) < font_height:
            exponent = exponent + 1
        return math.pow(10, exponent)

    def recurring_timer(self):
        self.update()
