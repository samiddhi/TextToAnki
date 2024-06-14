from tkinter import *
from tkinter import Text, Menu
from tkinter import messagebox, ttk

import re
import whisper
import os
import json

from tta_grammar import TextAnalyzer, Lexicon
from transcript_srt import main as transcript_to_srt
from settings_dialog import SettingsDialog, load_default_settings


class LanguageSelectDialog:
    def __init__(self):
        self.root = Tk()
        self.root.title("Select Language")
        self.language_var = StringVar()
        self.selected_language = None
        self.create_widgets()

    def create_widgets(self):
        label = ttk.Label(self.root, text="Select Language:")
        label.pack(pady=10)

        options = self.get_folder_names()  # Get folder names dynamically
        dropdown_values = [title for name, title in options]
        self.dropdown_mapping = {title: name for name, title in options}

        dropdown = ttk.Combobox(self.root, textvariable=self.language_var,
                                values=dropdown_values, state='readonly')
        dropdown.pack(pady=10, padx=25)

        default_selection = "SLOVENE"
        if default_selection.title() in dropdown_values:
            self.language_var.set(default_selection.title())

        submit_button = ttk.Button(self.root, text="Submit",
                                   command=self.submit)
        submit_button.pack(pady=10)

        # Bind events
        self.root.bind("<Return>", lambda
            event: submit_button.invoke())  # Trigger button action on Enter key

        dropdown.focus_set()


    def get_folder_names(self):
        base_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..')
        )
        langpack_path = os.path.join(base_path, 'data', 'language_packs')
        if not os.path.exists(langpack_path):
            return []
        folder_names = [name for name in os.listdir(langpack_path) if
                        os.path.isdir(os.path.join(langpack_path, name))]
        return [(name, name.title()) for name in folder_names]

    def submit(self):
        selected_display_name = self.language_var.get()
        if not selected_display_name:
            messagebox.showwarning("Warning", "Please select a language.")
            return
        self.selected_language = self.dropdown_mapping.get(
            selected_display_name)
        self.root.destroy()

    def run(self):
        self.root.mainloop()
        return self.selected_language

class TextAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.settings = load_default_settings()
        selected_language = self.settings.get("language")
        self.root.title(f"The ▪{selected_language.title()}▪ Box")
        self.root.minsize(420, 150)
        self.root.geometry("420x300")


        self.lexicon = Lexicon(selected_language, self.settings)
        self.setup_ui()
        self.create_menu()

    def setup_ui(self):
        # Set minimum size for rows and columns
        for i in range(3):
            self.root.grid_rowconfigure(i, weight=1, minsize=50)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1, minsize=100)

        self.input_text = Text(self.root, undo=True)
        self.input_text.grid(row=0, column=0, columnspan=4, sticky='nsew')
        self.input_text.bind("<Control-z>", lambda event: self.undo())
        self.input_text.bind("<Control-Shift-Z>", lambda event: self.redo())
        self.input_text.bind("<Control-Shift-P>",
                             lambda event: self.open_pystring_dialog())
        self.input_text.bind("<Control-Shift-T>",
                             lambda event: self.remove_timestamps())
        self.input_text.bind("<Control-f>",
                             lambda event: self.open_find_replace())
        self.input_text.bind("<Control-Return>",
                             lambda event: self.run_analysis())

        self.input_text.focus_set()

        self.analysis_type = IntVar(value=1)
        ttk.Radiobutton(self.root, text="Base Words",
                        variable=self.analysis_type,
                        value=1).grid(row=1, column=0, sticky=W)
        ttk.Radiobutton(self.root, text="Word Forms",
                        variable=self.analysis_type,
                        value=2).grid(row=1, column=1, sticky=W)

        self.return_frequencies = IntVar()
        self.freq_check = ttk.Checkbutton(self.root, text="Show Freqs",
                                          variable=self.return_frequencies)
        self.freq_check.grid(row=1, column=2, sticky=W)

        self.run_button = ttk.Button(self.root, text="Get Words",
                                     command=self.run_analysis)
        self.run_button.grid(row=1, column=3, columnspan=1, sticky=W + E)

        self.output_text = Text(self.root)
        self.output_text.grid(row=2, column=0, columnspan=4, sticky='nsew')

        self.scroll = ttk.Scrollbar(self.root, command=self.output_text.yview)
        self.scroll.grid(row=2, column=5, sticky='ns')
        self.output_text['yscrollcommand'] = self.scroll.set

    def create_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="Transcribe Audio",
                              command=self.transcribe_audio)
        file_menu.add_command(label="Transcript -> .srt",
                              command=self.srt)
        file_menu.add_separator()
        file_menu.add_command(label="Settings", command=self.open_settings)

        # Edit Menu
        edit_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit",
                            menu=edit_menu)

        edit_menu.add_command(label="Find & Replace",
                              command=self.open_find_replace)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)
        edit_menu.add_command(label="PyString",
                              command=self.open_pystring_dialog)
        edit_menu.add_command(label="Remove Timestamps",
                              command=self.remove_timestamps)

    # File
    # file (
    def transcribe_audio(self):
        transcriptions: str = "\n".join(whisper.main())
        self.input_text.delete("1.0", END)
        self.input_text.insert("1.0", transcriptions)

    def srt(self):
        input_text = self.input_text.get("1.0", END)
        srt_format: str = transcript_to_srt(input_text)
        self.input_text.delete("1.0", END)
        self.input_text.insert("1.0", srt_format)

    def open_settings(self):
        # Pass the appropriate path to the SettingsDialog instance
        settings_dialog = SettingsDialog(self.root)


    # ) file

    # Edit
    # edit (
    def open_find_replace(self):
        FindReplaceDialog(self.root, self.input_text)

    def undo(self):
        self.input_text.edit_undo()

    def redo(self):
        self.input_text.edit_redo()

    def open_pystring_dialog(self):
        PyStringDialog(self.root, self.input_text)

    def remove_timestamps(self):
        # Get the current text from the input text widget
        input_text = self.input_text.get("1.0", END)

        # Remove timestamps using the regular expression pattern
        updated_text = re.sub(r'\d{2}:\d{2} - ', '', input_text)

        # Replace the text in the input text widget with the updated text
        self.input_text.delete("1.0", END)
        self.input_text.insert("1.0", updated_text)

    # ) edit




    def run_analysis(self):
        text = self.input_text.get("1.0", END)
        analyzer = TextAnalyzer(text, self.lexicon)
        self.output_text.delete("1.0", END)
        result = analyzer.lemma_frequencies if self.analysis_type.get() == 1 else analyzer.token_frequencies
        sorted_items = sorted(result.items(), key=lambda item: item[1],
                              reverse=True)
        for item in sorted_items:
            if self.return_frequencies.get() == 0:
                self.output_text.insert(END, f'{item[0]}\n')
            else:
                self.output_text.insert(END, f'{item[0]}: {item[1]}\n')
        return "break"

