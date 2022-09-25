from tkinter import Entry
from turtle import onkey, onkeypress, textinput
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.dropdown import DropDown

class YourApp(App):
    def build(self):
        root_widget = BoxLayout(orientation='vertical')

        #output_label = Label(size_hint_y=1)

        entries_symbols = ('FTP', 'FTHR')

        entries_grid = GridLayout(cols=1, size_hint_y=None)
        for symbol in entries_symbols:
            entries_grid.add_widget(TextInput(hint_text=symbol, multiline=False))

        root_widget.add_widget(entries_grid)

        profile_label=Label(text='Profile')
        root_widget.add_widget(profile_label)


        
        profile_grid = GridLayout(cols=3, size_hint_y=None)
        profile_grid.add_widget(Label(text="Plutot rouleur"))
        profile_slide=Slider(min=0, max=10, value=5, step=1, orientation='horizontal')
        profile_grid.add_widget(profile_slide)
        profile_grid.add_widget(Label(text="Plutot puncheur"))

        root_widget.add_widget(profile_grid)

        
        dropdown = DropDown()

        device_list=["None1"]

        for index in device_list:
        
            btn = Button(text =index, size_hint_y = None, height = 40)
        
            btn.bind(on_release = lambda btn: dropdown.select(btn.text))
        
            dropdown.add_widget(btn)
        
        mainbutton = Button(text ='Hello', size_hint =(None, None), pos =(350, 300))

        mainbutton.bind(on_release = dropdown.open)
        
        dropdown.bind(on_select = lambda instance, x: setattr(mainbutton, 'text', x))

        root_widget.add_widget(mainbutton)



        def print_button_text(instance,value):
            if int(value)<5:
                profile="Plutot rouleur"
            elif int(value)>5:
                profile="Plutot puncheur"
            else:
                profile="Polyvalent"

            profile_label.text = str("FTP = "+str(entries_grid.children[1].text)+" | FTHR = "+str(entries_grid.children[0].text)+" | Profile = "+str(profile))
        profile_slide.bind(value=print_button_text)

        return root_widget



"""
        def print_button_text(instance):
            output_label.text += instance.text
        for button in button_grid.children[1:]:  # note use of the
                                             # `children` property
            button.bind(on_press=print_button_text)

        def resize_label_text(label, new_height):
            label.font_size = 0.5*label.height
        output_label.bind(height=resize_label_text)

        def evaluate_result(instance):
            try:
                output_label.text = str(eval(output_label.text))
            except SyntaxError:
                output_label.text = 'Python syntax error!'
        button_grid.children[0].bind(on_press=evaluate_result)

        def clear_label(instance):
            output_label.text = ''
        clear_button.bind(on_press=clear_label)

        root_widget.add_widget(output_label)
        root_widget.add_widget(button_grid)
        root_widget.add_widget(clear_button)"""



YourApp().run()