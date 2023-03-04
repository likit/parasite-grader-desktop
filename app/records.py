import PySimpleGUI as sg

from organisms import organisms, stages


def create_batch_insert_window():
    organism_list = []
    organism_widgets = []
    rows = []
    for n, org in enumerate(organisms, start=0):
        if n % 3 == 0:
            rows.append(
                sg.Checkbox(org, key=org,
                            default=False,
                            size=(18, 1),
                            enable_events=True)
            )
            organism_widgets.append(rows)
            rows = []
        else:
            rows.append(
                sg.Checkbox(org,
                            key=org,
                            default=False,
                            size=(18, 1),
                            enable_events=True)
            )
    if rows:
        organism_widgets.append(rows)

    layout = [
        organism_widgets,
        [sg.Text('Total: '), sg.Text('0', key='-TOTAL-')],
        [sg.Cancel(), sg.Ok()]
    ]

    window = sg.Window('Record Dialog',
                       layout=layout,
                       modal=True,
                       resizable=True,
                       finalize=True,
                       use_default_focus=True,
                       use_ttk_buttons=True
                       )

    while True:
        event, values = window.read()
        if event in [sg.WINDOW_CLOSED, 'Cancel']:
            break
        elif event == 'Ok':
            for key, value in values.items():
                if value:
                    organism_list.append(key)
            break
        else:
            total = len([(key, value) for key, value in values.items() if value])
            window.find_element('-TOTAL-').update(str(total))
            window.refresh()

    window.close()

    return organism_list


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
                    sg.Combo(organisms, key=f'-ORG{i}-', readonly=True, size=(16, 1)),
                    sg.Combo(stages, key=f'-STG{i}-', readonly=True, size=(16, 1)),
                    sg.Checkbox('Rare', key=f'-RARE{i}-', default=False),
                    sg.Combo(organisms, key=f'-KEYORG{i}-', readonly=True, size=(16, 1)),
                    sg.Combo(stages, key=f'-KEYSTG{i}-', readonly=True, size=(16, 1)),
                ],
            )
        else:
            combos.append(
                [
                    sg.Text(f'{i}:'),
                    sg.Combo(organisms, key=f'-ORG{i}-', readonly=True, default_value=item[2], size=(16, 1)),
                    sg.Combo(stages, key=f'-STG{i}-', readonly=True, default_value=item[3], size=(16, 1)),
                    sg.Checkbox('Rare', key=f'-RARE{i}-', default=item[6]),
                    sg.Combo(organisms, key=f'-KEYORG{i}-', readonly=True, default_value=item[4], size=(16, 1)),
                    sg.Combo(stages, key=f'-KEYSTG{i}-', readonly=True, default_value=item[5], size=(16, 1)),
                ],
            )
    layout = [
        [sg.Text('ID'), sg.Text(student_record[1])],
        [sg.Text('Name'), sg.Text(student_record[2])],
        [sg.Button('Quick Select', key='-BATCH-')],
        [
            sg.Text('Organism', justification='center', expand_x=True),
            sg.Text('Stage', justification='center', expand_x=True),
            sg.Text('Correct Organism', justification='center', expand_x=True),
            sg.Text('Correct Stage', justification='center', expand_x=True)
        ],
        *combos,
        [sg.Cancel('Close', button_color='red'), sg.Button('Save')]
    ]

    window = sg.Window('Record Dialog', layout=layout)

    while True:
        event, values = window.read()
        if event in [sg.WINDOW_CLOSED, 'Exit', 'Close']:
            break
        elif event == '-BATCH-':
            organism_list = create_batch_insert_window()
            for n, org in enumerate(organism_list):
                window.find_element(f'-ORG{n}-').update(org)
            window.refresh()
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
