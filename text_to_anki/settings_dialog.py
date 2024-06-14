import json
import os
from tkinter import Toplevel, Checkbutton, BooleanVar, StringVar, Label, Frame
from tkinter.ttk import Combobox

base_path = os.path.dirname(os.path.dirname(
            os.path.abspath(__file__)))
default_json = os.path.join(base_path, "data", "settings", "default.json")

class SettingsDialog:
    def __init__(self, parent):

        self.top = Toplevel(parent)
        self.top.title("Settings")
        self.default_settings = load_default_settings()
        self.create_widgets()

    def create_widgets(self):
        # Exclusion List Filtering (Checkbox)
        self.exclusion_var = BooleanVar()
        self.exclusion_var.set(
            self.default_settings["exclusion_list_filtering"])

        exclusion_frame = Frame(
            self.top)  # Create a frame to contain the label and checkbutton
        exclusion_frame.pack(anchor="w")

        exclusion_label = Label(exclusion_frame,
                                text="Exclusion List Filtering:")
        exclusion_label.pack(side="left")

        checkbutton = Checkbutton(exclusion_frame, variable=self.exclusion_var)
        checkbutton.pack(side="left")

        # Language (Dropdown Menu)
        language_options = self.get_language_options()  # Get list of language options
        if language_options:
            language_label = Label(self.top, text="Language:")
            language_label.pack(side="left", padx=(5, 0))
            self.language_var = StringVar(value=self.default_settings[
                "language"])  # Provide default value
            combobox = Combobox(self.top, textvariable=self.language_var,
                                values=language_options, width=20)
            combobox.pack(side="left")
        else:
            Label(self.top, text="No language options available").pack()

    def on_language_select(self, value):
        self.default_settings["language"] = value

    def get_language_options(self):
        # Get list of folders in data/language_packs/
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        language_packs_path = os.path.join(base_path, "data", "language_packs")
        print("Searching in:", language_packs_path)  # Print the search path
        language_folders = [name for name in os.listdir(language_packs_path) if
                            os.path.isdir(
                                os.path.join(language_packs_path, name))]
        return language_folders

    def apply_settings(self):
        # Implement logic to apply modified settings
        # Update global variables in tta_grammar module
        pass

    def save_default_settings(self):
        with open(default_json, "w") as file:
            json.dump(self.default_settings, file, indent=4)

    def __del__(self):
        # Save default settings when the dialog is closed
        self.save_default_settings()

    # Add other methods as needed


def load_default_settings() -> dict:
    try:
        with open(default_json, "r") as file:
            default_settings: dict = json.load(file)
    except FileNotFoundError:
        # Initialize default settings if the file doesn't exist
        default_settings = {
            "exclusion_list_filtering": True,
            "language": "slovene",
            # Add more settings as needed
        }
        with open(default_json, "w") as file:
            json.dump(
                default_settings,
                file,
                indent=4
            )
    return default_settings