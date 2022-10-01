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
    [sg.Button("Open"), sg.Button("Save"), sg.VerticalSeparator(), sg.Button("Up"), sg.Button("Down")],
    [table]
]

def TexInfo_to_TableValues(TexInfo):
    return [*[[idx['name'], idx['type']] for idx in TexInfo ]]

if __name__ == '__main__':
    window = sg.Window("GT3PMBBINEditor", layout=layout, size=(640,480));

    selected_texture = 0
    editor = None
    while True:
        event, values = window.read();
        if event in (sg.WIN_CLOSED, 'Exit'):
            break;

        elif event == 'Open':
            try:
                editor = Editor(values['-FILE-'])
                window['-TABLE-'].update(values=TexInfo_to_TableValues(editor.TexInfo), select_rows=[selected_texture])
            except Exception as e:
                sg.popup(e)
        
        elif event == 'Up':
            index = selected_texture
            if(index > 0 and editor != None):
                textures = editor.TexInfo
                textures[index-1], textures[index] = textures[index], textures[index-1]
                editor.TexInfo = textures
                window['-TABLE-'].update(values=TexInfo_to_TableValues(textures), select_rows=[index-1])

        elif event == 'Down':
            index = selected_texture
            if(editor != None and index < editor.texture_count-1 ):
                textures = editor.TexInfo
                textures[index+1], textures[index] = textures[index], textures[index+1]
                editor.TexInfo = textures
                window['-TABLE-'].update(values=TexInfo_to_TableValues(textures), select_rows=[index+1])
                
        elif event == '-TABLE-':
            selected_texture = values['-TABLE-'][0]
        
        elif event == 'Save':
            editor.assemble_and_save("out.bin")
            sg.popup("Saved as "+"out.bin")
    
    window.close()
