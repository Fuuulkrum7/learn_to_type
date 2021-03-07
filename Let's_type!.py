from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
import pickle
import random
import os
import asyncio
import maze  # подключаем лабиринтодел

on_windows = True
try:
    import winsound
except:
    on_windows = False


userName = ""  # имя игрока. мы же не грубияны!
w = True  # служебная переменная
userData = []  # данные пользователя
lastSave = 0  # место сохранения из файла
save = 0  # место сохранения во время обучения
auther = []  # авторский текст
lessonText = []  # текст-обучалка
x = 0  # координата икс для клавиш
y = 0  # координата игрек для клавиш
i = 0  # индекс
cD = [2, 1]  # с помощью этой переменной меняем конфигурацию окна вывода
check2 = False  # проверка нужно ли проверять букву на корректность
index = 0  # индекс для проверки буквы.
teaching = True  # переменная для проверки нажатия "выйти"
darkMode = -1  # переменная для проверки того, включена ли темная тема
lT = ""  # текст для проверки
allButtons = []  # заготовка для всех кнопок
errors = 0  # счетчик ошибок
nameRoot = ""  # заготовка под окно для ввода имени
colorRoot = ""  # заготовка под окно с цветами
ok = ""
chooseButton = ""
text1 = ""
text2 = ""  # прочие заготовки
my_maze = []  # переменная под лабиринт
x_point = 20  # координата точки по оси х
y_point = 20  # и по у
i_point = 1  # координата в лабиринте по оси у
j_point = 1  # и х
anim = False  # идет ли анимация
userWay = []
delay = 4
pole = None
letters_counter = 0  # счетчик букв в тире
text = None  # буква в тире
l_list = []  # временный список под буквы для тира
now_letter = ""  # буква в тире в данный момент
player_shooted = False  # проверка на факт выстрела
timer = 0  # таймер для тира
game_started = False  # проверка на клик по экрану для начала игры в тир
clav = ["ё", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "/", "", "    ", "й", "ц", "у", "к", "е", "н",
        "г", "ш", "щ", "з", "х", "пропуск", "ъ", "пропуск", "ф", "ы", "в", "а", "п", "р","о","л","д","ж","э","пропуск",
        "я", "ч", "с", "м", "и", "т", "ь", "б", "ю", ".", "пропуск", "ctrl", "W", "alt", " ", "alt", "W", "C", "ctrl"]
# текст для каждой (почти) кнопки
letters = ["й", "ц", "у", "к", "е", "н", "г", "ш", "щ", "з", "х", "ъ", "ф", "ы", "в", "а", "п", "р", "о", "л", "д", "ж",
           "э", "я", "ч", "с", "м", "и", "т", "ь", "б", "ю", "ё", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-",
           "=", "/", ".", ",", "!", """ " """, "+", "_", "?"]

sound = 1  # нужен ли звук

custColorTrue = "cyan"  # кастомный цвет подсветки кнопки
custColorFalse = "red"  # кастомный цвет подсветки ошибки

# список доступных цветов
colors = {
    "голубой": "cyan",
    "красный": "red",
    "случайный цвет": "",
    "белый": "snow",
    "серый": "gray",
    "туманная роза": "misty rose",
    "лавандовый": "lavender",
    "хаки": "khaki",
    "желтый": "yellow",
    "золотистый": "gold",
    "оранжевый": "orange",
    "кораловый": "coral",
    "коричневый": "saddle brown",
    "фиолетовый": "purple",
    "синий": "blue",
    "пестрый синий": "dodger blue",
    "лаймовый": "lime green",
    "бирюзовый": "turquoise",
    "цвет морской волны": "dark sea green",
    "салатовый": "lawn green",
    "оливковый": "olive drab",
    "зеленый": "green",
    "темно-зеленый": "dark green"
}

# небольшое пояснение. В программе часто встречаются записи по типу "if переменная + 1:"
# дело в том, что такие переменные могут иметь значение ИЛИ -1, ИЛИ 1.
# Если в условие передать аргумент, не равный 0, то он будет считаться как True, а если 0 - то как False
# поэтому, если мы прибавим 1 к -1, то получим "ложь", а если к 1 - то "правда"


# из файла извлекаем данные игрока
def getUserData():
    global userData
    try:
        with open("other/userData.dat", "rb") as fp:
            userData = pickle.load(fp)
    except FileNotFoundError:  # Если приложение запущено впервые
        userData = []


# Узнаем место сохранения
def getLastSave():
    global lastSave, userData, save, userName
    try:
        # считываем "сохранение" из списка с данными
        lastSave = userData[0]
    except IndexError:  # если пользователь запустил приложение впервые или стер данные
        lastSave = 0
        userData.append(lastSave)
    save = lastSave
    # открываем доп. файл с сохранением. Использовал для удобства кода, изменяя данное "сохранение"
    # и, плюсом, это подстраховка для случаев с утерей сохранения в главном файле (чего, по идее, быть не может)
    try:
        with open("other/save.dat", "r") as f:
            lastSave = int(f.readline())
        # если сохрание из главного файла меньше, чем из доп., меняем его
        if save < lastSave:
            save = lastSave
    except FileNotFoundError:
        pass


# получаем имя. Если его нет, запускаем метод ввода имени nameInput()
def getName():
    global userName, userData, x, w
    try:
        # извлекаем данные и меняем значение логической переменной
        if not len(userName):
            userName = userData[1]

        w = False
    except IndexError:
        # если элемента в списке нет (т.е., приложение запустили впервые)
        userName = ""
    if len(userName) == 0:
        w = True
        insertTextOut("Здравствуй! Я помогу тебе научиться методу слепой печати. \n"\
                      "Но сначала - введи свое имя, чтобы я мог обращаться к тебе по имени. \n"\
                      "Для этого в появившемся окне введи имя и нажми кнопку запомнить меня", "\n")
        root.after(1000, nameInput)


# получаем индекс для вывода текста
def getSound():
    global sound, userData
    try:
        sound = userData[2]
    except IndexError:
        sound = 1
        userData.append(sound)


