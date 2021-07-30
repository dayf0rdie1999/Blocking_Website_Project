from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.icon_definitions import md_icons
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.list import ILeftBodyTouch
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
import WebsiteBlocker
import sys, ctypes
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import OneLineListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.button import Button
from kivymd.uix.progressbar import ProgressBar
from time import sleep
from kivymd.uix.dropdownitem import MDDropDownItem


class root(MDBottomNavigation):
    pass


class Item(MDBoxLayout):
    pass


class ListItemWithCheckbox(OneLineIconListItem):
    "Custom List Item"
    pass


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    """Custom Left Container"""
    pass


class MyMainApp(MDApp):
    Website_Blocker = WebsiteBlocker.WebsiteBlocker();
    data_widget = []
    dialog = None
    remove_list = []
    selected_text = None;

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "500"

        return Builder.load_file("my.kv")

    def on_start(self):
        menu_items = [{"text": "Social Media"}, {"text": "Adult Content"}, {"text": "All Content"}];

        self.menu = MDDropdownMenu(
            caller=self.root.ids.auto_subscription, items=menu_items, width_mult=4,
            callback=self.set_item
        )
        data = self.Website_Blocker.Reading_Database();
        for item in data:
            self.data_widget.append(ListItemWithCheckbox(text=f" {item}"));

        for widget in self.data_widget:
            self.root.ids.container.add_widget(widget);

    def set_item(self, instance):
        self.root.ids.drop_item.set_item(instance.text)
        self.menu.dismiss()

    def refresh_data(self):
        # Clean the data from the widget
        for widget in self.data_widget:
            self.root.ids.container.remove_widget(widget);

        # Accessing and reading the data again
        self.Website_Blocker = WebsiteBlocker.WebsiteBlocker();
        data = self.Website_Blocker.Reading_Database();

        # Clean the data_widget
        self.data_widget.clear();

        # Adding the data back in
        for item in data:
            self.data_widget.append(ListItemWithCheckbox(text=f" {item}"));

        for widget in self.data_widget:
            self.root.ids.container.add_widget(widget);

    def Unblocking_Removing_List_Website_Calling_Dialog(self):
        self.remove_list.clear()
        # Checking which checkbox has been checked
        for widget in self.data_widget:
            if widget.ids.checkbox.state == "down":
                self.remove_list.append(self.data_widget.index(widget));
            else:
                pass

        if len(self.remove_list) == 0:
            self.alert_dialog(Message="No Websites have been selected")
        else:
            self.removing_block_list_dialog()

    def auto_subscription_dialog(self):
        # Creating a MDDialog to show the progressbar
        self.dialog = MDDialog(
            auto_dismiss= False,
            title="Processing Information",
            text="Beginning the loading process \n \n The procedure is completed when the dialog disappear",
            buttons=[
                MDFlatButton(
                    text='CANCEL', on_press=self.dismiss_dialog
                ),
                MDFlatButton(
                    text='CONFIRM', on_press=self.auto_subscription
                ),
            ],
        )
        self.dialog.open();

    def auto_subscription(self, instance):

        # Searching the websites
        self.Website_Blocker.SearchingWebsite(type_name=self.root.ids.drop_item.current_item);
        # Sorting the websites
        self.Website_Blocker.Sorting_Porn_Website();
        # Importing the websites
        self.Website_Blocker.Importing_Website_To_SQL();
        # Blocking the websites
        self.Website_Blocker.Blocking_Websites();

        # Dismiss the dialog
        self.dialog.dismiss();

    def searching_database(self):
        self.Website_Blocker = WebsiteBlocker.WebsiteBlocker();

        # Reading the data
        data = self.Website_Blocker.Reading_Database();
        # Checking the website whether it is real or not
        if self.root.ids.website_input.text == " ":
            self.alert_dialog(message="Receive No Information")
        else:
            for website in data:
                if website == self.root.ids.website_input.text:
                    self.removing_dialog()
                    return True;
                else:
                    pass
            Checking = self.Website_Blocker.Check_Website(URL=self.root.ids.website_input.text)
            if Checking == True:
                self.adding_dialog()
                return True
            else:
                pass

    def subscribe_connect_adding_dialog(self):
        Checking = self.Website_Blocker.Check_Website(URL=self.root.ids.website_input.text);
        self.Website_Blocker = WebsiteBlocker.WebsiteBlocker();
        data = self.Website_Blocker.Reading_Database();

        if Checking == True:
            for website in data:
                if self.root.ids.website_input.text == website:
                    self.alert_dialog(Message=f"{self.root.ids.website_input.text} exists in the blocking list")
                    break;
                else:
                    pass
            self.adding_dialog();
        else:
            self.alert_dialog(
                Message=f"The URL doesn't exist or {self.root.ids.website_input.text} exists in the blocking list")

    # Creating a dialog to add and block a website
    def adding_dialog(self):
        self.dialog = MDDialog(
            text="Adding " + self.root.ids.website_input.text + "?",
            buttons=[
                MDFlatButton(
                    text='Cancel', on_press=self.dismiss_dialog
                ),
                MDFlatButton(
                    text='Add', on_press=self.Blocking_Single_Website_From_Dialog
                ),
            ],
        )
        self.dialog.open()

    # Blocking a single website
    def Blocking_Single_Website_From_Dialog(self, instance):
        self.Website_Blocker.Blocking_Single_Website(self.root.ids.website_input.text);
        self.refresh_data();
        self.root.ids.website_input.text = "";
        self.dialog.dismiss();

    # Alerting the user something that they are missing
    def alert_dialog(self, Message):
        self.dialog = MDDialog(
            title="Warning",
            text=Message
        )
        self.dialog.open();

    # Creating a removing dialog for searching engine
    def removing_dialog(self):
        self.dialog = MDDialog(
            text="Remove " + self.root.ids.website_input.text + "?",
            buttons=[
                MDFlatButton(
                    text='Cancel', on_press=self.dismiss_dialog
                ),
                MDFlatButton(
                    text='Remove', on_press=self.Removing_Single_Website
                ),
            ],
        )
        self.dialog.open()

    def Removing_Single_Website(self, instance):
        self.Website_Blocker.Unblocking_Single_Website(website_name=self.root.ids.website_input.text);
        self.refresh_data();
        self.root.ids.website_input.text = ""
        self.dialog.dismiss();

    # Creating a dialog for removing multiple websites
    def removing_block_list_dialog(self):
        widget = Item();
        for num in self.remove_list:
            widget.ids.scroll.add_widget(OneLineListItem(text=f"{self.data_widget[num].text}"))

        self.dialog = MDDialog(
            auto_dismiss=False,
            title="Blocking Websites",
            type="custom",
            content_cls=widget,
            buttons=[
                MDFlatButton(
                    text="CANCEL", on_press=self.dismiss_dialog
                ),
                MDFlatButton(
                    text="CONFIRM", on_press=self.removing_Unblocking_List_Website
                ),
            ],
        )
        self.root.ids.website_input.text = ""
        self.dialog.open()

    def removing_Unblocking_List_Website(self, instance):
        data = self.Website_Blocker.Reading_Database();
        remove_website_list = []

        for num in self.remove_list:
            remove_website_list.append(data[num]);

        self.Website_Blocker.Unblocking_Multiple_Selected_Website(Website_list=remove_website_list);
        self.refresh_data();
        self.dialog.dismiss();

    # Creating a dialog to dismiss the dialog
    def dismiss_dialog(self, instance):
        self.dialog.dismiss()
        self.root.ids.website_input.text = ""


if __name__ == "__main__":
    if WebsiteBlocker.is_admin():
        MyMainApp().run();
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1);
