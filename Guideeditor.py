import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import tkinter.scrolledtext as scrolledtext
import re
import uu
import io
from PIL import Image, ImageTk
import pygame

class AmigaGuideEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("AmigaGuide Editor")
        self.language = 'en'  # Default language is English
        self.center_text = False  # Whether to center the text
        self.images = []  # Keep references to images to prevent garbage collection
        self.audio_data = None  # Holds the uuencoded audio data

        # Initialize pygame mixer for audio playback (if needed)
        pygame.mixer.init()

        # Create the menu
        self.create_menu()

        # Toolbar with formatting options
        self.create_toolbar()

        # Text editing area
        self.text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12))
        self.text.pack(fill=tk.BOTH, expand=True)

        # Tag configurations for formatting
        self.text.tag_configure("bold", font=("Arial", 12, "bold"))
        self.text.tag_configure("italic", font=("Arial", 12, "italic"))
        self.text.tag_configure("underline", font=("Arial", 12, "underline"))

    def create_menu(self):
        """Creates the menu bar and menus."""
        menubar = tk.Menu(self.root)

        # File menu
        self.file_menu = tk.Menu(menubar, tearoff=0)
        self.file_menu.add_command(label=self.get_label('New'), command=self.new_document)
        self.file_menu.add_command(label=self.get_label('Open'), command=self.open_document)
        self.file_menu.add_command(label=self.get_label('Save'), command=self.save_document)
        menubar.add_cascade(label=self.get_label('File'), menu=self.file_menu)

        # Insert menu
        self.insert_menu = tk.Menu(menubar, tearoff=0)
        self.insert_menu.add_command(label=self.get_label('Insert Link'), command=self.insert_link)
        self.insert_menu.add_command(label=self.get_label('Insert Image'), command=self.insert_image)
        self.insert_menu.add_command(label=self.get_label('Insert Audio'), command=self.insert_audio)
        menubar.add_cascade(label=self.get_label('Insert'), menu=self.insert_menu)

        # Options menu
        self.options_menu = tk.Menu(menubar, tearoff=0)
        # Language submenu
        self.language_menu = tk.Menu(self.options_menu, tearoff=0)
        self.language_menu.add_command(label='English', command=lambda: self.change_language('en'))
        self.language_menu.add_command(label='Deutsch', command=lambda: self.change_language('de'))
        self.language_menu.add_command(label='Français', command=lambda: self.change_language('fr'))
        self.options_menu.add_cascade(label=self.get_label('Language'), menu=self.language_menu)
        menubar.add_cascade(label=self.get_label('Options'), menu=self.options_menu)

        self.root.config(menu=menubar)

    def create_toolbar(self):
        """Creates a toolbar with formatting buttons."""
        toolbar = tk.Frame(self.root)
        toolbar.pack(fill=tk.X)

        bold_btn = tk.Button(toolbar, text="Bold", command=self.make_bold)
        bold_btn.pack(side=tk.LEFT)

        italic_btn = tk.Button(toolbar, text="Italic", command=self.make_italic)
        italic_btn.pack(side=tk.LEFT)

        underline_btn = tk.Button(toolbar, text="Underline", command=self.make_underline)
        underline_btn.pack(side=tk.LEFT)

    def get_label(self, text):
        """Returns the label text based on the selected language."""
        labels = {
            'en': {
                'File': 'File',
                'New': 'New',
                'Open': 'Open',
                'Save': 'Save',
                'Insert': 'Insert',
                'Insert Link': 'Insert Link',
                'Insert Image': 'Insert Image',
                'Insert Audio': 'Insert Audio',
                'Options': 'Options',
                'Language': 'Language',
                'Insert Link Button Here': 'Insert Link Button Here',
                'Enter Link Text:': 'Enter Link Text:',
                'Enter Node Name:': 'Enter Node Name:',
                'Select Image File': 'Select Image File',
                'Select Audio File': 'Select Audio File',
                'Save AmigaGuide File': 'Save AmigaGuide File',
                'Open AmigaGuide File': 'Open AmigaGuide File',
                'All Files': 'All Files',
                'AmigaGuide Files': 'AmigaGuide Files',
                'Error': 'Error',
                'Could not save file:': 'Could not save file:',
                'Could not open file:': 'Could not open file:',
                'Are you sure you want to create a new document? Unsaved changes will be lost.': 'Are you sure you want to create a new document? Unsaved changes will be lost.',
            },
            'de': {
                'File': 'Datei',
                'New': 'Neu',
                'Open': 'Öffnen',
                'Save': 'Speichern',
                'Insert': 'Einfügen',
                'Insert Link': 'Link einfügen',
                'Insert Image': 'Bild einfügen',
                'Insert Audio': 'Audio einfügen',
                'Options': 'Optionen',
                'Language': 'Sprache',
                'Insert Link Button Here': 'Link hier einfügen',
                'Enter Link Text:': 'Linktext eingeben:',
                'Enter Node Name:': 'Knotenname eingeben:',
                'Select Image File': 'Bilddatei auswählen',
                'Select Audio File': 'Audiodatei auswählen',
                'Save AmigaGuide File': 'AmigaGuide-Datei speichern',
                'Open AmigaGuide File': 'AmigaGuide-Datei öffnen',
                'All Files': 'Alle Dateien',
                'AmigaGuide Files': 'AmigaGuide-Dateien',
                'Error': 'Fehler',
                'Could not save file:': 'Datei konnte nicht gespeichert werden:',
                'Could not open file:': 'Datei konnte nicht geöffnet werden:',
                'Are you sure you want to create a new document? Unsaved changes will be lost.': 'Sind Sie sicher, dass Sie ein neues Dokument erstellen möchten? Ungespeicherte Änderungen gehen verloren.',
            },
            'fr': {
                'File': 'Fichier',
                'New': 'Nouveau',
                'Open': 'Ouvrir',
                'Save': 'Enregistrer',
                'Insert': 'Insérer',
                'Insert Link': 'Insérer un lien',
                'Insert Image': 'Insérer une image',
                'Insert Audio': 'Insérer un audio',
                'Options': 'Options',
                'Language': 'Langue',
                'Insert Link Button Here': 'Insérer un bouton de lien ici',
                'Enter Link Text:': 'Entrez le texte du lien :',
                'Enter Node Name:': 'Entrez le nom du nœud :',
                'Select Image File': 'Sélectionner le fichier image',
                'Select Audio File': 'Sélectionner le fichier audio',
                'Save AmigaGuide File': 'Enregistrer le fichier AmigaGuide',
                'Open AmigaGuide File': 'Ouvrir le fichier AmigaGuide',
                'All Files': 'Tous les fichiers',
                'AmigaGuide Files': 'Fichiers AmigaGuide',
                'Error': 'Erreur',
                'Could not save file:': 'Impossible d’enregistrer le fichier :',
                'Could not open file:': 'Impossible d’ouvrir le fichier :',
                'Are you sure you want to create a new document? Unsaved changes will be lost.': 'Êtes-vous sûr de vouloir créer un nouveau document ? Les modifications non enregistrées seront perdues.',
            }
        }
        return labels[self.language].get(text, text)

    def change_language(self, lang_code):
        """Changes the language to the selected one."""
        self.language = lang_code
        self.create_menu()
        # Update any other labels if necessary

    def new_document(self):
        """Creates a new document."""
        if messagebox.askyesno(self.get_label('File'), self.get_label('Are you sure you want to create a new document? Unsaved changes will be lost.')):
            self.text.delete(1.0, tk.END)
            self.audio_data = None

    def open_document(self):
        """Opens an existing AmigaGuide file."""
        file_path = filedialog.askopenfilename(
            title=self.get_label("Open AmigaGuide File"),
            filetypes=[(self.get_label("AmigaGuide Files"), "*.guide"), (self.get_label("All Files"), "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding='latin-1') as file:
                    content = file.read()
                self.text.delete(1.0, tk.END)
                self.text.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror(self.get_label("Error"), f"{self.get_label('Could not open file:')} {e}")

    def save_document(self):
        """Saves the current document as an AmigaGuide file."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".guide",
            title=self.get_label("Save AmigaGuide File"),
            filetypes=[(self.get_label("AmigaGuide Files"), "*.guide"), (self.get_label("All Files"), "*.*")]
        )
        if file_path:
            try:
                content = self.text.get(1.0, tk.END)
                with open(file_path, "w", encoding='latin-1') as file:
                    file.write(content)
                messagebox.showinfo(self.get_label("File"), self.get_label("File saved successfully."))
            except Exception as e:
                messagebox.showerror(self.get_label("Error"), f"{self.get_label('Could not save file:')} {e}")

    def insert_link(self):
        """Inserts a link at the current cursor position."""
        link_text = tk.simpledialog.askstring(self.get_label('Insert Link'), self.get_label('Enter Link Text:'))
        if link_text:
            node_name = tk.simpledialog.askstring(self.get_label('Insert Link'), self.get_label('Enter Node Name:'))
            if node_name:
                link_code = f'@{{"{link_text}" link "{node_name}"}}'
                self.text.insert(tk.INSERT, link_code)

    def insert_image(self):
        """Inserts a uuencoded image at the current cursor position."""
        file_path = filedialog.askopenfilename(
            title=self.get_label("Select Image File"),
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif"), (self.get_label("All Files"), "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "rb") as img_file:
                    img_data = img_file.read()
                # Uuencode the image
                uuencoded_data = self.uuencode_data(img_data, file_path)
                self.text.insert(tk.INSERT, uuencoded_data)
            except Exception as e:
                messagebox.showerror(self.get_label("Error"), f"Could not insert image: {e}")

    def insert_audio(self):
        """Inserts a uuencoded audio file at the current cursor position."""
        file_path = filedialog.askopenfilename(
            title=self.get_label("Select Audio File"),
            filetypes=[("MP3 Files", "*.mp3"), (self.get_label("All Files"), "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "rb") as audio_file:
                    audio_data = audio_file.read()
                # Uuencode the audio
                uuencoded_data = self.uuencode_data(audio_data, file_path)
                self.text.insert(tk.INSERT, uuencoded_data)
            except Exception as e:
                messagebox.showerror(self.get_label("Error"), f"Could not insert audio: {e}")

    def uuencode_data(self, data, filename):
        """Returns uuencoded data as a string."""
        file_basename = filename.split('/')[-1]
        uu_file = io.BytesIO()
        uu.encode(io.BytesIO(data), uu_file, file_basename)
        uuencoded_str = uu_file.getvalue().decode('utf-8')
        return uuencoded_str

    def make_bold(self):
        """Makes the selected text bold."""
        try:
            current_tags = self.text.tag_names("sel.first")
            if "bold" in current_tags:
                self.text.tag_remove("bold", "sel.first", "sel.last")
            else:
                self.text.tag_add("bold", "sel.first", "sel.last")
        except tk.TclError:
            pass  # No text selected

    def make_italic(self):
        """Makes the selected text italic."""
        try:
            current_tags = self.text.tag_names("sel.first")
            if "italic" in current_tags:
                self.text.tag_remove("italic", "sel.first", "sel.last")
            else:
                self.text.tag_add("italic", "sel.first", "sel.last")
        except tk.TclError:
            pass  # No text selected

    def make_underline(self):
        """Underlines the selected text."""
        try:
            current_tags = self.text.tag_names("sel.first")
            if "underline" in current_tags:
                self.text.tag_remove("underline", "sel.first", "sel.last")
            else:
                self.text.tag_add("underline", "sel.first", "sel.last")
        except tk.TclError:
            pass  # No text selected

if __name__ == "__main__":
    root = tk.Tk()
    app = AmigaGuideEditor(root)
    root.geometry("800x600")
    root.mainloop()
