import datetime
import time
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter.messagebox import showinfo

import pandas as pd

# Constants
COL_TIMESTAMP = 'timestamp'
COL_HOST = 'host'
COL_TARGET_HOST = 'target_host'
TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

# Variables
input_data = ''

root = Tk(className=' ')


def open_file():
    global input_data
    input_data = filedialog.askopenfilename(filetypes=[('Text files', '*.txt')])
    process_btn['state'] = 'normal'


def str2timestamp(date):
    return time.mktime(datetime.datetime.strptime(date, TIMESTAMP_FORMAT).timetuple()) * 1000


def timestamp2str(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp / 1000)
    return dt.strftime(TIMESTAMP_FORMAT)[:-3]


def process():
    try:
        columns = [COL_TIMESTAMP, COL_HOST, COL_TARGET_HOST]

        df = pd.read_csv(input_data, sep=' ', names=columns)

        init_datetime = str2timestamp(init_datetime_entry.get())
        end_datetime = str2timestamp(end_datetime_entry.get())

        df_result = df[(df[COL_TIMESTAMP] >= init_datetime) \
                        & (df[COL_TIMESTAMP] <= end_datetime) \
                        & (df[COL_TARGET_HOST] == hostname_entry.get())][COL_HOST]

        output_path = input_data.rsplit('/', 1)[0] + '/01_parse_the_data_output.csv'
        showinfo('File saved', 'Output saved at: ' + output_path)
        df_result.to_csv(output_path, index=False, header=False)
    except:
        showinfo('Format error', 'Date format must be: YYYY-MM-DD :%M:%S.%f')


# GUI
hostname_lbl = Label(text="hostname:")
hostname_entry = ttk.Entry(root)
init_datetime_lbl = Label(text="init_datetime:")
init_datetime_entry = ttk.Entry(root)
end_datetime_lbl = Label(text="end_datetime:")
end_datetime_entry = ttk.Entry(root)
load_file_btn = Button(root, text='Load file', command=open_file, height=1, width=10)
process_btn = Button(root, text="Process", state=DISABLED, command=process, height=1, width=10)

hostname_lbl.grid(row=0, column=0)
hostname_entry.grid(row=0, column=1)
init_datetime_lbl.grid(row=1, column=0)
init_datetime_entry.grid(row=1, column=1)
end_datetime_lbl.grid(row=2, column=0)
end_datetime_entry.grid(row=2, column=1)
load_file_btn.grid(row=3, column=0)
process_btn.grid(row=3, column=1)

root.mainloop()
