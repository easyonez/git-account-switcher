import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QComboBox, QPushButton

# Define translations for each language
translations = {
    "English": {
        "email_label": "Enter your email:",
        "name_label": "Enter your name:",
        "existing_label": "Or select:",
        "language_label": "Select language:",
        "button_text": "Set",
    },
    "Italian": {
        "email_label": "Inserisci la tua email:",
        "name_label": "Inserisci il tuo nome:",
        "existing_label": "Oppure seleziona:",
        "language_label": "Seleziona lingua:",
        "button_text": "Imposta",
    },
    "Spanish": {
        "email_label": "Ingrese su email:",
        "name_label": "Ingrese su nombre:",
        "existing_label": "O seleccione:",
        "language_label": "Seleccione idioma:",
        "button_text": "Establecer",
    },
    "French": {
        "email_label": "Entrez votre e-mail:",
        "name_label": "Entrez votre nom:",
        "existing_label": "Ou sélectionnez:",
        "language_label": "Sélectionnez la langue:",
        "button_text": "Définir",
    }
}

class GitAccountSwitcher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Git Account Switcher")
        self.setFixedSize(500, 300)  # Set fixed window size
        
        self.email_label = QLabel(self)
        self.name_label = QLabel(self)
        self.existing_label = QLabel(self)
        self.language_label = QLabel(self)
        
        self.email_entry = QLineEdit(self)
        self.name_entry = QLineEdit(self)
        self.existing_dropdown = QComboBox(self)
        self.language_dropdown = QComboBox(self)
        
        self.button_set = QPushButton("Set", self)
        
        self.init_ui()
        
    def init_ui(self):
        self.email_label.setText("")
        self.name_label.setText("")
        self.existing_label.setText("")
        self.language_label.setText("")
        
        self.email_label.setGeometry(50, 30, 150, 30)
        self.name_label.setGeometry(50, 80, 150, 30)
        self.existing_label.setGeometry(50, 130, 150, 30)
        self.language_label.setGeometry(50, 180, 200, 30)
        
        self.email_entry.setGeometry(250, 30, 200, 30)
        self.name_entry.setGeometry(250, 80, 200, 30)
        self.existing_dropdown.setGeometry(250, 130, 200, 30)
        self.language_dropdown.setGeometry(250, 180, 200, 30)
        
        self.button_set.setGeometry(200, 250, 100, 30)
        self.button_set.setEnabled(False)  # Disable button by default
        
        self.language_dropdown.addItems(list(translations.keys()))
        self.language_dropdown.setCurrentText("English")
        self.language_dropdown.currentTextChanged.connect(self.change_language)
        
        self.button_set.clicked.connect(self.set_git_config)
        self.existing_dropdown.currentIndexChanged.connect(self.on_existing_select)
        
        self.email_entry.textChanged.connect(self.check_fields)  # Connect textChanged signals
        self.name_entry.textChanged.connect(self.check_fields)
        
        self.update_text("English")
        self.load_existing_accounts()  # Load existing accounts
        
        self.existing_dropdown.setCurrentIndex(-1)  # Clear selection
        self.email_entry.clear()  # Clear email entry
        self.name_entry.clear()   # Clear name entry
        
        self.show()
        
    def change_language(self, language):
        self.update_text(language)
        
    def update_text(self, language):
        translations_dict = translations[language]
        self.email_label.setText(translations_dict["email_label"])
        self.name_label.setText(translations_dict["name_label"])
        self.existing_label.setText(translations_dict["existing_label"])
        self.language_label.setText(translations_dict["language_label"])
        self.button_set.setText(translations_dict["button_text"])
        
    def set_git_config(self):
        email = self.email_entry.text()
        name = self.name_entry.text()
        
        # Set up Git config
        subprocess.run(["git", "config", "--global", "user.email", email])
        subprocess.run(["git", "config", "--global", "user.name", name])
        
        # Store the current configuration
        with open("git_accounts.txt", "a") as f:
            f.write(f"{email}:{name}\n")
        
        # Update existing accounts dropdown
        self.existing_dropdown.addItem(email)
        self.email_entry.clear()
        self.name_entry.clear()
        
        print("Git account switched successfully.")
        
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
            self.name_entry.setText(selected_email.split(":")[1])  # Set name to email for demonstration
            self.email_entry.setText(selected_email)
    
    def check_fields(self):
        # Enable button only if both email and name fields are not empty
        if self.email_entry.text() and self.name_entry.text():
            self.button_set.setEnabled(True)
        else:
            self.button_set.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GitAccountSwitcher()
    sys.exit(app.exec_())
