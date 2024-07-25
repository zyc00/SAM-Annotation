from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from utils.category_functions import add_category, delete_category
from utils.file_functions_sam import ImageViewer
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from omegaconf import OmegaConf
import argparse


Ui_MainWindow, BaseClass = uic.loadUiType("main.ui")


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, config):
        super().__init__()
        self.gui_config = config["GUI"]
        self.annotation_config = config["Annotation"]
        self.setupUi(self)
        self.initUI()
        self.myGraphicsViewInstance = ImageViewer(
            self.listWidget3,
            self.listWidget,
            self.listWidget2,
            self.textEdit,
            self.graphicsView,
            config=config["SAM"],
        )
        self.loadAnnotationConfig()
        self.listWidget.setCurrentRow(1)

    def loadAnnotationConfig(self):
        # load image folder by config
        if "image_folder" in self.annotation_config:
            self.myGraphicsViewInstance.openImageFolder(
                self.annotation_config["image_folder"]
            )

        # load annotation categories by config
        if "categories" in self.annotation_config:
            for category in self.annotation_config["categories"]:
                add_category(self.listWidget, category)

    def initUI(self):

        # set window size
        if self.gui_config["use_proportion"]:
            width = int(
                self.gui_config["window_width_proportion"]
                * self.gui_config["screen_size"][0]
            )
            height = int(
                self.gui_config["window_height_proportion"]
                * self.gui_config["screen_size"][1]
            )
        else:
            width = self.gui_config["window_width"]
            height = self.gui_config["window_height"]
        self.resize(width, height)

        # add buttons for category
        self.addButton.clicked.connect(lambda: add_category(self.listWidget))
        self.deleteButton.clicked.connect(lambda: delete_category(self.listWidget))

        # add buttons for image folder
        self.openFile.triggered.connect(
            lambda: self.myGraphicsViewInstance.openImageFolder()
        )
        self.saveFile.triggered.connect(
            lambda: self.myGraphicsViewInstance.saveAnnotationsToFile()
        )

        # add buttons for annotation
        self.pointButton.clicked.connect(
            lambda: self.myGraphicsViewInstance.onPointButtonClick()
        )

        # add buttons for delete annotation
        self.deleteButton2.clicked.connect(
            lambda: self.myGraphicsViewInstance.deleteAnnotation()
        )

    # stop annotation when press 'E'
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_E:
            self.myGraphicsViewInstance.isPointButtonClicked = False
            self.myGraphicsViewInstance.graphicsView.setCursor(QCursor(Qt.ArrowCursor))
            self.myGraphicsViewInstance.finishAnnotation()
        if event.key() == Qt.Key_Z:
            self.myGraphicsViewInstance.undoLastPoint()
        if event.key() == Qt.Key_S:
            self.myGraphicsViewInstance.saveAnnotationsToFile()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="./configs/config_vit_h.yaml")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    config = OmegaConf.to_container(OmegaConf.load(args.config))
    app = QApplication([])

    screen = app.primaryScreen()
    size = screen.size()
    config["GUI"]["screen_size"] = (size.width(), size.height())
    win = MainWindow(config)

    win.show()
    app.exec_()
