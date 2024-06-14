from tkinter import Tk
from text_analysis_app import TextAnalysisApp, LanguageSelectDialog


def main() -> None:

    root = Tk()
    app = TextAnalysisApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
