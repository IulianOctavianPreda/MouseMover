import PySimpleGUI as sg
from userInput import UserInput
from enums.patterns import Pattern

patterns = [{"key": "Pattern" + str(x.value), "value": x}
            for x in Pattern]
userInput = UserInput()
userInput.addListeners()


def updatePattern(value):
    for pattern in patterns:
        if(pattern["value"] == value):
            window[pattern["key"]].update(True)
        else:
            window[pattern["key"]].update(False)


def time_as_int(time):
    return int(round(time * 100))


sg.theme('DarkBlue')
layout = [
    [sg.Input(visible=False)],
    [sg.Text('Current key combination:', size=(20, 1)),
     sg.Text(size=(20, 1), key='KeyCombination'),
     sg.Button(button_color=("white", "black"),
               button_text='Change', key='ChangeCombination')
     ],
    [sg.Text('Distance in pixels to move:', size=(20, 1)),
     sg.Input(size=(15, 1), key='Distance')
     ],
    [sg.Text('Inactive seconds to wait:', size=(20, 1)),
     sg.Input(size=(15, 1), key='WaitTime')
     ],
    [sg.Text('Duration of the movement:', size=(20, 1)),
     sg.Input(size=(15, 1), key='Duration')
     ],

    [sg.Text('Movement pattern:')] + [sg.Radio(pattern.name, "radio_group1",
                                               key="Pattern" + str(pattern.value)) for pattern in Pattern],
    [sg.Text('Current inactive time:', size=(20, 1)),
     sg.Text(size=(20, 1), key='InactiveTime'),
     sg.Button(button_color=("white", "black"),
               button_text="Update values",  key='Update')
     ],
    [sg.Text(size=(20, 1)),
     sg.Text(size=(20, 1),),
     sg.Button(button_color=("white", "black"),
               button_text="Start",  key='StartStop')
     ]
]


window = sg.Window('Mouse Mover', layout, icon="assets/ico.ico", finalize=True)
window.read(timeout=10)
window['KeyCombination'].update(userInput.keyCombo)
window['Distance'].update(userInput.distance)
window['WaitTime'].update(userInput.waitTime)
window['Duration'].update(userInput.duration)
updatePattern(userInput.patternSelected)
window["WaitTime"].Widget.config(takefocus=1)

while True:  # Event Loop
    event, values = window.read(timeout=10)
    if event in (None, 'Exit'):
        userInput.turnOff()
        break

    if(userInput.isOn):
        window['StartStop'].update("Stop")
        window['InactiveTime'].update('{:02d}:{:02d}.{:02d}'.format((time_as_int(userInput.inactiveTime) // 100) // 60,
                                                                    (time_as_int(
                                                                        userInput.inactiveTime) // 100) % 60,
                                                                    time_as_int(userInput.inactiveTime) % 100))
    else:
        window['StartStop'].update("Start")

    if(userInput.isChangingKeyCombination):
        window['KeyCombination'].update(userInput.keyCombo)

    if event == 'Update':
        userInput.distance = float(values['Distance'])
        userInput.waitTime = float(values['WaitTime'])
        userInput.duration = float(values['Duration'])
        for pattern in patterns:
            if values[pattern["key"]]:
                userInput.patternSelected = pattern["value"]

    if event == 'ChangeCombination':
        if(userInput.isChangingKeyCombination):
            userInput.isChangingKeyCombination = False
            window['ChangeCombination'].update("Change")
        else:
            userInput.isChangingKeyCombination = True
            window['ChangeCombination'].update("Finish")

    if event == 'StartStop':
        if(userInput.isOn):
            userInput.turnOff()
        else:
            userInput.turnOn()


window.close()