# получаем кастомные цвета
def getColors():
    global userData, custColorTrue, custColorFalse
    try:
        if custColorFalse == "red":
            custColorFalse = userData[4]
        if custColorTrue == "cyan":
            custColorTrue = userData[3]
    except IndexError:
        userData += [custColorTrue, custColorFalse]


# получаем переменную для проверки включения/выключения темной темы
def getMode():
    global userData, darkMode
    try:
        darkMode = userData[5]
    except IndexError:
        userData.append(darkMode)
        darkMode = -1


# ввод имени через окно
def nameInput():
    global userName, userData, nameRoot, ok

    def saveName():
        global userName, userData
        userName = name.get()
        if len(userName) > 0:
            try:
                userData[1] = userName
            except IndexError:
                userData.append(userName)
            nameRoot.destroy()
            if w:
                # получаем индекс для текста
                getSound()
                # и кастомные цвета
                getColors()
                # получаем переменную для темной темы
                getMode()
                # запускаем обучение
                start_any_level()
        # данный код был перенесен сюда, так как он запускался в то время, когда пользователь вводил имя

    # создаем окно, задаем геометрию и бла бла бла
    nameRoot = Toplevel(root)
    X = nameRoot.winfo_screenwidth() // 2 - 200 // 2
    Y = nameRoot.winfo_screenheight() // 2 - 100 // 2
    nameRoot.geometry(f"{200}x{100}+{X}+{Y}")
    nameRoot.title("Ввод имени")
    nameRoot.resizable(False, False)

    # переменная для получения текста из поля ввода
    name = StringVar()

    # создаем поле ввода и выводим его на экран
    enterName = Entry(nameRoot, textvariable=name)
    enterName.place(x=100, y=20, anchor="c")

    # создаем кнопку ок
    ok = Button(nameRoot, text="Запомни меня!", command=saveName)  # и кнопку
    ok.place(x=50, y=70)

    # биндим нажатие на энтер
    enterName.bind("<Return>", lambda event: saveName())

    # устанавливаем, если надо, темную тему
    setDarkMode()


# закрыть все к чертям
def CloseIt():
    quit(0)


# звщита от случайного нажатия на выход
def CloseBefore():
    answer = mb.askyesno(title="Выход", message="Вы уверены, что хотите выйти?")
    if answer:
        Close()


