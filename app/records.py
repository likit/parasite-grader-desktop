import PySimpleGUI as sg

from organisms import organisms, stages


def create_record_window(student_record, items):
    # check if the record exists
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
                    sg.Checkbox('Rare', key=f'-RARE{i}-', default=False),
                    sg.Combo(organisms, key=f'-KEYORG{i}-', readonly=True),
                    sg.Combo(stages, key=f'-KEYSTG{i}-', readonly=True),
                ],
            )
        else:
            combos.append(
                [
                    sg.Text(f'{i}:'),
                    sg.Combo(organisms, key=f'-ORG{i}-', readonly=True, default_value=item[2]),
                    sg.Combo(stages, key=f'-STG{i}-', readonly=True, default_value=item[3]),
                    sg.Checkbox('Rare', key=f'-RARE{i}-', default=item[6]),
                    sg.Combo(organisms, key=f'-KEYORG{i}-', readonly=True, default_value=item[4]),
                    sg.Combo(stages, key=f'-KEYSTG{i}-', readonly=True, default_value=item[5]),
                ],
            )
    layout = [
        [sg.Text('ID'), sg.Text(student_record[1])],
        [sg.Text('Name'), sg.Text(student_record[2])],
        [
            sg.Text('Organism', justification='center', expand_x=True),
            sg.Text('Stage', justification='center', expand_x=True),
            sg.Text('Correct Organism', justification='center', expand_x=True),
            sg.Text('Correct Stage', justification='center', expand_x=True)
        ],
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
                    values[f'-KEYORG{i}-'],
                    values[f'-KEYSTG{i}-'],
                    values[f'-RARE{i}-'],
                ])
            break

    window.close()
    return record
