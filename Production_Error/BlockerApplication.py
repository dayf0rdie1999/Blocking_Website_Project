from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import ObjectProperty
import WebsiteBlocker
import ctypes, sys
from kivymd.app import MDApp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from Website_Databases import UserDB
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.progressbar import ProgressBar

Builder.load_file("main.kv")


class MainScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update)
        self.bind(size=self.update)
        self.update()

    def update(self, *args):
        global width, length
        width, length = self.size
        with self.canvas:
            pass

    def Subscribe(self):
        self.myPopup = MyPopup();
        self.myPopup.Completion_popup()
        Vu_Com = WebsiteBlocker.WebsiteBlocker();
        Vu_Com.SearchingWebsite();
        self.myPopup.Progress_Bar.value = 25;
        Vu_Com.Sorting_Porn_Website();
        self.myPopup.Progress_Bar.value = 50;
        Vu_Com.Importing_Website_To_SQL();
        self.myPopup.Progress_Bar.value = 75;
        Vu_Com.Blocking_Websites();
        self.myPopup.Progress_Bar.value = 100;

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    pass


class SnippetView(BoxLayout, RecycleDataViewBehavior, Label):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)


    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes'''
        self.index = index
        return super(SnippetView, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        if super(SnippetView, self).on_touch_down(touch):
            return True
        elif self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        global selected_index
        self.selected = is_selected
        if is_selected:
            selected_index = index;
            pass
        else:
            selected_index = None
            pass


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.bind(pos=self.update)
        self.bind(size=self.update)
        window_sizes = Window.size
        self.width, self.length = window_sizes
        self.update()
        self.inputData();

    def update(self, *args):
        self.width, self.length = self.size
        with self.canvas:
            pass

    def inputData(self):
        self.dataSQL = UserDB();
        self.dataSQL.readURL();
        self.data = [{"text_size": (self.width - 10, None), "color": (0, 0, 0, 1), "font_size": "20sp", "text": str(x)}
                     for x in self.dataSQL.data]



class CustomizationScreen(Screen, Label):
    website = ObjectProperty(None);
    website_list = ObjectProperty();
    database = UserDB();
    Vu_Com = WebsiteBlocker.WebsiteBlocker();


    def AddingWebsite(self):
        self.myPopup = MyPopup();
        Checking_existence = self.Vu_Com.Check_Website(self.website.text);
        self.database.readURL();
        if Checking_existence == True:
            checking_in_data = self.Vu_Com.Checking_Website_list(self.website_list);
            if checking_in_data == True:
                pass
            else:
                self.database.readURL();
                self.Vu_Com.Blocking_Single_Website(self.website.text);
                self.website_list.inputData();
                self.website_list.refresh_from_viewport();
                self.website_list.refresh_from_data();
                self.website.text = ''
        else:
            text = self.website.text + " is not a website \n or it is missing the heading for example(www.) \n or it has been subscribed";
            self.myPopup.Warning_popup(text)
            self.myPopup.Cancel_Button.bind(on_press= self.popup_dismiss)


    def DeletingWebsite(self):
        # Working with Global variable Selected_Index
        if selected_index is None:
            self.myPopup = MyPopup();
            text = "No item has been selected";
            self.myPopup.Warning_popup(text)
            self.myPopup.Cancel_Button.bind(on_press=self.popup_dismiss)
        else:
            self.database.readURL();
            self.Vu_Com.Unblocking_Single_Website(website_index=selected_index)
            self.website_list.inputData();
            self.website_list.refresh_from_viewport();
            self.website_list.refresh_from_data();

    def Searching(self):
        # Getting the text from the textinput
        self.text = self.website.text
        # Looking through entire list
        self.myPopup = MyPopup();
        Checking = self.Vu_Com.Checking_Website_list(url = self.website.text)

        if Checking == True:
            self.myPopup.matched_popup(self.website.text);
            self.myPopup.Remove_Button.bind(on_press=self.popup_removing);
            self.myPopup.Cancel_Button.bind(on_press=self.popup_dismiss);

        else:
            self.myPopup.unmatched_popup(self.website.text);
            self.myPopup.Adding_Button.bind(on_press=self.popup_adding);
            self.myPopup.Cancel_Button.bind(on_press=self.popup_dismiss);

    def popup_dismiss(self, instance):
        self.myPopup.Matched_Popup.dismiss()

    def popup_adding(self, instance):
        self.Vu_Com.Blocking_Single_Website(self.website.text);
        self.myPopup.Matched_Popup.dismiss();
        self.website_list.inputData();
        self.website_list.refresh_from_viewport();
        self.website_list.refresh_from_data();
        self.website.text = ''

    def popup_removing(self, instance):
        self.Vu_Com.Unblocking_Single_Website(website_name= self.website.text);
        self.myPopup.Matched_Popup.dismiss()
        self.website_list.inputData();
        self.website_list.refresh_from_viewport();
        self.website_list.refresh_from_data();
        self.website.text = ''

    def update(self):
        self.myPopup = MyPopup();
        self.myPopup.Completion_popup()
        self.website_list.inputData();
        self.myPopup.Progress_Bar.value = 25;
        self.website_list.refresh_from_viewport();
        self.myPopup.Progress_Bar.value = 50;
        self.website_list.refresh_from_data();
        self.myPopup.Progress_Bar.value = 75;
        self.myPopup.Progress_Bar.value = 100;



class MyPopup(Popup):
    def matched_popup(self, website_name):
        layout = BoxLayout(orientation='vertical');
        anchorlayout = AnchorLayout(anchor_x='right', anchor_y='bottom', size_hint=(1, 0.3))
        boxlayout = BoxLayout(orientation='horizontal', size_hint=(0.5, 1));

        self.Remove_Button = Button(text="Remove", size_hint=(0.25, 0.5));
        self.Cancel_Button = Button(text="Cancel", size_hint=(0.25, 0.5));

        boxlayout.add_widget(self.Remove_Button);
        boxlayout.add_widget(self.Cancel_Button);

        anchorlayout.add_widget(boxlayout)

        Text = Label(text=website_name + " has been found", size_hint=(1, 0.2), font_size="24sp");
        layout.add_widget(Text)
        layout.add_widget(anchorlayout)
        self.Matched_Popup = Popup(title="Website URL", size_hint=(0.8, 0.5), content=layout, auto_dismiss=True)
        self.Matched_Popup.open()

    def unmatched_popup(self, website_name):
        layout = BoxLayout(orientation='vertical');
        anchorlayout = AnchorLayout(anchor_x='right', anchor_y='bottom', size_hint=(1, 0.3))
        boxlayout = BoxLayout(orientation='horizontal', size_hint=(0.5, 1));

        self.Adding_Button = Button(text="Add", size_hint=(0.25, 0.5));
        self.Cancel_Button = Button(text="Cancel", size_hint=(0.25, 0.5));

        boxlayout.add_widget(self.Adding_Button);
        boxlayout.add_widget(self.Cancel_Button);

        anchorlayout.add_widget(boxlayout)

        Text = Label(text=website_name + " has not been found \n" + "Do you want to add it ? ", size_hint=(1, 0.2),
                     font_size="24sp");
        layout.add_widget(Text)
        layout.add_widget(anchorlayout)
        self.Matched_Popup = Popup(title="Website URL", size_hint=(0.8, 0.5), content=layout, auto_dismiss=True)
        self.Matched_Popup.open()

    def Warning_popup(self, message):
        layout = BoxLayout(orientation='vertical');
        anchorlayout = AnchorLayout(anchor_x='right', anchor_y='bottom', size_hint=(1, 0.3))
        boxlayout = BoxLayout(orientation='horizontal', size_hint=(0.5, 1));

        self.Cancel_Button = Button(text="Cancel", size_hint=(0.25, 0.5));

        boxlayout.add_widget(self.Cancel_Button);

        anchorlayout.add_widget(boxlayout)

        Text = Label(text= message, size_hint=(1, 0.2),
                     font_size="24sp");
        layout.add_widget(Text)
        layout.add_widget(anchorlayout)
        self.Matched_Popup = Popup(title="Website URL", size_hint=(0.8, 0.5), content=layout, auto_dismiss=True)
        self.Matched_Popup.open()

    def Completion_popup(self):
        layout = BoxLayout(orientation='vertical');
        self.Progress_Bar = ProgressBar(max=100)

        layout.add_widget(self.Progress_Bar)

        self.Matched_Popup = Popup(title="Website URL", size_hint=(0.8, 0.5), content=layout, auto_dismiss=True)
        self.Matched_Popup.open()


sm = ScreenManager(transition=NoTransition())
sm.add_widget(MainScreen(name='main'))
sm.add_widget(CustomizationScreen(name='custom'))


class MainApp(App):
    def __init__(self, **kwargs):
        self.title = "Website Blocker"
        super().__init__(**kwargs);

    def build(self):
        return sm

    def on_start(self):
        pass


if __name__ == "__main__":
    if WebsiteBlocker.is_admin():
        MainApp().run()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1);