# прощаемся и сохраняем данные
def Close():
    global userData, teaching
    # обучение на данный момент все
    teaching = False
    try:  # Сохраняем все
        userData[0] = save
        userData[1] = userName
        userData[2] = sound
        userData[3] = custColorTrue
        userData[4] = custColorFalse
        userData[5] = darkMode
        print(save)
        with open("other/userData.dat", "wb") as fp:
            pickle.dump(userData, fp)
        with open("other/save.dat", "w") as f:
            f.write(str(save))

        # проводим неболльшие корректировки поля вывода
        textOutput["height"] = HEIGHT // 3 * 2 // 31

        # и полоски сбоку
        if len(userName):
            scrollOut.place(x=(WIDTH - 810) // 4 - 12, y=0, height=HEIGHT // 27 * 16)

        # очищаем поле вывода
        textOutput["state"] = "normal"
        textOutput.delete("1.0", END)
        textOutput["state"] = "disable"

        # Прощаемся
        insertTextOut(f"{' '*(WIDTH // 40) + 'До встречи!'}", "")
        root.after(1000, CloseIt)

    except:  # Если что-то пошло не так
        print("Файл не сохранился! АААААААА!")
        quit(0)


# Тут добавляем текст в верхнее окно
def insertTextOut(s, z):
    textOutput["state"] = "normal"
    textOutput.insert(INSERT, s + z*2)
    textOutput.see(END)
    textOutput["state"] = "disable"


# А тут - в нижнее окно
def insertTextIn(s, z):
    textIn["state"] = "normal"
    textIn.insert(INSERT, s + z)
    textIn.see(END)
    textIn["state"] = "disable"


# Здесь удаляем данные
def delit():
    global custColorTrue, custColorFalse, darkMode, teaching, w, index, sound

    answer = mb.askyesno(title="Удаление данных", message="Вы уверены, что хотите удалить данные?"
                                                          "\nПосле удаления данных программа будет перезапущена")

    # если игрок согласен на удаление данных
    if answer:
        try:
            # удаляем файл со всем-всем-всем + доп. сохранение
            os.remove("other/userData.dat")
            os.remove("other/save.dat")

            # обучение пока что окончено
            teaching = False

            # вырубаем темную тему
            darkMode = -1
            setDarkMode()

            # ставим дефолтные цвета
            custColorFalse = "red"
            custColorTrue = "cyan"

            # меняем подсветку кнопок
            for i in range(len(allButtons)):
                allButtons[i]["activebackground"] = custColorTrue

            # удаляем все из текст. полей
            textOutput["state"] = "normal"
            textIn["state"] = "normal"
            textOutput.delete("1.0", END)
            textIn.delete("1.0", END)
            textOutput["state"] = "disable"
            textIn["state"] = "disable"

            # ставим значение пункта меню с тем. темой на не выбрано
            for_checkbutton.set(0)
            for_sound.set(1)

            # обнуляем прочие переменные до дефолта
            index = 0
            sound = 1

            # и пишем, что все ок
            mb.showinfo(title="Успех", message="Данные успешно удалены. Программа перезагружена")
            teaching = True
            w = True

            # если кнопки уже есть на экране, запускаем главный метод
            if len(allButtons):
                main()
        except:
            # в случае ошибки пишем, что что-то пошло не так
            mb.showerror(title="Error", message="Ошибка в удалении данных.")


# выводим все кнопки и тп на экран
def Creating():
    global allButtons, x, y, i, lbl, lbl2

    # расставляем все виджеты
    textIn.place(x=(WIDTH - 810) // 4, y=HEIGHT // 27 * 8)
    scrollIn.place(x=(WIDTH - 810)//4 - 12, y=HEIGHT // 27 * 8, height=HEIGHT // 27 * 16 // 2)
    textOutput.place(x=(WIDTH - 810) // 4, y=0)
    scrollOut.place(x=(WIDTH - 810) // 4 - 12, y=0, height=HEIGHT // 27 * 16)

    forgr = "dodger blue"
    backgr = "white"
    begin = ""

    # если вкл темная тема
    if darkMode + 1:
        forgr = "light blue"
        backgr = "dim gray"

        # переменная для итспользования темных изображений
        begin = "dark_"

    # создаем вируальную клавиатуру
    i = 0
    while y <= 236:
        while x <= 756:
            # если нужно, поставить бекспейс
            if i == 14:
                allButtons.append(Button(root, image=eval(f"{begin}backIm"), activebackground=custColorTrue))
                allButtons[i].place(x=(WIDTH - 810) // 2 + x, y=HEIGHT // 5 * 3 + y)
                x += 54

            # тут - ставим таб
            elif i == 15:
                allButtons.append(Button(root, image=eval(f"{begin}tabIm"), activebackground=custColorTrue))
                allButtons[i].place(x=(WIDTH - 810) // 2 + x, y=HEIGHT // 5 * 3 + y)
                x += 108

            # а тут - энтер
            elif i == 27:
                allButtons.append(Button(root, image=eval(f"{begin}enterIm"), activebackground=custColorTrue))
                allButtons[i].place(x=(WIDTH - 810) // 2 + x + 3, y=HEIGHT // 5 * 3 + y)

            # тут - твердый знак. Он, увы имеет нюансы по местоположению, надо ставиить его на энтер
            elif i == 28:
                allButtons.append(
                    Button(root, compound="center", image=eval(f"{begin}buttonImage"), text=clav[i],
                           activebackground=custColorTrue))
                allButtons[i].place(x=(WIDTH - 810) // 2 + x, y=HEIGHT // 5 * 3 + y)
                x += 108

            # тут ставим капс лок
            elif i == 29:
                allButtons.append(Button(root, image=eval(f"{begin}capsIm"), activebackground=custColorTrue))
                allButtons[i].place(x=(WIDTH - 810) // 2 + x, y=HEIGHT // 5 * 3 + y)
                x += 108

            # здесь мы предохрняемся от установки букв на кнопке энтер
            elif (x == 54 * 13 and y == 118) or (x == 54 * 14 and y == 118):
                x += 54
                i -= 1

            # ставим шифты
            elif i == 41 or i == 52:
                allButtons.append(Button(root, image=eval(f"{begin}shiftIm"), activebackground=custColorTrue))
                allButtons[i].place(x=(WIDTH - 810) // 2 + x, y=HEIGHT // 5 * 3 + y)
                x += 136

            # и пробел
            elif i == 56:
                allButtons.append(Button(root, image=eval(f"{begin}spaceIm"), activebackground=custColorTrue))
                allButtons[i].place(x=(WIDTH - 810) // 2 + x + 2, y=HEIGHT // 5 * 3 + y)
                x += 428

            # ну а тут расставляем прочие кнопки
            else:
                allButtons.append(
                    Button(root, compound="center", image=eval(f"{begin}buttonImage"), text=clav[i],
                           activebackground=custColorTrue,
                           command=lambda n=clav[i]: checking(n)))
                allButtons[i].place(x=(WIDTH - 810) // 2 + x, y=HEIGHT // 5 * 3 + y)
                x += 54

            # ставим фон
            allButtons[i]["fg"] = forgr
            allButtons[i]["bg"] = backgr
            if i < 60:
                i += 1
        y += 59
        x = 0

    # биндим нажатия на клавиши
    root.bind("<Key>", pressKey)

    # удаляем ненужное
    delButton.destroy()
    stButton.destroy()
    brButton.destroy()

    # загружаем каритнку
    if save == 0:
        lbl = PhotoImage(file="other/put_hands.png")
        lbl2 = Label(image=lbl)
        lbl2.bind("<Button-1>", level0_1)
    main()


# меняем цвет
def changeColor():
    global custColorFalse, custColorTrue, colorRoot, chooseButton, text1, text2

    # цвет для правильного нажатия
    def saveColor1(*args):
        global custColorTrue
        color = newColor.get()

        # если выбран не случайный цвет
        if color != "случайный цвет":
            custColorTrue = colors[color]

            # если вдруг в переменной нет названия цвета
            if custColorTrue == "":
                custColorTrue = random.choice(list(colors.values()))

                if custColorTrue == "случайный цвет":
                    custColorTrue = "green yellow"

        # если выбран случайный цвет
        elif len(color) != 0:
            custColorTrue = random.choice(list(colors.values()))
            if custColorTrue == "случайный цвет":
                custColorTrue = "green yellow"
        show1["bg"] = custColorTrue

    # цвет для подсветки ошибки
    def saveColor2(*args):
        global custColorFalse
        color = newColor2.get()

        # если выбран не случайный цвет
        if color != "случайный цвет":
            custColorFalse = colors[color]

            # если вдруг в переменной нет названия цвета
            if custColorFalse == "":
                custColorFalse = random.choice(list(colors.values()))

                if custColorFalse == "случайный цвет":
                    custColorFalse = "tomato"

        # если выбран случайный цвет
        elif len(color) != 0:
            custColorFalse = random.choice(list(colors.values()))
            if custColorFalse == "случайный цвет":
                custColorFalse = "tomato"
        show2["bg"] = custColorFalse

    def closeIt():  # закрываем окно и обновляем параметры
        for i in range(len(allButtons)):
            allButtons[i]["activebackground"] = custColorTrue
        colorRoot.destroy()
        root.update()

    # создаем окно и тд и тп
    colorRoot = Toplevel(root)
    POS_X = colorRoot.winfo_screenwidth() // 2 - 350 // 2
    POS_Y = colorRoot.winfo_screenheight() // 2 - 400 // 2
    colorRoot.geometry(f"{350}x{400}+{POS_X}+{POS_Y}")
    colorRoot.title("Изменение цвета подсветки")
    colorRoot.resizable(False, False)

    # квадратики для визуализации выбранного цвета
    show1 = Label(colorRoot, width=8, height=4, bg=custColorTrue)
    show1.place(x=250, y=40)

    show2 = Label(colorRoot, width=8, height=4, bg=custColorFalse)
    show2.place(x=250, y=240)

    # тупо надписи выбранный цвет
    text1 = Label(colorRoot, text="Выбранный цвет:")
    text2 = Label(colorRoot, text="Выбранный цвет:")

    text1.place(x=10, y=10)
    text2.place(x=10, y=210)

    # переменные для выбора цвета
    newColor = StringVar()
    newColor2 = StringVar()

    # выпадающие списки для выбора цвета
    cmbx1 = ttk.Combobox(colorRoot)
    cmbx2 = ttk.Combobox(colorRoot)

    # выбираем состояние только чтение
    cmbx1["state"] = "readonly"
    cmbx2["state"] = "readonly"

    # выводим на экран
    cmbx1.place(x=10, y=30)
    cmbx1["textvariable"] = newColor

    cmbx2.place(x=10, y=230)
    cmbx2["textvariable"] = newColor2

    # доступные краски
    cmbx1["values"] = list(colors.keys())
    cmbx2["values"] = list(colors.keys())

    # устанавливаем открытие с текщего цвета
    cmbx1.current(list(colors.values()).index(custColorTrue))
    cmbx2.current(list(colors.values()).index(custColorFalse))

    # выбираем функцию, что будет вызвана при выборе цвета
    cmbx1.bind("<<ComboboxSelected>>", saveColor1)
    cmbx2.bind("<<ComboboxSelected>>", saveColor2)

    # создаем кнопку... Не поверите... ок для выбора цветов
    chooseButton = Button(colorRoot, text="    Ок    ", font="arial 10", command=closeIt)
    chooseButton.place(x=280, y=350)

    # подрубаем, если надо, темную тему
    if darkMode + 1:
        setDarkMode()

    # биндим нажатие на энтер
    colorRoot.bind("<Return>", lambda event: closeIt())


# смена цветов под темную тему
# здесь мы просто меняем цвет всех видимых элементов.
# лень писать про каждый элемент
def setDarkMode():
    if darkMode + 1:
        textOutput["bg"] = "dim grey"
        textIn["bg"] = "dim grey"
        root["bg"] = "dim gray"
        textOutput["fg"] = "white"
        textIn["fg"] = "white"
        scrollOut["bg"] = "dim gray"
        scrollIn["bg"] = "dim gray"
        if not (len(allButtons)):
            stButton["bg"] = "dim grey"
            stButton["fg"] = "white"
            brButton["bg"] = "dim grey"
            brButton["fg"] = "white"
            delButton["bg"] = "dim grey"
            delButton["fg"] = "white"
        try:
            nameRoot["bg"] = "dim grey"
            ok["bg"] = "dim grey"
            ok["fg"] = "white"
        except:
            pass
        try:
            colorRoot["bg"] = "dim grey"
            text1["bg"] = "dim grey"
            text2["bg"] = "dim grey"

            text1["fg"] = "white"
            text2["fg"] = "white"

            chooseButton["bg"] = "dim grey"
            chooseButton["fg"] = "white"
        except:
            pass
        for i in range(len(allButtons)):
            if i == 14:
                allButtons[i]["image"] = dark_backIm
            elif i == 15:
                allButtons[i]["image"] = dark_tabIm
            elif i == 27:
                allButtons[i]["image"] = dark_enterIm
            elif i == 29:
                allButtons[i]["image"] = dark_capsIm
            elif i == 41 or i == 52:
                allButtons[i]["image"] = dark_shiftIm
            elif i == 56:
                allButtons[i]["image"] = dark_spaceIm
            else:
                allButtons[i]["image"] = dark_buttonImage
            allButtons[i]["fg"] = "light blue"
            allButtons[i]["bg"] = "dim grey"
        root.update()
    else:
        textOutput["bg"] = "white"
        textIn["bg"] = "white"
        root["bg"] = "white"
        textOutput["fg"] = "black"
        textIn["fg"] = "black"
        if not (len(allButtons)):
            stButton["fg"] = "black"
            stButton["bg"] = "white"
            brButton["fg"] = "black"
            brButton["bg"] = "white"
            delButton["fg"] = "black"
            delButton["bg"] = "white"
        try:
            nameRoot["bg"] = "white"
            ok["fg"] = "black"
            ok["bg"] = "white"
        except:
            pass
        try:
            colorRoot["bg"] = "white"
            text1["fg"] = "black"
            text2["fg"] = "black"

            text1["bg"] = "white"
            text2["bg"] = "white"

            chooseButton["fg"] = "black"
            chooseButton["bg"] = "white"
        except:
            pass
        for i in range(len(allButtons)):
            if i == 14:
                allButtons[i]["image"] = backIm
            elif i == 15:
                allButtons[i]["image"] = tabIm
            elif i == 27:
                allButtons[i]["image"] = enterIm
            elif i == 28:
                allButtons[i]["image"] = buttonImage
            elif i == 29:
                allButtons[i]["image"] = capsIm
            elif i == 41 or i == 52:
                allButtons[i]["image"] = shiftIm
            elif i == 56:
                allButtons[i]["image"] = spaceIm
            else:
                allButtons[i]["image"] = buttonImage
            allButtons[i]["fg"] = "dodger blue"
            allButtons[i]["bg"] = "white"
        root.update()


# запуск темной темы из меню
def DarkMode():
    global darkMode
    # меняем значение переменной на обратное
    darkMode *= -1

    # защита от случайностей, когда вдруг (чего быть не может) темная тема включается, но при этом не была отключена
    if root["bg"] == "white" and darkMode == -1:
        darkMode = 1
    setDarkMode()


# игра лабиринт
def make_a_maze(wasd):
    global x_point, y_point, i_point, j_point, pole, my_maze
    # создаем окно
    mazeRoot = Toplevel(root)

    # вычисляем место для окна и устанавиваем его "геометрию"
    POS_X = WIDTH // 2 - 1020 // 2
    POS_Y = HEIGHT // 2 - 500 // 2
    mazeRoot.geometry(f"{1020}x{500}+{POS_X}+{POS_Y}")

    # имя окна
    mazeRoot.title(f"Лабиринт. Управление: {wasd[0]} - вперед, {wasd[1]} - назад, {wasd[2]} - влево,  "
                   f"{wasd[3]} - вправо")

    # устанавливаем цвет фона, если темная тема включена, ставим темный фон
    mazeRoot["bg"] = "white"
    if darkMode + 1:
        mazeRoot["bg"] = "dim grey"

    # запрещаем изменение размеров окна
    mazeRoot.resizable(False, False)

    # создаем лабиринт с заданными параметрами
    my_maze = maze.createMaze(width=51, height=25)

    # переменная для проверки победил ли игрок
    won = False

    # странное название у переменной... Словарь для определения того, как изменятся координаты игрока
    # при нажатии на ту или иную клавишу
    now = {
        1: [-1, 0],
        2: [1, 0],
        3: [0, -1],
        4: [0, 1]
    }

    # единственное место, где используется asyncio. Анимация движения точки
    async def animation(where, won):
        global x_point, y_point, i_point, j_point, anim

        # анимация началась
        anim = True

        # меняем координаты на поле
        x_point += where[1] * 20
        y_point += where[0] * 20

        # меняем координаты в списке
        i_point += where[0]
        j_point += where[1]

        # что-то типа куратины. Меняем координаты точки с задержкой.
        for k in range(18, -2, -2):
            point.place(x=x_point - where[1] * k, y=y_point - where[0] * k)
            mazeRoot.update()
            await asyncio.sleep(0.01)

        # анимация всё
        anim = False

        # если игрок на финише
        if i_point == 23 and j_point == 49:
            # то он победил
            won = True

            # и пора закрыть окно с лабиринтом и написать, что он - молодец.
            mazeRoot.after(500, close)

    # закрываем окно
    def close():
        global save
        mazeRoot.destroy()

        # меняем сохранение
        save += 1

        # хвалим
        insertTextOut("Отлично!", '\n')

        # продолжаем мучить его заданиями
        root.after(2000, start_any_level)

    # обработка нажатий на клавишу
    def move(ev, won):
        if not ev in wasd:
            return

        # узнаем, куда двигаться
        where = now[wasd.index(ev) + 1]

        # если соседний элемент списка-поля не стена
        if my_maze[i_point + where[0]][j_point + where[1]] == 1 and not won and not anim:
            # и игрок не выиграл или анимация не запущена
            # запускаем анимацию
            mazeRoot.after(0, asyncio.run(animation(where, won)))

    # создаем переменный под корординаты лабиринта, точнее, его визуальной составляющей
    x = 0
    y = 0
    i = 0

    # расставляем стены
    # создаем канвас
    pole = Canvas(mazeRoot, width=1020, height=500, bg="white")
    pole.pack()

    # пока координата по оси у не дошла до низу
    while y < 500:
        # координата по оси у для списка
        j = 0
        # пока не дошли до правого края окна
        while x < 1020:
            # если на данном месте проход
            if my_maze[i][j] == 1:
                # если это финиш
                if i == 23 and j == 49:
                    pole.create_rectangle(x, y, x + 20, y + 20, fill="red", outline='white')

                # если это старт
                elif i == j == 1:
                    pole.create_rectangle(x, y, x + 20, y + 20, fill="dark green", outline='white')

                # если просто проход
                else:
                    pole.create_rectangle(x, y, x + 20, y + 20, fill="snow", outline='white')

            # если стена
            else:
                pole.create_rectangle(x, y, x + 20, y + 20, fill="dodger blue", outline='white')

            # двигаемся по оси х
            x += 20
            j += 1

        # двигаемся по оси у
        i += 1

        y += 20
        # сбрасываем координаты по оси х
        x = 0

    del x, y, i

    # ставим точку-игрока
    point = Label(mazeRoot, image=pointIm)
    point.place(x=20, y=20)

    # подключаем обработку нажатий
    mazeRoot.bind("<Key>", lambda event: move(event.char, won))


# тир
def shoot_range(letters_list):
    global letters_counter, text, l_list, now_letter, errors

    # Я ленив. Увы. Мне лень писать буквы под тир большими в файле. Поэтому делаю их таковыми тут
    for j in range(len(letters_list)):
        letters_list[j] = letters_list[j].upper()

    # делаем копию списка из букв для тира
    # это нужно, т.к. отсюда буквы будут удаляться
    l_list = list(letters_list)

    # и перемешиваем их
    random.shuffle(l_list)

    # запоминаем нашу нынешнюю букву-мишень
    now_letter = l_list[0]

    letters_counter = (len(letters_list) * random.randint(2, 4))

    # старт. Проверка на факт клика по окну. Если да, запускаем главный цикл.
    # Дело вот в чем - если это не сделать, но окно будет не выбрано, при этом таймер пойдет
    # При всем при том буквы не будут вводиться. Точнее, выстрелов не будет
    def st():
        global game_started, player_shooted
        if not game_started:
            game_started = True
            player_shooted = False
            update(0)

    # выбор новой буквы, удаление пулевого отверстия и т.д.
    def new_letter(hole, player_sh):
        global letters_counter, text, l_list, now_letter, errors, save, player_shooted, game_started

        # если выстрелил игрок, удаляем дырку от пули
        if (player_sh):
            pole.delete(hole)
        else:
            # иначе увеличиваем счетчик ошибок на 1, обновляем число ошибок, точнее, штрафов
            errors += 1
            er_label["text"] = f"Штрафов: {errors}"

        letters_counter -= 1  # это число мишеней. Уменьшаем его на 1

        # если мы уже не по всем мишеням выстрелили
        if (letters_counter > 0):
            # удаляем мишень, точнее, букву
            pole.delete(text)

            # если буквы в списке закончились
            if (len(l_list) == 0):
                # обновляем список, закидываем туда буквы и перемешиваем. *Подавать горячими*
                l_list = list(letters_list)
                random.shuffle(l_list)
            # пересоздаем букву-мишень
            text = pole.create_text(500, 235, text=l_list[0], font="Verdana 40")

            # запоминаем, какая буква на экране
            now_letter = l_list[0]

            # и удаляем ее из списка
            l_list.pop(0)

            # сбрасываем значение
            player_shooted = False

            # запускаем основной цикл нашего тира
            update(0)
        # если отстрелялись
        else:
            # удаляем окно
            shoot_root.destroy()

            # обнуляем значения *берем пример с Владимира Владимировича*
            game_started = False

            # если игрок оказался косой
            if (errors >= len(letters_list)):
                print("по новой")
                insertTextOut("Прости, но это никуда не годится. Придется перепройти задание", "\n")

                # запускаем по новой
                errors = 0
                root.after(3000, any_task)
            # иначе, если он снайпер и молодец
            else:
                # сохраняем и идем дальше
                save += 1
                if errors > 0:
                    insertTextOut("Отлично! Ты молодец!", "\n")
                else:
                    f = userName
                    if len(userName) < 1:
                        f = "Друг мой"
                    insertTextOut(f"{f}, это было великолепно! Браво)", "\n")
                root.after(1950, clear_text)
                root.after(2000, start_any_level)

    # здесь у нас *у меня* обработка нажатия на клавишу
    def check_shoot(event):
        global player_shooted, errors

        # если буковка в допустимых буковках
        if (event.char.lower() in letters):

            # заносим данные о верности нашего выстрела в переменную
            player_shooted = event.char.upper() == now_letter

            # если игрок косой
            if (not player_shooted):
                # и звук включен и он не линуксе/маке
                if (sound + 1 and on_windows):
                    winsound.PlaySound('other/click.wav', winsound.SND_ALIAS | winsound.SND_ASYNC)

                # обновляем данные об ошибках
                errors += 1
                er_label["text"] = f"Штрафов: {errors}"

    def update(timer):

        # если игрок выстрелил и попал
        if player_shooted:
            # если звук включен и польз. на винде
            if (on_windows and sound + 1):
                # включаем звук выстрела
                winsound.PlaySound('other/shot.wav', winsound.SND_ALIAS | winsound.SND_ASYNC)

            # создаем дырку от выстрела
            hole = pole.create_image(random.randint(460, 500), random.randint(190, 250),
                                     image=random.choice(bullet_holes))

            # запускаем функцию вывода новой буквы
            shoot_root.after(1000, lambda h=hole: new_letter(h, True))

        # если выстрела не было
        else:
            # увеличиваем значение таймера и обновляем данные на экране
            timer += 0.01
            t_label["text"] = str(round(timer, 2))

            # если время вышло
            if (round(timer, 2) == 3):
                t_label["text"] = str(timer)
                shoot_root.after(0, lambda: new_letter(None, False))

            # иначе вызываем цикл еще раз
            else:
                shoot_root.after(10, lambda: update(timer))

    # создаем окно
    shoot_root = Toplevel(root)

    # вычисляем позицию и бла бла бла
    POS_X = WIDTH // 2 - 1020 // 2
    POS_Y = HEIGHT // 2 - 500 // 2

    shoot_root.geometry(f"{1020}x{500}+{POS_X}+{POS_Y}")

    shoot_root.title("Тир")

    # создаем канвас
    pole = Canvas(shoot_root, width=1020, height=500, bg="snow")
    pole.place(x=0, y=0)

    # мишень
    pole.create_oval(430, 170, 570, 310, fill="white")

    # букву на мишени
    text = pole.create_text(500, 235, text=l_list[0], font="Verdana 40")

    # удаляем первую букву
    l_list.pop(0)

    # создаем пистолет
    pole.create_image(500, 385, image=digle_image)

    # таймер
    t_label = Label(shoot_root, text="0.00", font="Verdana 30", bg="snow")
    t_label.place(x=900, y=440)

    # счетчик штрафов
    er_label = Label(shoot_root, text="Штрафов: 0", font="Verdana 15", bg="snow")
    er_label.place(x=860, y=30)

    # биндим нажатия на клавиши и клик мышкой по окну
    shoot_root.bind("<Key>", check_shoot)
    shoot_root.bind("<Button-1>", lambda event: st())


# вкл/вкл звука
def changeSound():
    global sound
    sound *= -1


# очистка текстовых полей
def clear_text():
    textOutput["state"] = "normal"
    textIn["state"] = "normal"
    textIn.delete("1.0", END)
    textOutput.delete("1.0", END)
    textOutput["state"] = "disable"
    textIn["state"] = "disable"


# перемешиваем буквы
def shuffleText(j=0, spaces=False, lenght=10):
    # если ндекс не задан
    if j == 0:
        j = save

    # получаемп буквы для перемешивания
    text = list(lessonText[j])

    # пробел
    space = ""

    # если надо, делаем его пробелом
    if spaces:
        space = " "
    textBack = ""

    # мешаем буквы
    for i in range(lenght):
        random.shuffle(text)
        textBack += (''.join(text))

        # если элемент не последний
        if i < lenght - 1:
            # добавляем пробел
            textBack += space

    # возвращаем перемешанный текст
    return textBack


# меняем размеры окна
def changeConfig():
    global cD
    # разворачиваем "конфигурацию"
    cD = cD[::-1]
    textOutput["height"] = HEIGHT // 3 * cD[0] // 31  # проводим неболльшие корректировки размера поля вывода
    scrollOut.place(x=(WIDTH - 810) // 4 - 12, y=0, height=HEIGHT // 27 * cD[0] * 8)  # и полоски сбоку


# загружаем текст
def getText():
    global auther, lessonText
    file0 = "other/auther's_text.txt"
    file1 = "other/lesson_text.txt"

    with open(file0, 'r') as f:
        auther = f.read().split("\n")

    first = []
    second = []
    # здесь происходит перебор списка с текстом.
    # В файле текст под разные уроки разделен "//". Мы удаляем их и формируем двухмерный список
    for i in auther:
        if i != "//":
            second.append(i)
        else:
            first.append(second)
            second = []
    auther = first

    with open(file1, 'r') as f:
        lessonText = f.read().split("\n")


# звук ошибки
def errorSound():
    # если звук включен и польз. на винде
    if sound + 1 and on_windows:
        winsound.Beep(600, 50)
        winsound.Beep(300, 50)


# проверка буквы на наличие ее в слове
def checking(letter):
    global index, save, check2, errors
    # если задание запущено
    if check2:
        # если буква, нажатая польз. - буква, нужная по заданию
        if letter == lT[index]:
            # двигаем индекс
            index += 1

            # добавляем букву
            insertTextIn(letter, "")

            # если текста для перепечатывания равна индексу
            if len(lT) == index:
                # если ошибок у польз. меньше 20
                if errors <= 20:
                    # меняем сохранение
                    save += 1

                    # если польз. совсем молодец
                    if errors <= 3:
                        insertTextOut("Великолепно! Продолжай в том же духе!", "\n")

                    # если польз. просто молодец
                    elif errors <= 5:
                        insertTextOut("Отлично! Ты - молодец.", "\n")

                    # если почти молодец
                    elif errors <= 10:
                        insertTextOut("Неплохо. Но может быть и лучше. Я уверен, что у тебя все получится", "\n")

                    # если не очень молодец
                    elif errors <= 15:
                        insertTextOut("Откровенно говоря, не очень. Стоит больше стараться", "\n")

                    # если совсем не молодец и был на грани
                    else:
                        insertTextOut("Мда. Плохо. Как так-то? У тебя все получится, но тебе нужно больше тренироваться"
                                      , "\n")

                    # меняем конфиг. окна обратно
                    changeConfig()

                    # заврешаем задание и сбрасываем значения переменных
                    check2 = False
                    errors = 0
                    index = 0

                    # запускаем след. кровень
                    root.after(3000, start_any_level)

                # если польз. наделал ошибок
                else:
                    # "давай по новой, Миша! Все..." (отсылка к мему)
                    insertTextOut("Прости, но это никуда не годится. Придется перепройти задание", "\n")
                    insertTextIn("\n", "\n")
                    errors = 0
                    index = 0
                    check2 = False

                    # сброс значений до дефолта и перезапуск уровня
                    root.after(3000, any_task)

        # если игрок нажал не ту букву
        else:
            errors += 1


# выключаем подсветку кнопки
def stopRgb(bN):
    # если темная тема
    if darkMode == 1 or root["bg"] == "dim grey":
        allButtons[bN]["bg"] = "dim grey"
        allButtons[bN]["fg"] = "light blue"

    # если нет
    else:
        allButtons[bN]["bg"] = "white"
        allButtons[bN]["fg"] = "dodger blue"
    root.update()


# включаем подсветку кнопки
def rgb(buttonNumber, letter):
    # если идет задание и нажатая буква не английская и тд
    if check2 and (letter.lower() in letters) and letter != lT[index]:
        # подсветка нажатой клавиши
        allButtons[buttonNumber]["bg"] = custColorFalse
        allButtons[buttonNumber]["fg"] = custColorFalse
        root.update()

        # остановка подсветки и включение звука ошибки
        root.after(100, lambda b=buttonNumber: stopRgb(b))
        root.after(0, errorSound)

    # иначе просто подсвечиваем клавишу стандартным цветом
    else:
        allButtons[buttonNumber]["bg"] = custColorTrue
        allButtons[buttonNumber]["fg"] = custColorTrue
        root.update()

        # вырубаем подсветку
        root.after(100, lambda b=buttonNumber: stopRgb(b))


# переменная, созд. для того, чтобы при нажатии на right alt не светлся как нажатый control
c = True


# обработка нажатий
def pressKey(event):
    global c
    if event.keycode == 8:  # если нажат бекспейс
        rgb(14, "")
    elif event.keycode == 9:  # если нажат таб
        rgb(15, "")
    elif event.keycode == 16:  # если нажат шифт
        rgb(41, "")
        rgb(52, "")
    elif event.keycode == 18:  # если нажат alt
        rgb(55, "")
        rgb(57, "")
        c = False
    elif event.keycode == 17 and c:  # если нажат control
        rgb(53, "")
        rgb(60, "")
    elif event.keycode == 13:  # если нажат энтер
        rgb(27, "")
    elif event.keycode == 20:  # если нажат капслок
        rgb(29, "")
    elif event.keycode == 91:  # если нажатая правая кнопка (не знаю, как зовут ее, со значком винды)
        rgb(54, "")
    elif event.keycode == 92:  # аналогично с предыдущей, только левая
        rgb(58, "")

    # если нажата другая кнопка, проверяем ее на наличие в списке допустимых значений
    elif event.char.lower() in clav or event.char == ',':
        if event.char != ',':
            rgb(clav.index(event.char.lower()), event.char)
        else:
            rgb(clav.index('.'), event.char)
        checking(event.char)
    elif ord('A') <= ord(event.char) <= ord('z'):  # если нажата английская буква
        checking(event.char)
    elif event.keycode == 27:  # если нажат энтер
        CloseBefore()
    c = True


# -----------------------------
# САМО ОБУЧЕНИЕ
# -----------------------------


# здесь загружаем все, что надо
def main():
    # Получаем данные пользователя
    getUserData()
    # получаем место последнего сохранения
    getLastSave()
    # получаем имя игрока
    getName()
    # получаем тексты
    getText()
    # если мы не запрашиваем имя в этот момент
    if not w:
        # запускаем уровень
        start_any_level()


# подуровень к перовму уровню
# создал его, т.к. в первом уровне я показываю картинку пользователю, и без этого просто не получилось бы
# вывести весь текст так, как мне надо.
def level0_1(j):
    # если запуск через клик по картинке
    if type(j) != int:
        j = 6

    # если идет процесс обучения
    if teaching:
        # если индекс стартовый, который мы ставим при запуске через клик
        if j == 6:
            try:
                lbl2.destroy()
            except:
                pass
            root.update()

        # выводим текст
        insertTextOut(auther[save][j], "\n")
        # увеличиваем индекс
        j += 1
        # если не пора закругляться
        if j < 9:
            root.after(3000, lambda: level0_1(j))

        # иначе запускаем задание
        else:
            root.after(2000, any_task)


def for_usual_task():
    global check2
    # выводим текст
    insertTextOut(lT, "\n")

    # разрешаем обработку нажатий
    check2 = True


# запуск любого задания
def any_task():
    global lT
    if save > 203:
        return
    if save in [1, 5, 11, 20, 27, 30, 40, 43, 52, 57, 62, 66, 76, 95, 109, 117, 125, 132, 138, 147, 154, 161, 173, 176,
                184, 198]:
        number = 3 if len(lessonText[save]) == 4 else int((lambda a: 2 - a // 8)(len(lessonText[save])))

        if number == 0:
            number = 1

        shoot_range(list(shuffleText(lenght=number)))
    elif save in [12, 31, 44, 99, 134]:
        root.after(2000, lambda: make_a_maze(list(lessonText[save])))
    else:
        if " " in lessonText[save]:
            lT = lessonText[save]
        else:
            number = 10 if len(lessonText[save]) == 4 else int((lambda a: 5 + (1 - a // 8) * 3)(len(lessonText[save])))

            if number == 0:
                number = 2

            if save == 0:
                lT = shuffleText(lenght=number)
            else:
                lT = shuffleText(spaces=True, lenght=number)
        root.after(0, changeConfig)
        root.after(50, for_usual_task)


# все уровни
def start_any_level():
    try:
        clear_text()
        text_lenght = len(auther[save])
        if save == 0:
            text_lenght = 6
        level(text_lenght, text_lenght)
    except IndexError:
        pass


def level(j, text_len):
    if teaching:
        insertTextOut(auther[save][text_len - j], "\n")
        j -= 1
        if j > 0:
            root.after(3500, lambda: level(j, text_len))
        else:
            if save == 0:
                root.after(3000, lambda: lbl2.place(x=(WIDTH - 600) // 2, y=(HEIGHT - 400) // 2))
            else:
                root.after(3000, any_task)


# ------------------------------
# СОЗДАЕМ ОКНО
# ------------------------------
root = Tk()
root["bg"] = "white"
WIDTH = root.winfo_screenwidth()  # ширина и высота экрана
HEIGHT = root.winfo_screenheight()
root.attributes('-fullscreen', True)  # делаем экран как у комп.игр
root.title("Let's type!")

# получаем данные игрока
getUserData()

# если список не пустой
if len(userData):
    # получаем сохранение, цвета и бла-бла-бла
    getLastSave()
    getColors()
    getMode()
    getSound()

myMenu = Menu(root)  # создаем менюшку сверху
root.config(menu=myMenu)

# меню настроек
optionsMenu = Menu(myMenu, tearoff=0)
optionsMenu.add_command(label="Сменить имя", command=nameInput)
optionsMenu.add_command(label="Удалить все данные", command=delit)

optionsMenu.add_separator()

for_checkbutton = BooleanVar(root)
for_checkbutton.set((darkMode + 1) // 2)

optionsMenu.add_command(label="Изменить цвет подсветки клавиш", command=changeColor)
optionsMenu.add_checkbutton(label="Темная тема", variable=for_checkbutton, command=DarkMode)

optionsMenu.add_separator()

for_sound = BooleanVar(root)
for_sound.set((sound + 1) // 2)

optionsMenu.add_checkbutton(label="Звук", variable=for_sound, command=changeSound)

optionsMenu.add_separator()

optionsMenu.add_command(label="Выход", command=Close)

# привязываем меню настроек к меню сверху
myMenu.add_cascade(label="Выйти из приложения", command=CloseBefore)
myMenu.add_cascade(label="Настройки", menu=optionsMenu)

# окно ввода
textIn = Text(font="consolas 18", width=WIDTH // 10 * 8 // 13, height=HEIGHT // 3 * 2 // 31 // 2, wrap=WORD)

scrollIn = Scrollbar(command=textIn.yview, width=10)
textIn["yscrollcommand"] = scrollIn.set
textIn["state"] = "disable"

# окно вывода текста заданий
textOutput = Text(font="consolas 18", width=WIDTH // 10 * 8 // 13, height=HEIGHT // 3 * 2 // 31, wrap=WORD)

scrollOut = Scrollbar(command=textOutput.yview, width=10)
textOutput["yscrollcommand"] = scrollOut.set
textOutput["state"] = "disable"

# если список не пустой, получаем имя
if len(userData):
    getName()

# картинки для кнопок
buttonImage = PhotoImage(file="letters/usualButton.png")
enterIm = PhotoImage(file="letters/enter.png")
backIm = PhotoImage(file="letters/backspace.png")
tabIm = PhotoImage(file="letters/tab.png")
shiftIm = PhotoImage(file="letters/shift.png")
capsIm = PhotoImage(file="letters/caps.png")
spaceIm = PhotoImage(file="letters/space.png")


# картинки для темных кнопок
dark_buttonImage = PhotoImage(file="letters/dark_usualButton.png")
dark_enterIm = PhotoImage(file="letters/dark_enter.png")
dark_backIm = PhotoImage(file="letters/dark_backspace.png")
dark_tabIm = PhotoImage(file="letters/dark_tab.png")
dark_shiftIm = PhotoImage(file="letters/dark_shift.png")
dark_capsIm = PhotoImage(file="letters/dark_caps.png")
dark_spaceIm = PhotoImage(file="letters/dark_space.png")

pointIm = PhotoImage(file="other/point.png")

digle_image = PhotoImage(file="other/digle.png")

bullet_holes = []

for i in range(1,6):
    bullet_holes.append(PhotoImage(file=f"other/bullet_hole{i}.png"))

# объявление переменных под картинку
if save == 0:
    lbl = ""
    lbl2 = ""


# создаем стартовые кнопки
stButton = Button(text="Начать обучение", width=15, command=Creating)
brButton = Button(text="Выйти", width=15, command=CloseBefore)
delButton = Button(text="Удалить данные", width=15, command=delit)

stButton.place(x=WIDTH // 2 - 45, y=HEIGHT // 2 - 40)
delButton.place(x=WIDTH // 2 - 45, y=HEIGHT // 2 - 5)
brButton.place(x=WIDTH // 2 - 45, y=HEIGHT // 2 + 30)


# обрабатываем комбинации клавиш
root.bind("<Control_L>"+"d", lambda event: DarkMode())
root.bind("<Control_L>"+"в", lambda event: DarkMode())
root.bind("<Control_L>"+"D", lambda event: DarkMode())
root.bind("<Control_L>"+"В", lambda event: DarkMode())

root.bind("<Control_L>"+"c", lambda event: changeColor())
root.bind("<Control_L>"+"с", lambda event: changeColor())
root.bind("<Control_L>"+"C", lambda event: changeColor())
root.bind("<Control_L>"+"С", lambda event: changeColor())

if darkMode + 1:
    setDarkMode()

root.protocol("WM_DELETE_WINDOW", CloseBefore)
# root.after(0, lambda: make_a_maze(["ц", "ы", "ф", "в"]))
root.mainloop()
