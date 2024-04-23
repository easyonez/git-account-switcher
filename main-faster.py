import os
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
        "remove_text": "Remove",
        "success_message": "Git account switched successfully.",
        "confirm_delete_message": "Are you sure you want to delete this account?"
    },
    "Italian": {
        "email_label": "Inserisci la tua email:",
        "name_label": "Inserisci il tuo nome:",
        "existing_label": "Oppure seleziona:",
        "language_label": "Seleziona lingua:",
        "button_text": "Imposta",
        "remove_text": "Rimuovi",
        "success_message": "Account Git cambiato con successo.",
        "confirm_delete_message": "Sei sicuro di voler eliminare questo account?"
    },
    "Spanish": {
        "email_label": "Ingrese su email:",
        "name_label": "Ingrese su nombre:",
        "existing_label": "O seleccione:",
        "language_label": "Seleccione idioma:",
        "button_text": "Establecer",
        "remove_text": "Eliminar",
        "success_message": "Cuenta Git cambiada exitosamente.",
        "confirm_delete_message": "¿Seguro que quieres eliminar esta cuenta?"
    },
    "French": {
        "email_label": "Entrez votre e-mail:",
        "name_label": "Entrez votre nom:",
        "existing_label": "Ou sélectionnez:",
        "language_label": "Sélectionnez la langue:",
        "button_text": "Définir",
        "remove_text": "Supprimer",
        "success_message": "Compte Git changé avec succès.",
        "confirm_delete_message": "Êtes-vous sûr de vouloir supprimer ce compte ?"
    }
}



appdata_path = os.environ.get('APPDATA')
git_switch_accounts_path = os.path.join(appdata_path, 'Git Account Switcher')
git_accounts_file_path = os.path.join(git_switch_accounts_path, 'git_accounts.txt')
os.makedirs(git_switch_accounts_path, exist_ok=True)
if not os.path.exists(git_accounts_file_path):
    with open(git_accounts_file_path, "w") as f:
        pass

class GitAccountSwitcher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Git Account Switcher 1.0.0")
        self.setFixedSize(500, 400)
        self.setWindowIcon(QIcon("icon.ico"))
        
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
        self.remove = QPushButton("Remove", self)
        
        self.init_ui()
        
    def init_ui(self):
        self.label.setText("<b>Git Account Switcher 1.0.0</b>")
        self.email_label.setText("")
        self.name_label.setText("")
        self.existing_label.setText("")
        self.icons_label.setText("Icons by Icons8")

        self.label.setGeometry(150, 0, 250, 30)
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
        self.remove.setGeometry(200, 300, 100, 30)
        self.remove.setEnabled(False)
        self.remove.clicked.connect(self.delete_account)

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
        self.remove.setText(translations_dict["remove_text"])
        self.success_message = translations_dict["success_message"]

    def delete_account(self):
        selected_email = self.existing_dropdown.currentText()
        if selected_email:
            with open(git_accounts_file_path, "r+") as f:
                lines = f.readlines()
                f.seek(0)
                for line in lines:
                    if line.strip() != selected_email:
                        f.write(line)
                f.truncate()
            self.existing_dropdown.removeItem(self.existing_dropdown.currentIndex())
        
    def set_git_config(self):
        email = self.email_entry.text()
        name = self.name_entry.text()
        
        # Check if account already exists
        if any(f"{email}:{name}\n" == self.existing_dropdown.itemText(index) for index in range(self.existing_dropdown.count())):
            QMessageBox.warning(self, "Warning", "Account already exists.", QMessageBox.Ok)
            return
        
        # Set up Git config
        try:
            subprocess.run(["git", "config", "--global", "user.email", email], check=True)
            subprocess.run(["git", "config", "--global", "user.name", name], check=True)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Failed to set Git config: {e.stderr.decode()}", QMessageBox.Ok)
            return
        
        # Store the current configuration
        flag = False
        with open(git_accounts_file_path, "r") as f:
            for line in f:
                if line.strip() == f"{email}:{name}":
                    flag = True
                    break
        if not flag:
            with open(git_accounts_file_path, "a") as f:
                f.write(f"{email}:{name}\n")
            self.existing_dropdown.addItem(f"{email}:{name}")
            self.email_entry.clear()
            self.name_entry.clear()
                
        self.show_success_message()
        
    def load_existing_accounts(self):
        try:
            with open(git_accounts_file_path, "r") as f:
                existing_accounts = [line.strip() for line in f.readlines() if line.strip()]
                self.existing_dropdown.addItems(existing_accounts)
        except FileNotFoundError:
            pass
        
    def on_existing_select(self, index):
        selected_email = self.existing_dropdown.currentText()
        if selected_email:
            self.remove.setEnabled(True)
            self.name_entry.setText(selected_email.split(":")[1])
            self.email_entry.setText(selected_email.split(":")[0])
    
    def check_fields(self):
        # Enable button only if both email and name fields are not empty
        if self.email_entry.text() and self.name_entry.text():
            self.button_set.setEnabled(True)
        else:
            self.button_set.setEnabled(False)
            
    def show_success_message(self):
        sys.exit(app.exec_())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GitAccountSwitcher()
    sys.exit(app.exec_())
