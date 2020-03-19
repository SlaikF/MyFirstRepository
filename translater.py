import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import requests

YA_TOKEN = 'trnsl.1.1.20200228T124248Z.23d3f30fe1bc309f.8c9ccda6143f22ccb6fb89bef10fbdec79b24dca'

# Запрос на Yandex-переводчик
def translate_api_call(text, direction):
    r = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate', params={'key': YA_TOKEN, 'text': text, 'lang': direction})
    if r.status_code != 200:
        raise requests.HTTPError
    return r.json()['text'][0]


# Перевод текста
def translate_text():

    current_tab_index = notebook.index(notebook.select())
    current_tab_object = notebook.winfo_children()[current_tab_index]
    required_tab_object = notebook.winfo_children()[not(current_tab_index)]

    required_tab_object.children['!text'].delete(1.0, tk.END)

    if str(current_tab_object) == '.!notebook.!frame':
        current_lang, required_lang = 'en', 'ru'
        required_tab_name = '.!notebook.!frame2'
    else:
        current_lang, required_lang = 'ru', 'en'
        required_tab_name = '.!notebook.!frame'

    text = current_tab_object.children['!text'].get(1.0, tk.END).rstrip()

    try:
        result = translate_api_call(text, f'{current_lang}-{required_lang}')
    except requests.HTTPError:
        messagebox.showwarning('Warning', 'Yandex.API is not available. Check your network connection')
    else:
        notebook.select(required_tab_name)
        required_tab_object.children['!text'].insert(1.0, result)

# Показывает контекстное меню
def show_context_menu(event):
    menu.post(event.x_root, event.y_root)



root = tk.Tk() #Главное окно
root.title('Ya.Translator')#Название
root.geometry('500x300')#Размер окна
root.resizable(False, False)#Запрет изменения размера главного окна 

#Работа самого переводчика
notebook = ttk.Notebook(root)
frame_en = tk.Frame(notebook)
frame_ru = tk.Frame(notebook)
text_en = tk.Text(frame_en)
text_ru = tk.Text(frame_ru)
button = tk.Button(root, text='Translate!', command=translate_text)

button.pack(side=tk.BOTTOM, fill=tk.X, expand=True)
frame_en.pack(fill=tk.BOTH)
frame_ru.pack(fill=tk.BOTH)
text_en.pack(fill=tk.BOTH)
text_ru.pack(fill=tk.BOTH)

notebook.add(frame_en, text='English')
notebook.add(frame_ru, text='Russian')
notebook.pack(fill=tk.BOTH)

text_en.focus_set()

#Возможности контекстного меню
menu = tk.Menu(root, tearoff=False)
menu.add_command(label="Выделить всё", command=None)
menu.add_separator()
menu.add_command(label="Копировать", command=None)
menu.add_command(label="Вырезать", command=None)
menu.add_command(label="Вставить", command=None)
menu.add_separator()
menu.add_command(label="Очистить", command=None)


#Работа главного меню
menubar = tk.Menu(root)

file_menu = tk.Menu(menubar, tearoff=False)
file_menu.add_command(label="Open", command=None)
file_menu.add_command(label="Close", command=root.quit)
menubar.add_cascade(label="File", menu=file_menu)

language_menu = tk.Menu(menubar, tearoff=False)
language_menu.add_radiobutton(label="En", command=None)
language_menu.add_radiobutton(label="Ru", command=None)
menubar.add_cascade(label="Language", menu=language_menu)

view_menu = tk.Menu(menubar, tearoff = False)
view_menu.add_command(label="Font", command=None)
view_menu.add_command(label="Scale", command=None)
menubar.add_cascade(label="View", menu=view_menu)

help_menu = tk.Menu(menubar, tearoff=False)
help_menu.add_command(label="About", command=None)
help_menu.add_separator()
help_menu.add_command(label="Check for Update", command=None)
menubar.add_cascade(label="Help", menu=help_menu)

root.configure(menu=menubar)#Для показа главного меню
root.bind('<Button-3>', show_context_menu)#Событие для срабатывания контекстного меню

root.mainloop()#Запускает главный цикл обработки событий

