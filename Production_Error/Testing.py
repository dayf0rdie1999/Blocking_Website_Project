from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.icon_definitions import md_icons
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.list import ILeftBodyTouch
from kivymd.uix.list import OneLineIconListItem


KV = '''
<ListItemWithCheckbox>:
    checkbox: checkbox
    
    LeftCheckbox:
        id: checkbox
        on_active: app.on_checkbox_active(*args)


BoxLayout:

    ScrollView:

        MDList:
            id: scroll
            
    MDRectangleFlatButton:
        text: "Checking"
        on_press: app.checking_checkbox()
        
'''


class ListItemWithCheckbox(OneLineIconListItem):
    '''Custom list item.'''


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    '''Custom right container.'''


class MainApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        icons = list(md_icons.keys())
        self.data_widget = [];

        for i in range(5):
            self.data_widget.append(ListItemWithCheckbox(text=f"Item {i}"));

        for item in self.data_widget:
            self.root.ids.scroll.add_widget(item);

    def on_checkbox_active(self, checkbox, value):
        if value:
            print('The checkbox', checkbox, 'is active', 'and', checkbox.state, 'state')
        else:
            print('The checkbox', checkbox, 'is inactive', 'and', checkbox.state, 'state')

    def checking_checkbox(self):
        for item in self.data_widget:
            self.root.ids.scroll.remove_widget(item);

        self.data_widget = []
        for i in range(10):
            self.data_widget.append(ListItemWithCheckbox(text=f"Item {i}"));

        for item in self.data_widget:
            self.root.ids.scroll.add_widget(item);

MainApp().run()