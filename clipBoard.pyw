import PySimpleGUI as sg
import clipboard

sg.theme('Black')

clipList = ['empty']

notice = sg.Text("Click a item to copy")



layout = [  [sg.Text("clipBoard\n",font='Any 18 bold')],
[sg.Button("Help",tooltip='Press Log to store your clipboard data\nPress Clear to clear the list\nPress Exit to close clipboard')],
    [sg.Button("Log"),sg.Button("Clear"),sg.Button("Exit")] ,[notice] ,
            [sg.Listbox(clipList, size=(30,20), key='-CLIP-', enable_events=True)]
            ]

window = sg.Window('clipBoard', layout,
                    no_titlebar=True,
                    size = (200, 300), 
                    resizable = True,
                    grab_anywhere=True,
                    element_padding=(0, 0),
                    element_justification = "center",
                    keep_on_top=True,
                    location = (0, 0),
                    icon = "clipboard.ico"
                    )

def updateList(clipList,value):
    clipList.insert(0, value)
    window['-CLIP-'].update(clipList)

def clearList(clipList):
    clipList =[]
    updateList(clipList,'empty')
    return clipList

while True:                 
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "Clear":
        clipList = clearList(clipList)
    if event == "Log":
        updateList(clipList,clipboard.paste())
    if event == "Help":
        sg.popup('Press Log to store your clipboard data\nPress Clear to clear the list\nPress Exit to close clipboard')
    if values['-CLIP-']:
        notice.update("copied")
        clipboard.copy(str(values['-CLIP-'][0]))
window.close()