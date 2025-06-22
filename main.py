import random
import re
from pickle import dump, load
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Better Windows DPI scaling
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

print("Let the learning begin!")

nauka = True
index = 0
skip = False
q = True
q *= -1
file_to_learn = "datasets/EstymacjaOprogramowania.csv"

# --- Color definitions for themes ---
THEMES = {
    "dark": {
        "bg": "#282c34",
        "fg": "#abb2bf",
        "button_bg": "#3e4451",
        "button_fg": "#abb2bf",
        "entry_bg": "#3e4451",
        "entry_fg": "#abb2bf",
        "scrolledtext_bg": "#3e4451",
        "scrolledtext_fg": "#abb2bf",
        "selectcolor": "#3e4451"
    },
    "light": {
        "bg": "#f0f0f0",
        "fg": "#333333",
        "button_bg": "#e1e1e1",
        "button_fg": "#333333",
        "entry_bg": "#ffffff",
        "entry_fg": "#333333",
        "scrolledtext_bg": "#ffffff",
        "scrolledtext_fg": "#333333",
        "selectcolor": "#e1e1e1"
    }
}

current_theme = "dark"


def apply_theme(theme_name):
    global current_theme
    current_theme = theme_name
    theme_colors = THEMES[current_theme]

    root.config(bg=theme_colors["bg"])
    setup_frame.config(bg=theme_colors["bg"])
    learning_frame.config(bg=theme_colors["bg"])

    # Setup Frame Widgets
    nauka_checkbox.config(bg=theme_colors["bg"], fg=theme_colors["fg"],
                          selectcolor=theme_colors["selectcolor"],
                          activebackground=theme_colors["bg"], activeforeground=theme_colors["fg"])
    odnowa_checkbox.config(bg=theme_colors["bg"], fg=theme_colors["fg"],
                           selectcolor=theme_colors["selectcolor"],
                           activebackground=theme_colors["bg"], activeforeground=theme_colors["fg"])
    theme_checkbox.config(bg=theme_colors["bg"], fg=theme_colors["fg"],
                          selectcolor=theme_colors["selectcolor"],
                          activebackground=theme_colors["bg"], activeforeground=theme_colors["fg"])
    wejsciowki_label.config(bg=theme_colors["bg"], fg=theme_colors["fg"])
    wejsciowki_entry.config(bg=theme_colors["entry_bg"], fg=theme_colors["entry_fg"],
                            insertbackground=theme_colors["fg"])
    start_button.config(bg=theme_colors["button_bg"], fg=theme_colors["button_fg"],
                        activebackground=theme_colors["bg"], activeforeground=theme_colors["fg"])

    # Learning Frame Widgets
    save_button.config(bg=theme_colors["button_bg"], fg=theme_colors["button_fg"],
                       activebackground=theme_colors["bg"], activeforeground=theme_colors["fg"])
    question_label.config(bg=theme_colors["bg"], fg=theme_colors["fg"])
    answer_text.config(bg=theme_colors["scrolledtext_bg"], fg=theme_colors["scrolledtext_fg"],
                       insertbackground=theme_colors["fg"])
    show_answer_button.config(bg=theme_colors["button_bg"], fg=theme_colors["button_fg"],
                              activebackground=theme_colors["bg"], activeforeground=theme_colors["fg"])
    known_button.config(bg=theme_colors["button_bg"], fg=theme_colors["button_fg"],
                        activebackground=theme_colors["bg"], activeforeground=theme_colors["fg"])


def toggle_theme():
    if theme_var.get():  # Jeśli checkbox jest zaznaczony (czyli chcemy ciemny motyw)
        apply_theme("dark")
    else:  # Jeśli checkbox nie jest zaznaczony (czyli chcemy jasny motyw)
        apply_theme("light")


def wczytajPytania(odnowa, nauka, wejsciowki):
    wejsciowka = []
    if len(wejsciowki) > 0:
        l = wejsciowki.split(",")
        for k in l:
            k = k.replace(" ", "")
            if re.fullmatch("[0-9]+", k):
                wejsciowka.append(int(k))
            elif re.fullmatch("[0-9]+-[0-9]+", k):
                numbers = [int(num) for num in k.split("-")]
                for i in range(min(numbers), max(numbers) + 1):
                    wejsciowka.append(i)
    print(wejsciowka)
    questions = []
    if odnowa:
        try:
            with open(file_to_learn, mode='r', encoding='utf-8') as f:
                for line in f:
                    l = line.split(";")
                    l.append(False)
                    l[1] = l[1].replace(r"\n", "\n")

                    if len(wejsciowki) > 0:
                        if int(l[2]) in wejsciowka:
                            questions.append(l)
                    else:
                        questions.append(l)
        except Exception as e:  # Lepsza obsługa błędów, aby zobaczyć co poszło nie tak
            messagebox.showerror("Błąd odczytu pliku",
                                 f"Wystąpił błąd podczas wczytywania pytań z {file_to_learn}: {e}")
            # Zapewnij, że questions jest puste, jeśli wystąpi błąd
            questions = []
    else:
        try:
            with open('Latest.pkl', 'rb') as f:
                questions = load(f)
        except FileNotFoundError:
            messagebox.showerror("Błąd", "Plik Latest.pkl nie znaleziony. Rozpoczynam od początku.")
            with open(file_to_learn, mode='r', encoding='utf-8') as f:
                for line in f:
                    l = line.split(";")
                    l.append(False)
                    if len(wejsciowki) > 0:
                        if int(l[2]) in wejsciowka:
                            questions.append(l)
                    else:
                        questions.append(l)
        except Exception as e:
            messagebox.showerror("Błąd odczytu pliku", f"Wystąpił błąd podczas wczytywania z Latest.pkl: {e}")
            questions = []  # Ustaw na puste, aby uniknąć dalszych błędów

    random.shuffle(questions)
    return questions


