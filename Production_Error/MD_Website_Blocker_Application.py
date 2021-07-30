from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.gridlayout import GridLayout
import WebsiteBlocker
import ctypes, sys
from kivy.uix.image import Image
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import ObjectProperty
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import MDList
from kivymd.uix.list import OneLineListItem
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import ILeftBodyTouch, OneLineIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.icon_definitions import md_icons
from kivy.properties import StringProperty
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

Builder.load_file("newmainApp.kv")


class ListItemWithCheckbox(OneLineIconListItem):
    "Custom List Item"
    pass


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    """Custom Left Container"""
    pass


# Creating a main screen
class MainScreen(Screen):
    pass


# Creating a secondary screen to customize
class CustomizationScreen(Screen):
    pass


class NewMainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs);
        # Screen manager
        self.data_widget = [];
        self.sm = ScreenManager(transition=NoTransition());
        self.mainScreen = MainScreen(name='main');
        self.CustomizationScreen = CustomizationScreen(name='custom');
        self.Website_Blocker = WebsiteBlocker.WebsiteBlocker();
        self.data = self.Website_Blocker.Reading_Database();
        self.sm.add_widget(self.mainScreen);
        self.sm.add_widget(self.CustomizationScreen);
        self.dialog = None;
        menu_items = [{"text": "Social Media"}, {"text": "Adult Content"}, {"text": "All Content"}];

        self.menu = MDDropdownMenu(
            caller=self.mainScreen.ids.auto_Subscription, items=menu_items, width_mult=4,
            callback=self.change_Auto_Subscription
        )
        Clock.schedule_interval(self.update_data, 2)

    def update_data(self, instance):
        self.data_widget = [];
        self.data = self.Website_Blocker.Reading_Database();

        for i in range(5):
            self.data_widget.append(ListItemWithCheckbox(text=f"Item {i}"));

        for item in self.data_widget:
            self.CustomizationScreen.ids.container.add_widget(item);

    def on_checkbox_active(self, checkbox, value):
        if value:
            print('The checkbox', checkbox, 'is active', 'and', checkbox.state, 'state')
        else:
            print('The checkbox', checkbox, 'is inactive', 'and', checkbox.state, 'state')

    # Removing single or multiple data from Selection Behavior Check Box
    def Removing_Unblocking_Data_Using_CheckBox(self):
        # Creating a list to store index that has been selected
        selected_index = []

        # Adding all the selected item to the list
        for item in self.data_widget:
            if item.ids.checkbox.state == "normal":
                pass
            elif item.ids.checkbox.state == "down":
                selected_index.append(self.data_widget.index(item))

        # Checking if the list is empty or not
        if len(selected_index) == 0:
            self.alert_dialog();

        elif len(selected_index) > 0:
            self.confirm_Unblocking_List_Websites_dialog();

    def Removing_Unblocking_List_Data(self):
        # Calling a function to delete a list of websites
        print("Unblocking All the selected websites")
        pass

    # Searching_data
    def search_data(self):
        # Updating the data
        self.Website_Blocker = WebsiteBlocker.WebsiteBlocker();

        # Reading the data
        self.data = self.Website_Blocker.Reading_Database();

        # Checking the data with the text input
        for item in self.data:
            if item == self.CustomizationScreen.ids.website_input.text:
                self.removing_dialog()
                return True
            else:
                continue

        self.adding_dialog()

    # Creating a dialog to add and block a website
    def adding_dialog(self):
        self.dialog = MDDialog(
            text="Adding " + self.CustomizationScreen.ids.website_input.text + "?",
            buttons=[
                MDFlatButton(
                    text='Cancel', on_press=self.dismiss_dialog
                ),
                MDFlatButton(
                    text='Add', on_press=self.Adding_Blocking_data
                ),
            ],
        )
        self.dialog.open()

    # Creating a confirm dialog to remove the websites
    def confirm_Unblocking_List_Websites_dialog(self):
        # Creating a dialog to confirm the user
        self.dialog = MDDialog(
            text="Discard Websites?",
            buttons=[
                MDFlatButton(
                    text='Cancel', on_press=self.dismiss_dialog
                ),
                MDFlatButton(
                    text='Discard', on_press=self.Removing_Unblocking_List_Data
                ),
            ]
        )
        self.dialog.open()

    # Creating a function to add and block a single website
    def Adding_Blocking_data(self, instance):
        # Adding and Blocking a single website

        # Updating the database
        self.refresh_data();

        # Dismiss the dialog
        self.dialog.dismiss();

    # Creating a removing dialog for searching engine
    def removing_dialog(self):
        self.dialog = MDDialog(
            text="Remove " + self.CustomizationScreen.ids.website_input.text + "?",
            buttons=[
                MDFlatButton(
                    text='Cancel', on_press=self.dismiss_dialog
                ),
                MDFlatButton(
                    text='Remove', on_press=self.Remove_Unblock_data
                ),
            ],
        )
        self.dialog.open()

    def alert_dialog(self):
        self.dialog = MDDialog(
            title="Warning",
            text="Nothing has been selected!"
        )
        self.dialog.open();

    def dismiss_dialog(self, instance):
        self.dialog.dismiss()

    def Remove_Unblock_Single_data(self, instance):
        # Remove and Unblock the website from the data

        # Refresh the data
        self.refresh_data();

        # Dismiss the dialog
        self.dialog.dismiss();

    def change_Auto_Subscription(self, instance):
        self.Website_Blocker.SearchingWebsite(type_name=instance.text);
        self.menu.dismiss();

    def build(self):
        # Setting all the default color for the application
        self.theme_cls.theme_style = "Light";
        self.theme_cls.primary_palette = "Blue";
        self.theme_cls.primary_hue = "500";

        return self.sm

    def change_screen(self, screen):
        self.sm.current = screen;


# Running the application
if __name__ == "__main__":
    if WebsiteBlocker.is_admin():
        NewMainApp().run();
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1);
