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
    [sg.Input(key='-FILEPATH-'),
     sg.FileBrowse(key='-FILEBROWSE-', target='-FILEPATH-', file_types=(('Excel', '*.xlsx'),))],
    [sg.Text('Sheet name')],
    [sg.Input('Sheet1', key='-SHEETNAME-'), sg.Button('Open')],
    [sg.Text('Save As')],
    [sg.InputText(key='-SAVE-PATH-'), sg.SaveAs('Browse', file_types=(("Excel", "*.xlsx"),)), sg.Button('Save')],
    [sg.Text('Load Records')],
    [sg.InputText(key='-LOAD-PATH-'), sg.FileBrowse('Browse', file_types=(("Excel", "*.xlsx"),)), sg.Button('Load')],
    [sg.Exit()],
]

window = sg.Window('Parasite Grader', layout=layout, resizable=True)
student_names = []
records = []

while True:
    event, values = window.read()
    if event in ('Exit', sg.WINDOW_CLOSED):
        break
    elif event == 'Open':
        filepath = values['-FILEPATH-']
        for idx, row in pd.read_excel(filepath, sheet_name=values['-SHEETNAME-']).iterrows():
            student_names.append(row.to_list())
        table.update(values=student_names)
        for row in student_names:
            items = []
            for i in range(10):
                items.append([
                    row[1],
                    row[2],
                    None,
                    None,
                    True,
                    True,
                ])
            records.append(items)
    elif event == '-STUDENTTABLE-':
        index = values['-STUDENTTABLE-'][0]
        student_record = student_names[index]
        rec = create_record_window(student_record, records[index])
        records.pop(index)
        records.insert(index, rec)
    elif event == 'Save':
        data_rows = []
        for rec in records:
            data_rows += [*rec]
        df = pd.DataFrame(data_rows)
        df.to_excel(values['-SAVE-PATH-'], index=False)
    elif event == 'Load':
        if not student_names:
            sg.popup_error('Students name not found.\nPlease load the student file and try again.')
            window['-LOAD-PATH-'].update('')
            continue
        records = []
        file_path = values['-LOAD-PATH-']
        df = pd.read_excel(file_path)
        items = []
        current_id = None
        for idx, row in df.fillna('').iterrows():
            if current_id is None:
                items.append(row.to_list())
                current_id = row[1]
            elif row[1] == current_id:
                items.append(row.to_list())
            else:
                records.append(items)
                items = [row.to_list()]
                current_id = row[1]
        records.append(items)
        sg.popup_notify('Loaded data successfully.')

window.close()
