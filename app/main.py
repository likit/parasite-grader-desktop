import PySimpleGUI as sg
import pandas as pd
from records import create_record_window

sg.theme('BlueMono')
table = sg.Table(headings=['No.', 'ID', 'Name'], values=[], expand_x=True, expand_y=True,
                 auto_size_columns=True, display_row_numbers=True,
                 enable_events=True, key='-STUDENTTABLE-')

layout = [
    [sg.Text('Students')],
    [table],
    [sg.Input(key='-FILEPATH-'), sg.FileBrowse(key='-FILEBROWSE-', target='-FILEPATH-', file_types=(('Excel', '*.xlsx'),))],
    [sg.Text('Sheet name')],
    [sg.Input('Sheet1', key='-SHEETNAME-'), sg.Button('Open')],
    [sg.Text('Save As')],
    [sg.InputText(key='-SAVE-PATH-'), sg.SaveAs('Browse', file_types=(("Excel", "*.xlsx"),)), sg.Button('Save')],
    [sg.Exit()],
]

window = sg.Window('Parasite Grader', layout=layout)

while True:
    event, values = window.read()
    if event in ('Exit', sg.WINDOW_CLOSED):
        break
    elif event == 'Open':
        filepath = values['-FILEPATH-']
        rows = []
        for idx, row in pd.read_excel(filepath, sheet_name=values['-SHEETNAME-']).iterrows():
            rows.append(row.to_list())
        table.update(values=rows)
        records = [list() for i in range(len(rows))]
    elif event == '-STUDENTTABLE-':
        index = values['-STUDENTTABLE-'][0]
        student_record = rows[index]
        rec = create_record_window(student_record, records[index])
        records.pop(index)
        records.insert(index, rec)
    elif event == 'Save':
        rows = []
        for rec in records:
            rows += [item for item in rec if item[2] or item[3]]
        df = pd.DataFrame(rows)
        df.to_excel(values['-SAVE-PATH-'], index=False)



window.close()

