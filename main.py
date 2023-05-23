import random
import re
from pickle import dump, load

import PySimpleGUI as sg
from win11toast import notify

# TODO: nic sie nie dzieje jak koniec nauki
# TODO: skalowalność
# TODO: od początku wykładów dodawaj pytania aby wczystko było - skróty itp.
# Skończone wykłady: 5,6,7
# TODO: do niektórych pytań dodajemy zdjęcia - nowa koluman w csv
# TODO: uogólnienie do wielu przedmiotów
# TODO: Bug: pierwsze pytanie po od nowa może być już umiane
# TODO: nauka tylko skrótów
# TODO: opakować te wszystkie if elsy przy przyciskach w metody bo syf się robi
# TODO: Dzieli pytania na zestawy (np po 20) i wtedy uczy dopóki wszystkich nie umie --- nowy tryb pracy do tego

print("Let the learning begin!")

nauka = True
index = 0
skip = False
q = True
q *= -1
subIndex = 0

layout = [[sg.Button("Pokaż odpowiedź", key="-odp-", visible=False), sg.Button("Umiem", key="-wiem-", visible=False)],
          [sg.Text("Witaj, pomogę ci nauczyć się sieci!", key="-pytanie-", justification="center", font=('Helvetica', 13))],
          [sg.Sizer(25, 25)],
          [sg.Multiline("", key="-txtodp-", justification="left", visible=False, font=('Helvetica', 13), size=(300, 3), background_color='#64778d', text_color='white')],
          [sg.Text("", key="-heh-", justification="center", visible=False)],
          [sg.Button("Następne pytanie", key="-nast-", visible=False)],
          [sg.Checkbox("Nauka ostatniej wejściówki", key="-nauka-"),
           sg.Checkbox("Zacznij od początku", key="-odnowa-")],
          [sg.Text("Numery wyjściówek:", key="-txtwej-", justification="center", visible=True, font=('Helvetica', 13)),
           sg.Input(key="-wejsciowki-", expand_x=True)],
          [sg.Button("Taaak! Zaczynajmy!", key="-start-")],
          [sg.Button("Zapisz postęp", key="-zapisz-", visible=False)]
          ]

window = sg.Window("Sieci", layout, size=(1250, 350))


def wczytajPytania(odnowa, nauka, wejsciowki):
    wejsciowka = []
    if len(wejsciowki) > 0:
        l = wejsciowki.split(",")
        for k in l:
            k = k.replace(" ", "")
            if re.fullmatch("[1-9]([0-9]*)?", k):
                wejsciowka.append(int(k))
            elif re.fullmatch("[1-9]([0-9]*)?-[1-9]([0-9]*)?", k):
                numbers = [int(num) for num in k.split("-")]
                # print(type(numbers[1]))
                for i in range(min(numbers), max(numbers) + 1):
                    wejsciowka.append(i)
    print(wejsciowka)
    questions = []
    if odnowa:
        try:
            with open('Sieci.csv') as f:
                for line in f:
                    l = line.split(";")
                    l.append(False)
                    if len(wejsciowki) > 0:
                        if int(l[2]) in wejsciowka:
                            questions.append(l)
                    else:
                        questions.append(l)
        except:
            print(line)
    else:
        with open('Sieci.pkl', 'rb') as f:
            questions = load(f)
    random.shuffle(questions)
    # for row in questions:
    #     try:
    #         print(row[3])
    #     except:
    #         print(row)
    return questions


while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == "-start-":
        window["-nauka-"].update(visible=False)
        nauka = window["-nauka-"].get()
        odnowa = window["-odnowa-"].get()
        window["-odp-"].update(visible=True)
        window["-start-"].update(visible=False)
        window["-heh-"].update(visible=True)
        window["-zapisz-"].update(visible=True)
        window["-odnowa-"].update(visible=False)
        questions = wczytajPytania(odnowa, nauka, values["-wejsciowki-"])
        window["-wejsciowki-"].update(visible=False)
        window["-pytanie-"].update(questions[index][0])
        window["-txtwej-"].update(visible=False)

    elif event == "-odp-":
        if q == -1:  # pokaż odpowiedz
            window["-txtodp-"].update(questions[index][1])
            window["-txtodp-"].update(visible=True)
            window["-odp-"].update("Następne pytanie")
            window["-heh-"].update(visible=False)
            window["-wiem-"].update(visible=True)

            q *= -1
        else:  # nastepne pytanie
            index += 1
            # print(f"1{questions[:][3]}")
            # print(f"{subIndex / sum(map(lambda x: x == False, [row[3] for row in questions]))*100}%")
            while index < len(questions) and questions[index][-1]:
                index += 1

                # print(f"2{questions[3][:]}")
                # print(f"{subIndex / sum(map(lambda x: x == False, [row[3] for row in questions]))*100}%")
            if index == len(questions):
                index = 0
                random.shuffle(questions)
                print("Od nowa!")
                notify("Sieci", "Nauka od nowa!")
            window["-pytanie-"].update(questions[index][0])
            window["-odp-"].update("Pokaż odpowiedź")
            window["-txtodp-"].update("")
            window["-heh-"].update(visible=True)
            window["-wiem-"].update(visible=False)
            q *= -1
    elif event == "-wiem-":
        questions[index][-1] = True
        index += 1
        subIndex += 1
        # print(f"{subIndex / sum(map(lambda x: x==False, [row[3] for row in questions]))}%")
        while index < len(questions) and questions[index][-1]:
            index += 1
            # print(f"3{questions[3][:]}")
            # print(f"{subIndex / sum(map(lambda x: x == False, [row[3] for row in questions]))*100}%")
        if index == len(questions):
            index = 0
            random.shuffle(questions)
            print("Od nowa!")
            notify("Sieci", "Nauka od nowa!")
        window["-pytanie-"].update(questions[index][0])
        window["-odp-"].update("Pokaż odpowiedź")
        window["-txtodp-"].update("")
        window["-heh-"].update(visible=True)
        window["-wiem-"].update(visible=False)
        q *= -1
    elif event == "-zapisz-":
        with open("./Sieci.pkl", "wb") as f:
            dump(questions, f)
            break
window.close()
