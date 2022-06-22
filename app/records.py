import PySimpleGUI as sg

from organisms import organisms, stages


def create_record_window(student_record, items):
    # check if the record exists
    print(items)
    record = [item for item in items if item[0] == student_record[1]]
    combos = []
    for i in range(0, 10):
        try:
            item = record[i]
        except IndexError:
            combos.append(
                [
                    sg.Text(f'{i}:'),
                    sg.Combo(organisms, key=f'-ORG{i}-', readonly=True),
                    sg.Combo(stages, key=f'-STG{i}-', readonly=True),
                    sg.Checkbox('ORG:', key=f'-ORG{i}-CHK-', default=True),
                    sg.Checkbox('STAGE:', key=f'-STG{i}-CHK-', default=True),
                ],
            )
        else:
            combos.append(
                [
                    sg.Text(f'{i}:'),
                    sg.Combo(organisms, key=f'-ORG{i}-', readonly=True, default_value=item[2]),
                    sg.Combo(stages, key=f'-STG{i}-', readonly=True, default_value=item[3]),
                    sg.Checkbox('ORG:', key=f'-ORG{i}-CHK-', default=item[4]),
                    sg.Checkbox('STAGE:', key=f'-STG{i}-CHK-', default=item[5]),
                ],
            )
    layout = [
        [sg.Text('ID'), sg.Text(student_record[1])],
        [sg.Text('Name'), sg.Text(student_record[2])],
        *combos,
        [sg.Button('Save')]
    ]

    window = sg.Window('Record Dialog', layout=layout)

    while True:
        event, values = window.read()
        if event in [sg.WINDOW_CLOSED, 'Exit']:
            break
        elif event == 'Save':
            record = []
            for i in range(0, 10):
                record.append([
                    student_record[1],
                    student_record[2],
                    values[f'-ORG{i}-'],
                    values[f'-STG{i}-'],
                    values[f'-ORG{i}-CHK-'],
                    values[f'-STG{i}-CHK-'],
                ])
            break

    window.close()
    return record
