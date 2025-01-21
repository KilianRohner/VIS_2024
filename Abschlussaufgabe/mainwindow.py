import sys
import json
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QStatusBar,
    QFileDialog,
    QMessageBox,
    QPushButton,
)
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QSize
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
import inputfilereader
import mbsModel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("3D-Viewer mit VTK")
        self.resize(800, 600)

        # Initialize model
        self.model = None

        # Create main layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.button_layout = QHBoxLayout()  # Layout for buttons

        # Add VTK render window
        self.vtk_widget = QVTKRenderWindowInteractor(self.central_widget)
        self.main_layout.addWidget(self.vtk_widget)

        # Initialize VTK renderer
        self.renderer = vtk.vtkRenderer()  # Create the VTK renderer
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)  # Attach renderer to VTK window

        # Initialize interactor
        self.interactor = self.vtk_widget.GetRenderWindow().GetInteractor()

        # Add buttons
        self.add_buttons()

        # Setup menu
        self._create_menu()

        # Setup status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.show()

    def add_buttons(self):
        """Add buttons for ISO view, move, zoom, and rotate."""
        # ISO View Button
        self.iso_button = QPushButton(self)
        self.iso_button.setIcon(QIcon("VIS_2024/Abschlussaufgabe/icons/box.svg"))  # Replace with your actual SVG path
        self.iso_button.setIconSize(QSize(32, 32))
        self.iso_button.setToolTip("Switch to ISO view")
        self.iso_button.clicked.connect(self.set_iso_view)
        self.button_layout.addWidget(self.iso_button)

       

        # Zoom Button
        self.zoom_button = QPushButton(self)
        self.zoom_button.setIcon(QIcon("VIS_2024/Abschlussaufgabe/icons/scan-search.svg"))  # Replace with your actual SVG path
        self.zoom_button.setIconSize(QSize(32, 32))
        self.zoom_button.setToolTip("Zoom")
        self.zoom_button.clicked.connect(self.set_zoom_mode)
        self.button_layout.addWidget(self.zoom_button)

        # Rotate Button
        self.rotate_button = QPushButton(self)
        self.rotate_button.setIcon(QIcon("VIS_2024/Abschlussaufgabe/icons/rotate-3d.svg"))  # Replace with your actual SVG path
        self.rotate_button.setIconSize(QSize(32, 32))
        self.rotate_button.setToolTip("Rotate")
        self.rotate_button.clicked.connect(self.set_rotate_mode)
        self.button_layout.addWidget(self.rotate_button)

        # Add button layout to the main layout
        self.main_layout.addLayout(self.button_layout)

    def _create_menu(self):
        menu_bar = self.menuBar()

        # File menu
        file_menu = menu_bar.addMenu("File")

        load_action = QAction("Load", self)
        load_action.triggered.connect(self.load_model)
        file_menu.addAction(load_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_model)
        file_menu.addAction(save_action)

        import_action = QAction("Import FDD", self)
        import_action.triggered.connect(self.import_fdd)
        file_menu.addAction(import_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu
        view_menu = menu_bar.addMenu("View")

        iso_view_action = QAction("ISO View", self)
        iso_view_action.triggered.connect(self.set_iso_view)
        view_menu.addAction(iso_view_action)

        self.setMenuBar(menu_bar)

    def load_model(self):
        """Load a model from a JSON file."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Model", "", "JSON Files (*.json)")
        if file_name:
            try:
                self.model = mbsModel.mbsModel()  # Initialize the model
                self.model.loadDatabase(file_name)  # Load the model from JSON
                self.status_bar.showMessage(f"Model loaded: {file_name}")
                self.render_model()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load model: {e}")

    def save_model(self):
        """Save the current model to a JSON file."""
        if not self.model:
            QMessageBox.warning(self, "Warning", "No model to save.")
            return

        file_name, _ = QFileDialog.getSaveFileName(self, "Save Model", "", "JSON Files (*.json)")
        if file_name:
            try:
                self.model.saveDatabase(file_name)  # Save the model as JSON
                self.status_bar.showMessage(f"Model saved: {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save model: {e}")

    def import_fdd(self):
        """Import a model from a .fdd file."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Import FDD File", "", "FDD Files (*.fdd)")
        if file_name:
            try:
                self.model = mbsModel.mbsModel()  # Initialize the model
                if self.model.importFddFile(file_name):  # Import the model from FDD
                    self.status_bar.showMessage(f"FDD file imported: {file_name}")
                    self.render_model()
                else:
                    QMessageBox.critical(self, "Error", "Failed to import FDD file.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import FDD file: {e}")

    def render_model(self):
        """Render the model in the VTK window."""
        if not self.model:
            return

        self.renderer.RemoveAllViewProps()  # Clear the renderer

        # Add mbsObjects to the renderer
        self.model.showModel(self.renderer)  # Use model's showModel method

        self.renderer.ResetCamera()
        self.vtk_widget.GetRenderWindow().Render()

    def set_iso_view(self):
        """Set the camera to an isometric view."""
        if not self.renderer:
            QMessageBox.warning(self, "Warning", "No model loaded to set ISO view.")
            return

        # Set the camera position and focal point for an isometric view
        camera = self.renderer.GetActiveCamera()
        camera.SetPosition(1, 1, 1)  # Equal distance along X, Y, Z
        camera.SetFocalPoint(0, 0, 0)  # Look at the origin
        camera.SetViewUp(0, 0, 1)  # Define the "up" direction

        # Update the view
        self.renderer.ResetCamera()
        self.vtk_widget.GetRenderWindow().Render()

    def set_zoom_mode(self):
        """Set the interactor style to zoom."""
        interactor_style = vtk.vtkInteractorStyleRubberBandZoom()  # Rubber band zoom for zoom mode
        self.interactor.SetInteractorStyle(interactor_style)
        self.status_bar.showMessage("Zoom mode activated.")

    def set_rotate_mode(self):
        """Set the interactor style to rotate."""
        interactor_style = vtk.vtkInteractorStyleTrackballCamera()
        self.interactor.SetInteractorStyle(interactor_style)
        self.status_bar.showMessage("Normal mode activated.")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    # If there's a command line argument for the .fdd file, load it immediately
    if len(sys.argv) > 1:
        fdd_file_path = sys.argv[1]
        if window.model is None:
            window.model = mbsModel.mbsModel()
        window.model.importFddFile(fdd_file_path)
        window.render_model()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
