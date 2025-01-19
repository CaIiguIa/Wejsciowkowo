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
file_to_learn = "datasets/hurtownie.csv"

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
        except:
            print(line)
    else:
        try:
            with open('Latest.pkl', 'rb') as f:
                questions = load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", "Latest.pkl file not found. Starting from scratch.")
            with open(file_to_learn, mode='r', encoding='utf-8') as f:
                for line in f:
                    l = line.split(";")
                    l.append(False)
                    if len(wejsciowki) > 0:
                        if int(l[2]) in wejsciowka:
                            questions.append(l)
                    else:
                        questions.append(l)
    random.shuffle(questions)
    return questions

def start_learning():
    global nauka, questions, index
    nauka = nauka_var.get()
    odnowa = odnowa_var.get()
    wejsciowki = wejsciowki_entry.get()
    questions = wczytajPytania(odnowa, nauka, wejsciowki)
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
            messagebox.showinfo("Wejściówkowo", "Umiesz wszystko! Fajrant!")
            exit()

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
    del questions[index]

    show_question()

def save_progress():
    with open("./Latest.pkl", "wb") as f:
        dump(questions, f)
    root.quit()

root = tk.Tk()
root.title("Wejściówkowo")
root.geometry("1250x450")

setup_frame = tk.Frame(root)
setup_frame.pack(pady=10)

nauka_var = tk.BooleanVar()
odnowa_var = tk.BooleanVar(value=True)

nauka_checkbox = tk.Checkbutton(setup_frame, text="Nauka ostatniej wejściówki", variable=nauka_var)
nauka_checkbox.pack(pady=5)

odnowa_checkbox = tk.Checkbutton(setup_frame, text="Zacznij od początku", variable=odnowa_var)
odnowa_checkbox.pack(pady=5)

wejsciowki_label = tk.Label(setup_frame, text="Numery wyjściówek:", font=('Helvetica', 13), justify="center")
wejsciowki_label.pack(pady=5)

wejsciowki_entry = tk.Entry(setup_frame, width=50)
wejsciowki_entry.pack(pady=5)

start_button = tk.Button(setup_frame, text="Taaak! Zaczynajmy!", command=start_learning)
start_button.pack(pady=5)

learning_frame = tk.Frame(root)

save_button = tk.Button(learning_frame, text="Zapisz postęp", command=save_progress)
save_button.pack(pady=5)

question_label = tk.Label(learning_frame, text="Witaj, pomogę ci nauczyć się pytanek!", font=('Helvetica', 13), justify="center")
question_label.pack(pady=10)

answer_text = scrolledtext.ScrolledText(learning_frame, font=('Helvetica', 13), height=6, width=100, bg='#64778d', fg='white')

show_answer_button = tk.Button(learning_frame, text="Pokaż odpowiedź", command=show_answer)
show_answer_button.pack(pady=5)

known_button = tk.Button(learning_frame, text="Umiem", command=mark_known)
known_button.pack(pady=5)

root.mainloop()