def start_learning():
    global nauka, questions, index
    nauka = nauka_var.get()
    odnowa = odnowa_var.get()
    wejsciowki = wejsciowki_entry.get()
    questions = wczytajPytania(odnowa, nauka, wejsciowki)
    if not questions:
        messagebox.showinfo("Brak pytań", "Nie znaleziono pytań do nauki.")
        return
    setup_frame.pack_forget()
    learning_frame.pack(pady=10)
    show_question()


def show_question():
    global index, q
    if index < len(questions):
        question_label.config(text=questions[index][0])
        answer_text.delete(1.0, tk.END)
        answer_text.insert(tk.END, questions[index][1])
        answer_text.pack_forget()
        show_answer_button.config(text="Pokaż odpowiedź")
        q = -1
    else:
        if len(questions) > 0:
            index = 0
            random.shuffle(questions)
            messagebox.showinfo("Wejściówkowo", "Nauka od nowa!")
            show_question()
        else:
            messagebox.showinfo("Wejściówkowo", "Udało Ci się! Wszystko umiesz! Fajrant!")
            root.quit()


def show_answer():
    global q, index
    if q == -1:
        answer_text.pack()
        show_answer_button.config(text="Następne pytanie")
        q *= -1
    else:
        index += 1
        show_question()


def mark_known():
    global index, questions
    if questions and 0 <= index < len(questions):
        del questions[index]

    if not questions:
        messagebox.showinfo("Wejściówkowo", "Udało Ci się! Wszystko umiesz! Fajrant!")
        root.quit()
        return

    if index >= len(questions) and len(questions) > 0:
        index = 0

    show_question()


def save_progress():
    with open("./Latest.pkl", "wb") as f:
        dump(questions, f)
    root.quit()


root = tk.Tk()
root.title("Wejściówkowo")
root.geometry("1250x450")

theme_var = tk.BooleanVar(value=True)  # True = dark theme, False = light theme

setup_frame = tk.Frame(root)
setup_frame.pack(pady=10)

nauka_var = tk.BooleanVar()
odnowa_var = tk.BooleanVar(value=True)

nauka_checkbox = tk.Checkbutton(setup_frame, text="Nauka ostatniej wejściówki", variable=nauka_var)
nauka_checkbox.pack(pady=5)

odnowa_checkbox = tk.Checkbutton(setup_frame, text="Zacznij od początku", variable=odnowa_var)
odnowa_checkbox.pack(pady=5)

theme_checkbox = tk.Checkbutton(setup_frame, text="Ciemny motyw", variable=theme_var, command=toggle_theme)
theme_checkbox.pack(pady=5)

wejsciowki_label = tk.Label(setup_frame, text="Numery wyjściówek:", font=('Helvetica', 13), justify="center")
wejsciowki_label.pack(pady=5)

wejsciowki_entry = tk.Entry(setup_frame, width=50)
wejsciowki_entry.pack(pady=5)

start_button = tk.Button(setup_frame, text="Taaak! Zaczynajmy!", command=start_learning)
start_button.pack(pady=5)

learning_frame = tk.Frame(root)

save_button = tk.Button(learning_frame, text="Zapisz postęp", command=save_progress)
save_button.pack(pady=5)

question_label = tk.Label(learning_frame, text="Witaj, pomogę ci nauczyć się pytanek!", font=('Helvetica', 13),
                          justify="center")
question_label.pack(pady=10)

answer_text = scrolledtext.ScrolledText(learning_frame, font=('Helvetica', 13), height=15, width=150)

show_answer_button = tk.Button(learning_frame, text="Pokaż odpowiedź", command=show_answer)
show_answer_button.pack(pady=5)

known_button = tk.Button(learning_frame, text="Umiem", command=mark_known)
known_button.pack(pady=5)

apply_theme(current_theme)

root.mainloop()