import sys
import csv
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QTableWidget, QTableWidgetItem, QMessageBox
)
from PySide6.QtCore import Qt

class WatchListApp(QMainWindow):
    #set up window properties
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shows Watchlist Converter")
        self.setGeometry(100, 100, 600, 400)
        self.watchlist_path = None
        self.init_ui()

    #set up window UI components
    def init_ui(self):
        #layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        #file open button
        self.open_button = QPushButton("Open Watchlist File")
        self.open_button.clicked.connect(self.open_watchlist_file)
        layout.addWidget(self.open_button)

        #table and columns
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Show Name', 'Episode Number', 'Watch Status'])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        #export button
        self.export_button = QPushButton("Export to CSV")
        self.export_button.clicked.connect(self.export_csv)
        layout.addWidget(self.export_button)

        central_widget.setLayout(layout)

    #function to open watchlist file
    def open_watchlist_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Watchlist File", "", "Watchlist Files (*.watchlist);;All Files (*)")
        if not path:
            return
        self.watchlist_path = path
        self.load_watchlist(path)

    #function to load watchlist file into table
    def load_watchlist(self, path):
        self.table.setRowCount(0)
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split(":::")
                    if len(parts) == 3:
                        row = self.table.rowCount()
                        self.table.insertRow(row)
                        for col, value in enumerate(parts):
                            self.table.setItem(row, col, QTableWidgetItem(value))
        except Exception as e:
            QMessageBox.warning(self, "File Error", f"Could not open file:\n{e}")

    #function to export table data to CSV
    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "shows.csv", "CSV Files (*.csv)")
        if not path:
            return
        try:
            with open(path, "w", newline='', encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Show Name', 'Episode Number', 'Watch Status'])
                for row in range(self.table.rowCount()):
                    row_data = [
                        self.table.item(row, col).text() if self.table.item(row, col) else ""
                        for col in range(self.table.columnCount())
                    ]
                    writer.writerow(row_data)
            QMessageBox.information(self, "Export Successful", f"Data exported to {path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", str(e))

#actaully load app window
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WatchListApp()
    window.show()
    sys.exit(app.exec())