class PyStringDialog:
    """Dialog class for running Python code on a string."""

    def __init__(self, parent, text_widget):
        self.top = Toplevel(parent)
        self.text = text_widget
        self.top.title("Edit PyString")
        self.create_widgets()

    def create_widgets(self):
        frame = Frame(self.top)
        frame.pack(padx=10, pady=10)

        Label(frame, text="Python code:").grid(row=0, column=0, sticky=W)
        self.code_entry = Entry(frame, width=50)
        self.code_entry.grid(row=0, column=1, padx=2, pady=2)

        self.code_entry.focus_set()

        Button(frame, text="Run", command=self.run_code).grid(row=1,
                                                              column=0,
                                                              columnspan=2,
                                                              pady=5)
        self.code_entry.bind("<Control-Return>",
                             lambda event: self.run_code())
        self.code_entry.bind("<Return>", lambda event: self.run_code())

    def run_code(self):
        code = self.code_entry.get()
        try:
            result = eval(code, {}, {'box': self.text.get("1.0", END)})
            self.text.delete("1.0", END)
            self.text.insert("1.0", result)
        except Exception as e:
            messagebox.showerror("Error", str(e))

class FindReplaceDialog:
    """Dialog class for find and replace functionality."""

    def __init__(self, parent, text_widget):
        self.top = Toplevel(parent)
        self.text = text_widget
        self.top.title("Find and Replace")
        self.create_widgets()
        self.current_index = None

    def create_widgets(self):
        frame = Frame(self.top)
        frame.pack(padx=10, pady=10)

        Label(frame, text="Find:").grid(row=0, column=0, sticky=W)
        self.find_entry = Entry(frame, width=25)
        self.find_entry.grid(row=0, column=1, padx=2, pady=2)

        self.find_entry.focus_set()

        Label(frame, text="Replace:").grid(row=1, column=0, sticky=W)
        self.replace_entry = Entry(frame, width=25)
        self.replace_entry.grid(row=1, column=1, padx=2, pady=2)

        self.next_button = Button(frame, text="Next",
                                  command=self.find_next)
        self.next_button.grid(row=2, column=0, sticky=W, padx=2, pady=2)

        Button(frame, text="Replace All", command=self.replace_all).grid(
            row=2, column=1, sticky=E, padx=2, pady=2)
        Button(frame, text="Replace One", command=self.replace_one).grid(
            row=2, column=2, sticky=E, padx=2, pady=2)

    def find_next(self):
        self.text.tag_remove("found", "1.0", END)
        find_text = self.find_entry.get()
        start_index = self.current_index if self.current_index else "1.0"
        next_index = self.text.search(find_text, f"{start_index}+1c",
                                      stopindex=END)
        while next_index:
            self.current_index = next_index
            end_index = f"{self.current_index}+{len(find_text)}c"
            self.text.tag_add("found", self.current_index, end_index)
            self.text.tag_configure("found", background="deep sky blue")
            self.current_index = next_index
            next_index = self.text.search(find_text, f"{next_index}+1c",
                                          stopindex=END)
            return  # Exit method if a match is found
        # If no match found, reset to beginning and display message
        self.current_index = None
        messagebox.showinfo("No Matches", "No matches found.")

    def replace_all(self):
        find_text = self.find_entry.get()
        replace_text = self.replace_entry.get()
        content = self.text.get("1.0", END)
        new_content = content.replace(find_text, replace_text)
        self.text.delete("1.0", END)
        self.text.insert("1.0", new_content)

    def replace_one(self):
        if self.current_index:
            find_text = self.find_entry.get()
            replace_text = self.replace_entry.get()
            start_index = self.current_index
            end_index = f"{self.current_index}+{len(find_text)}c"
            self.text.delete(start_index, end_index)
            self.text.insert(start_index, replace_text)
            self.find_next()

