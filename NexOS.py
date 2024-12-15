import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel,
                             QStackedWidget, QWidget, QHBoxLayout, QDialog, QGridLayout, QMessageBox, QTextEdit, QTreeView, QFileSystemModel)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import os

class AppWindow(QWidget):
    def __init__(self, title, content):
        super().__init__()
        self.setWindowTitle(title)
        self.setWindowFlags(Qt.Window)
        self.resize(600, 400)

        layout = QVBoxLayout()
        label = QLabel(content)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        close_button = QPushButton("Fermer")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

class FileExplorer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Explorateur de fichiers")
        self.resize(800, 600)

        layout = QVBoxLayout()

        # Modèle pour afficher le système de fichiers
        self.model = QFileSystemModel()
        self.model.setRootPath("")

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(""))
        self.tree.setColumnWidth(0, 250)
        layout.addWidget(self.tree)

        close_button = QPushButton("Fermer")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

class WebBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Navigateur Web")
        self.resize(1024, 768)

        layout = QVBoxLayout()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))  # URL de départ
        layout.addWidget(self.browser)

        close_button = QPushButton("Fermer")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

class WindowManager:
    def __init__(self):
        self.windows = []

    def create_window(self, title, content):
        window = AppWindow(title, content)
        self.windows.append(window)
        window.show()

    def create_file_explorer(self):
        explorer = FileExplorer()
        self.windows.append(explorer)
        explorer.show()

    def create_browser(self):
        browser = WebBrowser()
        self.windows.append(browser)
        browser.show()

    def close_all_windows(self):
        for window in self.windows:
            window.close()
        self.windows.clear()

class Desktop(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NexOS 1.0")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()

        # Chemin des icônes
        self.icon_path = os.path.join(os.path.dirname(__file__), "icons")

        # Gestionnaire de fenêtres
        self.window_manager = WindowManager()

        # Layout principal
        main_layout = QVBoxLayout()

        # Barre des tâches personnalisée
        self.taskbar = QHBoxLayout()
        self.create_taskbar()
        main_layout.addLayout(self.taskbar)

        # Conteneur principal pour les applications
        self.container = QStackedWidget()
        main_layout.addWidget(self.container)

        # Widgets de bureau et autres fenêtres
        self.desktop_widget = QWidget()
        self.create_desktop()
        self.container.addWidget(self.desktop_widget)

        # Widget central
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_taskbar(self):
        self.menu_button = QPushButton("NexOS Menu")
        self.menu_button.setIcon(QIcon(os.path.join(self.icon_path, "menu.png")))
        self.menu_button.clicked.connect(self.open_menu)
        self.taskbar.addWidget(self.menu_button)

        self.settings_button = QPushButton("Paramètres")
        self.settings_button.setIcon(QIcon(os.path.join(self.icon_path, "settings.png")))
        self.settings_button.clicked.connect(self.open_settings)
        self.taskbar.addWidget(self.settings_button)

        self.return_to_windows_button = QPushButton("Revenir à Windows")
        self.return_to_windows_button.setIcon(QIcon(os.path.join(self.icon_path, "windows.png")))
        self.return_to_windows_button.clicked.connect(self.return_to_windows)
        self.taskbar.addWidget(self.return_to_windows_button)

        self.taskbar.addStretch()

    def create_desktop(self):
        layout = QGridLayout()

        def create_icon_button(icon_name, text, callback):
            widget = QWidget()
            vbox = QVBoxLayout()
            button = QPushButton()
            button.setIcon(QIcon(os.path.join(self.icon_path, icon_name)))
            button.setIconSize(QSize(64, 64))
            button.setFlat(True)
            button.clicked.connect(callback)

            label = QLabel(text)
            label.setAlignment(Qt.AlignCenter)

            vbox.addWidget(button)
            vbox.addWidget(label)
            vbox.setAlignment(Qt.AlignCenter)
            widget.setLayout(vbox)
            return widget

        file_explorer = create_icon_button("explorer.png", "Explorateur", self.window_manager.create_file_explorer)
        browser = create_icon_button("browser.png", "Navigateur", self.window_manager.create_browser)
        notes = create_icon_button("notes.png", "Bloc-notes", self.open_notes)
        custom_app = create_icon_button("app.png", "Application", lambda: self.window_manager.create_window("Application personnalisée", "Ceci est une application personnalisée."))

        layout.addWidget(file_explorer, 0, 0)
        layout.addWidget(browser, 0, 1)
        layout.addWidget(notes, 1, 0)
        layout.addWidget(custom_app, 1, 1)

        self.desktop_widget.setLayout(layout)

    def open_notes(self):
        self.window_manager.create_window("Bloc-notes", "L'application Bloc-notes est en cours de développement.")

    def open_menu(self):
        menu_dialog = QDialog(self)
        menu_dialog.setWindowTitle("NexOS Menu")
        menu_dialog.setWindowFlags(Qt.Window)
        menu_layout = QVBoxLayout()

        app_button = QPushButton("Applications")
        app_button.setIcon(QIcon(os.path.join(self.icon_path, "apps.png")))
        app_button.clicked.connect(lambda: QMessageBox.information(self, "Applications", "Applications disponibles: Explorateur, Navigateur, Bloc-notes, Application."))
        menu_layout.addWidget(app_button)

        shutdown_button = QPushButton("Arrêter")
        shutdown_button.setIcon(QIcon(os.path.join(self.icon_path, "shutdown.png")))
        shutdown_button.clicked.connect(self.shutdown)
        menu_layout.addWidget(shutdown_button)

        menu_dialog.setLayout(menu_layout)
        menu_dialog.exec_()

    def open_settings(self):
        QMessageBox.information(self, "Paramètres", "Les paramètres sont en cours de développement.")

    def shutdown(self):
        QMessageBox.information(self, "Arrêt", "NexOS va s'arrêter.")
        self.close()

    def return_to_windows(self):
        QMessageBox.information(self, "Retour à Windows", "Vous revenez à l'environnement Windows.")
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    nexos = Desktop()
    nexos.show()
    sys.exit(app.exec_())
