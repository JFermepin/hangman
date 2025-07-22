from tkinter import *
from words import get_random_word, format_word
from constants import INITIAL_LEVEL, DIMENSIONS

class MainWindow:

    def __init__(self):
        # Configure the main window
        self.window = Tk()
        self.window.title("Hangman")
        self.window.geometry(DIMENSIONS)
        self.window.config(bg="black")

        for i in range(3):
            self.window.grid_rowconfigure(i, weight=1)
            self.window.grid_columnconfigure(i, weight=1)

        self.current_language = None
        self.current_level = INITIAL_LEVEL
        self.errors = 0
        self.hangman_image = PhotoImage(file=f"images/hangman-{self.errors}.png")

    def initiate_window(self):
        # Start window with the main menu
        self.show_main_menu()
        self.window.mainloop()

    def show_main_menu(self):
        self.clear_screen()

        # Center container for the main menu
        center_frame = Frame(self.window, bg="black")
        center_frame.grid(row=1, column=1)

        # Main menu UI setup
        main_title = Label(center_frame, text="Hangman", font=("Arial", 24), bg="black", fg="white")
        main_title.pack(pady=20)

        buttons_frame = Frame(center_frame, bg="black")
        buttons_frame.pack()

        spanish_button = Button(buttons_frame, text="Español", command=lambda: self.start_game(INITIAL_LEVEL, "es"), font=("Arial", 16), bg="black", fg="white")
        spanish_button.pack(side=LEFT, padx=20, pady=10)

        english_button = Button(buttons_frame, text="English", command=lambda: self.start_game(INITIAL_LEVEL, "en"), font=("Arial", 16), bg="black", fg="white")
        english_button.pack(side=LEFT, padx=20, pady=10)

    def start_game(self, level, language):
        self.clear_screen()

        # Set the current language and level
        self.current_language = language
        self.current_level = level
        self.errors = 0
        self.hangman_image = PhotoImage(file=f"images/hangman-{self.errors}.png")

        # Fetch a random word based on the level and language
        word = get_random_word(level, language)
        print(word)

        # Game UI setup
        word_frame = Frame(self.window, bg="black")
        word_frame.grid(row=1, column=1)

        word_label = Label(word_frame, text=format_word(word), font=("Arial", 30), bg="black", fg="white", image=self.hangman_image, compound="top", padx=10, pady=10)
        word_label.pack(padx=10, pady=10)

        letters_frame = Frame(self.window, bg="white", highlightbackground="white", highlightthickness=1)
        letters_frame.grid(row=2, column=0, pady=20, columnspan=3)

        letters_label = Label(letters_frame, text="Used letters: ", font=("Arial", 20), bg="black", fg="white")
        letters_label.pack(padx=10, pady=10)

        # Bind key events and logic for the word guessing game
        self.window.bind("<Key>", lambda event: self.guess_letter(event, word_label, letters_label, word))

    def guess_letter(self, event, word_label, letters_label, word):
        letter = event.keysym.lower()
        if not letter.isalpha() or len(letter) != 1:
            return
        if letter in word:
            # Update the displayed word with the guessed letter
            updated_word = format_word(word, word_label.cget("text").replace(" ", ""), letter)
            word_label.config(text=updated_word)
            if "_" not in updated_word:
                self.show_win_message(word)
        else:
            letters_label.config(text=letters_label.cget("text") + " " + letter)
            self.errors += 1
            self.hangman_image = PhotoImage(file=f"images/hangman-{self.errors}.png")
            word_label.config(image=self.hangman_image)
            if self.errors == 6:
                self.show_lose_message(word)

    def show_win_message(self, word):
        self.clear_screen()
        self.window.unbind("<Key>")

        # Center container for the win message
        center_frame = Frame(self.window, bg="black")
        center_frame.grid(row=1, column=1)

        # Win message UI setup
        win_message = Label(center_frame, text=f"Congratulations! The word was: {word}", font=("Arial", 24), bg="black", fg="white", image=self.hangman_image, compound="top", padx=10, pady=10)
        win_message.pack(pady=20)

        buttons_frame = Frame(center_frame, bg="black")
        buttons_frame.pack()

        continue_button = Button(buttons_frame, text="Continue", command=lambda: self.start_game(self.current_level + 1, self.current_language), font=("Arial", 16), bg="black", fg="white")
        continue_button.pack(side=LEFT, padx=20, pady=10)

        main_menu_button = Button(buttons_frame, text="Main menu", command=self.show_main_menu, font=("Arial", 16), bg="black", fg="white")
        main_menu_button.pack(side=LEFT, padx=20, pady=10)

    def show_lose_message(self, word):
        self.clear_screen()
        self.window.unbind("<Key>")

        # Center container for the win message
        center_frame = Frame(self.window, bg="black")
        center_frame.grid(row=1, column=1)

        # Win message UI setup
        lose_message = Label(center_frame, text=f"You lose! The word was: {word}", font=("Arial", 24), bg="black", fg="white", image=self.hangman_image, compound="top", padx=10, pady=10)
        lose_message.pack(pady=20)

        buttons_frame = Frame(center_frame, bg="black")
        buttons_frame.pack()

        continue_button = Button(buttons_frame, text="Restart", command=lambda: self.start_game(INITIAL_LEVEL, self.current_language), font=("Arial", 16), bg="black", fg="white")
        continue_button.pack(side=LEFT, padx=20, pady=10)

        main_menu_button = Button(buttons_frame, text="Main menu", command=self.show_main_menu, font=("Arial", 16), bg="black", fg="white")
        main_menu_button.pack(side=LEFT, padx=20, pady=10)
    

    def clear_screen(self):
        # Clear all widgets from the window
        for widget in self.window.winfo_children():
            widget.destroy()
