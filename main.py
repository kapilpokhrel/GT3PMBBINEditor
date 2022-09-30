import PySimpleGUI as sg
from editor import Editor

table = sg.Table(
    values=[],
    headings=['Name', 'Type'],
    justification='left',
    auto_size_columns=False,
    col_widths=[50, 10],
    expand_x=True,
    expand_y=True,
    enable_events=True,
    key='-TABLE-',
    display_row_numbers=True,
    vertical_scroll_only=False,
    select_mode=sg.TABLE_SELECT_MODE_BROWSE
)
layout = [
    [sg.Text('File: '), sg.In(size=(25,1), enable_events=True ,key='-FILE-'), sg.FileBrowse()],
    [sg.Button("Open")],
    [table]
]

def TexInfo_to_TableValues(TexInfo):
    return [*[[idx['name'], idx['type']] for idx in TexInfo ]]

if __name__ == '__main__':
    window = sg.Window("GT3PMBBINEditor", layout=layout, size=(640,480));

    selected_texture = 0
    while True:
        event, values = window.read();
        if event in (sg.WIN_CLOSED, 'Exit'):
            break;

        elif event == 'Open':
            editor = Editor(values['-FILE-'])
            window['-TABLE-'].update(values=TexInfo_to_TableValues(editor.TexInfo_list), select_rows=[selected_texture])
    
    window.close()
