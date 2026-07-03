from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout

class ErrorPopup(QDialog):
    """ Code from https://www.pythonguis.com/tutorials/pyside6-dialogs/"""
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("ERROR!")

        QBtn = (
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        message = QLabel("Cells cannot be empty!")
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)