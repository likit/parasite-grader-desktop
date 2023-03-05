from collections import defaultdict, Counter

import PySimpleGUI as sg
import pathlib
import pandas as pd
from records import create_record_window


def print_ascii_bar_chart(data, symbol=":"):
    counter = Counter(data)
    chart = {category: symbol * frequency for category, frequency in counter.items()}
    max_len = max(len(category) for category in chart)
    for category, frequency in chart.items():
        padding = (max_len - len(category)) * " "
        print(f"{category}{padding} |{frequency}")


def create_report_output_window(reports, names, score_dict, organism_counts):
    layout = [
        [sg.Output(size=(80, 20))],
        [sg.Button('Close', button_color='red'), sg.Button('Save')]
    ]

    window = sg.Window('Report', resizable=True, modal=True, finalize=True, layout=layout)

    for stuid in reports:
        message = '-' * 50
        message += f'\n{names[stuid]} {stuid}\n'
        message += '=' * 50
        message += f'\nคะแนน {score_dict.get(stuid)}\n'
        message += '-' * 50
        message += '\nคำตอบ -> เฉลย\n'
        message += '\n'.join(reports[stuid])
        message += '\n'
        print(message)

    print('\nRight answer = +5, rare = 0, wrong genus and species = -2, wrong stage = -1')
    print('\n\nSummary\n')
    print_ascii_bar_chart(answers)
    window.refresh()

    while True:
        event, values = window.read()
        if event in ('Exit', sg.WINDOW_CLOSED, 'Close'):
            break
        elif event == 'Save':
            filepath = sg.popup_get_file('Please select the output file', title='Save As', save_as=True)
            with open(filepath, 'w') as fp:
                for stuid in reports:
                    message = '-' * 50
                    message += f'\n{names[stuid]} {stuid}\n'
                    message += '=' * 50
                    message += f'\nคะแนน {score_dict.get(stuid)}\n'
                    message += '-' * 50
                    message += '\nคำตอบ -> เฉลย\n'
                    message += '\n'.join(reports[stuid])
                    message += '\n\n'
                    fp.write(message)

                fp.write('\n\nRight answer = +5, rare = 0, wrong genus and species = -2, wrong stage = -1\n')
            sg.popup_notify('Saved data successfully', fade_in_duration=0, display_duration_in_ms=500)



    window.close()


sg.theme('BlueMono')
sg.set_options(font=('Helvetica', 18, 'normal'))
table = sg.Table(headings=['No.', 'ID', 'Name'], values=[], expand_x=True, expand_y=True,
                 auto_size_columns=True, display_row_numbers=True,
                 enable_events=True, key='-STUDENTTABLE-')

layout = [
    [sg.Text('Students')],
    [table],
    [sg.Text('Students File')],
    [sg.Input(key='-FILEPATH-'),
     sg.FileBrowse(key='-FILEBROWSE-', target='-FILEPATH-', file_types=(('Excel', '*.xlsx'),))],
    [sg.Text('Sheet name')],
    [sg.Input('Sheet1', key='-SHEETNAME-'), sg.Button('Open')],
    [sg.Text('Save As')],
    [sg.InputText(key='-SAVE-PATH-'), sg.SaveAs('Browse', file_types=(("Excel", "*.xlsx"),)), sg.Button('Save')],
    [sg.Text('Load Records')],
    [sg.InputText(key='-LOAD-PATH-'), sg.FileBrowse('Browse', file_types=(("Excel", "*.xlsx"),)), sg.Button('Load')],
    [sg.Exit(), sg.Button('Tally Up', key='-TALLY-'), sg.Button('View Report', key='-SCORE-REPORT-')],
]

window = sg.Window('Parasite Grader', layout=layout, resizable=True)
student_names = []
records = []
scores = []
score_dict = {}

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
                    None,
                    None,
                    False,
                ])
            records.append(items)
    elif event == '-STUDENTTABLE-':
        index = values['-STUDENTTABLE-'][0]
        student_record = student_names[index]
        rec = create_record_window(student_record, records[index])
        records.pop(index)
        records.insert(index, rec)
    elif event == '-SCORE-REPORT-':
        reports = defaultdict(list)
        names = {}
        answers = []
        for rec in records:
            for stuid, name, ans_org, ans_stage, key_org, key_stage, rare in rec:
                if ans_org:
                    key_org = '' if key_org == ans_org else key_org
                    key_stage = '' if key_stage == ans_stage else key_stage
                    key_stage_report = f'{key_stage} -1' if key_stage else ''
                    # do not show a stage if an organism is not correct
                    if (key_org != '') and (key_org != ans_org):
                        key_stage_report = ''
                    key_org_report = f'{key_org} -2' if key_org else '+5'
                    rare = '(rare)' if rare else ''
                    if key_stage:
                        print(stuid, ans_stage, key_stage)
                        print(key_stage_report)
                        print(f'{ans_org} {ans_stage} -> {key_org_report} {key_stage_report} {rare}')
                    reports[stuid].append(f'{ans_org} {ans_stage} -> {key_org_report} {key_stage_report} {rare}')
                    names[stuid] = name
                    answers.append(ans_org)
        create_report_output_window(reports, names, score_dict, answers)

    elif event == 'Save':
        data_rows = []
        for rec in records:
            data_rows += [*rec]
        df = pd.DataFrame(data_rows)
        save_path = values['-SAVE-PATH-']
        if not pathlib.Path(save_path).suffix:
            save_path = pathlib.Path(save_path + '.xlsx')
        with pd.ExcelWriter(save_path) as Writer:
            df.to_excel(Writer, index=False, sheet_name='records')
            if scores:
                score_df = pd.DataFrame(scores)
                score_df.to_excel(Writer, index=False, sheet_name='scores')
        sg.popup_notify('Data have been saved successfully.', display_duration_in_ms=500, fade_in_duration=0)
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
        window.find_element('-SAVE-PATH-').update(file_path)
        sg.popup_notify('Data have been loaded successfully.', display_duration_in_ms=500, fade_in_duration=0)
    elif event == '-TALLY-':
        scores = []  # reset scores
        score_dict = {}
        for rec in records:
            score = 0
            corrects = set()
            for stuid, name, ans_org, ans_stage, key_org, key_stage, rare in rec:
                if not rare:  # if not rare
                    if ans_org:
                        if key_org and ans_org != key_org:
                            score -= 2
                        else:
                            if ans_org not in corrects:
                                score += 5
                                corrects.add(ans_org)
                    if ans_stage:
                        # do not penalize for a wrong stage if an organism is wrong
                        if (key_org != '') or (key_org == ans_org):
                            if key_stage and ans_stage != key_stage:
                                score -= 1
                            else:
                                score += 0
            scores.append([stuid, name, score])
            score_dict[stuid] = score
        sg.popup_notify('Finished tallying.', display_duration_in_ms=500, fade_in_duration=0)

window.close()
