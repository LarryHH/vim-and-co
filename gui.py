from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog, StringVar, OptionMenu
import pandas as pd
import csv

dict_arr = []


def load_csv(fp: str, col_one: int, col_two: int):
    with open(fp, mode='r', encoding="utf8") as inp:
        reader = csv.reader(inp)
        dict_arr.append({rows[col_one]: rows[col_two] for rows in reader})


def update():
    try:
        dict_arr[1].update(dict_arr[0])
        data = dict_arr[1].items()
        pd.DataFrame(data=data).to_csv(
            "UPDATED_INVENTORY.csv", index=False, header=None)
        print('created updated file')
        create_csv.config(text='✅ CSV created')
        create_csv.config(bg='#d5fcbd')
    except Exception as e:
        print(e)


def processButton(old, new):
    try:
        load_csv(new, 26, 30)
        load_csv(old, 2, 14)
    except Exception as e:
        print(e)
        create_csv.config(text=f"Error: {e}")
        create_csv.config(bg='#f55858')
        help_button.place_configure(x=40.0,
                                    y=286.0,
                                    width=420.0,
                                    height=30.0)

    update()


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.title("Vim & Co. Website Stock Updater")
window.geometry("500x341")
window.configure(bg="#FFFFFF")


canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=341,
    width=500,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)


WEB_EXPORT = ''
STOCK_EXPORT = ''


def select_file(type):
    global WEB_EXPORT, STOCK_EXPORT
    filetypes = [('CSV', '*.csv')]
    filename = filedialog.askopenfilename(
        title='select afile',
        initialdir='./',
        filetypes=filetypes
    )
    if type == "web_export":
        WEB_EXPORT = filename
    else:
        STOCK_EXPORT = filename
    print(f"{type}: {filename}")
    return filename


def button_pressed(button):
    if button == "web_export":
        web_export_button.config(text=select_file(button))
    else:
        inventory_management_export.config(text=select_file(button))


web_export_button = Button(
    text='Click me to select the website export CSV',
    command=lambda: button_pressed("web_export"),
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)

web_export_button.place(
    x=40.0,
    y=65,
    width=420.0,
    height=57.0
)

inventory_management_export = Button(
    text='Click me to select the inventory management export CSV',
    command=lambda: button_pressed("inventory_management_export"),
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)

inventory_management_export.place(
    x=40.0,
    y=132.0,
    width=420.0,
    height=57.0
)

create_csv = Button(
    bg='#d5fcbd',
    borderwidth=0,
    highlightthickness=0,
    command=lambda: processButton(WEB_EXPORT, STOCK_EXPORT),
    relief="flat",
    text='Create the updated stock file CSV',
    font='arial 11 bold'
)
create_csv.place(
    x=40.0,
    y=219.0,
    width=420.0,
    height=57.0
)

help_button = Button(
    borderwidth=0,
    highlightthickness=0,
    relief="flat",
    text='Click me to contact Gus for help',
    font='arial 8 bold',
    bg='#8cddfe'
)


window.resizable(False, False)
window.mainloop()
