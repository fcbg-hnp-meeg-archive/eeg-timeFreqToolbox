from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QListWidget,
                             QDialogButtonBox, QLabel)


class PickEvents(QDialog):
    def __init__(self, parent, events, selected=[]):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle('Pick Events')
        self.initial_selection = selected
        self.layout = QVBoxLayout(self)
        self.init_channel_box(events, selected)
        self.init_buttonbox()
        self.ch.itemSelectionChanged.connect(self.init_buttons)
        self.init_buttons()

    # ---------------------------------------------------------------------
    def init_buttonbox(self):
        """Initialize button box
        """
        self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok |
                                          QDialogButtonBox.Cancel)
        (self.buttonbox.button(QDialogButtonBox.Ok)
         .clicked.connect(self.close))
        (self.buttonbox.button(QDialogButtonBox.Cancel)
         .clicked.connect(self.close))
        self.layout.addWidget(self.buttonbox)

    # ---------------------------------------------------------------------
    def init_channel_box(self, events, selected):
        """Initialize list
        """
        self.ch = QListWidget()
        self.ch.insertItems(0, events)
        self.ch.setSelectionMode(QListWidget.ExtendedSelection)
        for i in range(self.ch.count()):
            if self.ch.item(i).data(0) in selected:
                self.ch.item(i).setSelected(True)
        self.layout.addWidget(self.ch)

    # ---------------------------------------------------------------------
    def init_buttons(self):
        """Toggle OK button
        """
        selected = [item.data(0) for item in self.ch.selectedItems()]
        if selected != self.initial_selection:
            self.buttonbox.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonbox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.parent.set_selected_events(selected)
