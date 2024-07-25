from PyQt5.QtWidgets import QInputDialog, QListWidgetItem


def add_category(listWidget, text=None):
    if text is None:
        text, ok = QInputDialog.getText(None, "Add Category", "Enter category name:")
    else:
        ok = True
    if ok and text:
        listWidget.addItem(text)


def delete_category(listWidget):
    current_item = listWidget.currentItem()
    if current_item:
        row = listWidget.row(current_item)
        listWidget.takeItem(row)
        print(listWidget)
