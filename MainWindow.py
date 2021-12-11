from aqt.qt import Qt, QRect, QWidget, QPainter, QColor, QFont, QBrush, QPen, QMainWindow, QVBoxLayout, QLabel, \
    QTextEdit
from . import GradientProgressBar, VerticalBarChart


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Anki Plugin")
        self.setMinimumWidth(500)

        self.progresses = [GradientProgressBar.GradientProgressBar(self) for i in range(4)]
        for progress in self.progresses:
            progress.setMinimumHeight(35)
        self.verticalBarChart = VerticalBarChart.VerticalBarChart()
        self.verticalBarChart.setMinimumHeight(500)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Progress of the current deck", self))
        layout.addWidget(self.progresses[0])
        layout.addWidget(QLabel("Progress of the current deck + accumulated"))
        layout.addWidget(self.progresses[1])
        layout.addWidget(QLabel("Progress of all decks"))
        layout.addWidget(self.progresses[2])
        layout.addWidget(QLabel("Progress of all decks + accumulated"))
        layout.addWidget(self.progresses[3])
        layout.addWidget(QLabel("Future due"))
        layout.addWidget(self.verticalBarChart, 100)

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

    def update_future_due_chart(self, data):
        self.verticalBarChart.update_state(data)
