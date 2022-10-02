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
    [sg.Button("Open"), sg.Button("Save"), sg.VerticalSeparator(),
        sg.Button("Extract"), sg.Button("Up"), sg.Button("Down"), sg.Button("Add"), sg.Button("Remove")],
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
                filepath = sg.popup_get_file("Choose the .bin file to edit.")
                editor = Editor(filepath)
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
        
        elif event == 'Extract':
            editor.extract_texture(selected_texture)
        
        elif event == 'Add':
            try:
                filepath = sg.popup_get_file("Choose the texture file to add.")
                editor.add_texture(filepath)
                window['-TABLE-'].update(values=TexInfo_to_TableValues(editor.TexInfo), select_rows=[editor.texture_count-1])
            except Exception as e:
                sg.popup(e)
        
        elif event == 'Remove':
            editor.remove_texture(selected_texture)
            selected_texture = min(selected_texture, editor.texture_count-1)
            window['-TABLE-'].update(values=TexInfo_to_TableValues(editor.TexInfo), select_rows=[selected_texture])
            
    
    window.close()
