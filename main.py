import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon

# Define translations for each language
translations = {
    "English": {
        "email_label": "Enter your email:",
        "name_label": "Enter your name:",
        "existing_label": "Or select:",
        "language_label": "Select language:",
        "button_text": "Set",
        "success_message": "Git account switched successfully."
    },
    "Italian": {
        "email_label": "Inserisci la tua email:",
        "name_label": "Inserisci il tuo nome:",
        "existing_label": "Oppure seleziona:",
        "language_label": "Seleziona lingua:",
        "button_text": "Imposta",
        "success_message": "Account Git cambiato con successo."
    },
    "Spanish": {
        "email_label": "Ingrese su email:",
        "name_label": "Ingrese su nombre:",
        "existing_label": "O seleccione:",
        "language_label": "Seleccione idioma:",
        "button_text": "Establecer",
        "success_message": "Cuenta Git cambiada exitosamente."
    },
    "French": {
        "email_label": "Entrez votre e-mail:",
        "name_label": "Entrez votre nom:",
        "existing_label": "Ou sélectionnez:",
        "language_label": "Sélectionnez la langue:",
        "button_text": "Définir",
        "success_message": "Compte Git changé avec succès."
    }
}

class GitAccountSwitcher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Git Account Switcher")
        self.setFixedSize(500, 400)
        self.setWindowIcon(QIcon("icon.png"))
        
        self.label = QLabel(self)
        self.email_label = QLabel(self)
        self.name_label = QLabel(self)
        self.existing_label = QLabel(self)
        self.icons_label = QLabel(self)

        self.email_entry = QLineEdit(self)
        self.name_entry = QLineEdit(self)
        self.existing_dropdown = QComboBox(self)
        self.language_dropdown = QComboBox(self)
        
        self.button_set = QPushButton("Set", self)
        
        self.init_ui()
        
    def init_ui(self):
        self.label.setText("<b>Git Account Switcher</b>")
        self.email_label.setText("")
        self.name_label.setText("")
        self.existing_label.setText("")
        self.icons_label.setText("Icons by Icons8")

        self.label.setGeometry(175, 0, 200, 30)
        self.email_label.setGeometry(50, 60, 150, 30)
        self.name_label.setGeometry(50, 110, 150, 30)
        self.existing_label.setGeometry(50, 160, 150, 30)
        self.icons_label.setGeometry(100, 350, 150, 30)

        self.email_entry.setGeometry(250, 60, 200, 30)
        self.name_entry.setGeometry(250, 110, 200, 30)
        self.existing_dropdown.setGeometry(250, 160, 200, 30)
        self.language_dropdown.setGeometry(250, 350, 200, 30)
        
        self.button_set.setGeometry(200, 250, 100, 30)
        self.button_set.setEnabled(False)
        
        self.language_dropdown.addItems(list(translations.keys()))
        self.language_dropdown.setCurrentText("English")
        self.language_dropdown.currentTextChanged.connect(self.change_language)
        
        self.button_set.clicked.connect(self.set_git_config)
        self.existing_dropdown.currentIndexChanged.connect(self.on_existing_select)
        
        self.email_entry.textChanged.connect(self.check_fields)
        self.name_entry.textChanged.connect(self.check_fields)
        
        self.update_text("English")
        self.load_existing_accounts()
        
        self.existing_dropdown.setCurrentIndex(-1)
        self.email_entry.clear()
        self.name_entry.clear()
        
        self.show()
        
    def change_language(self, language):
        self.update_text(language)
        
    def update_text(self, language):
        translations_dict = translations[language]
        self.email_label.setText(translations_dict["email_label"])
        self.name_label.setText(translations_dict["name_label"])
        self.existing_label.setText(translations_dict["existing_label"])
        self.button_set.setText(translations_dict["button_text"])
        self.success_message = translations_dict["success_message"]
        
    def set_git_config(self):
        email = self.email_entry.text()
        name = self.name_entry.text()
        
        # Check if account already exists
        if any(f"{email}:{name}\n" == self.existing_dropdown.itemText(index) for index in range(self.existing_dropdown.count())):
            QMessageBox.warning(self, "Warning", "Account already exists.", QMessageBox.Ok)
            return
        
        # Set up Git config
        subprocess.run(["git", "config", "--global", "user.email", email])
        subprocess.run(["git", "config", "--global", "user.name", name])
        
        # Store the current configuration
        flag = False
        with open("git_accounts.txt", "r") as f:
            for line in f:
                if line.strip() == f"{email}:{name}":
                    flag = True
                    break
        if flag == False:
            with open("git_accounts.txt", "a") as f:
                f.write(f"{email}:{name}\n")
            self.existing_dropdown.addItem(f"{email}:{name}")
            self.email_entry.clear()
            self.name_entry.clear()
                
        self.show_success_message()
        
    def load_existing_accounts(self):
        try:
            with open("git_accounts.txt", "r") as f:
                existing_accounts = [line.strip() for line in f.readlines() if line.strip()]
                self.existing_dropdown.addItems(existing_accounts)
        except FileNotFoundError:
            pass
        
    def on_existing_select(self, index):
        selected_email = self.existing_dropdown.currentText()
        if selected_email:
            self.name_entry.setText(selected_email.split(":")[1])
            self.email_entry.setText(selected_email.split(":")[0])
    
    def check_fields(self):
        # Enable button only if both email and name fields are not empty
        if self.email_entry.text() and self.name_entry.text():
            self.button_set.setEnabled(True)
        else:
            self.button_set.setEnabled(False)
            
    def show_success_message(self):
        QMessageBox.information(self, "Success", self.success_message, QMessageBox.Ok)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GitAccountSwitcher()
    sys.exit(app.exec_())
