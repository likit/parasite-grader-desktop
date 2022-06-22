import PySimpleGUI as sg

from organisms import organisms, stages


def create_record_window(student_record, record):
    # check if the record exists
    record = [item for item in record if item[1] == student_record[1]]
    combos = []
    for i in range(0, 10):
        try:
            item = record[i]
        except IndexError:
            combos.append(
                [
                    sg.Text(f'{i}:'),
                    sg.Combo(organisms, key=f'-ORG{i}-', readonly=True),
                    sg.Combo(stages, key=f'-STG{i}-', readonly=True)
                 ],
            )
        else:
            combos.append(
                [
                    sg.Text(f'{i}:'),
                    sg.Combo(organisms, key=f'-ORG{i}-', readonly=True, default_value=item[2]),
                    sg.Combo(stages, key=f'-STG{i}-', readonly=True, default_value=item[3])
                ],
            )
    layout = [
        [sg.Text('ID'), sg.Text(student_record[0])],
        [sg.Text('Name'), sg.Text(student_record[1])],
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
                    student_record[0],
                    student_record[1],
                    values[f'-ORG{i}-'],
                    values[f'-STG{i}-']
                ])
            break

    window.close()
    return record
