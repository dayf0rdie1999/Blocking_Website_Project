from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior

Builder.load_string('''
<RV>:
    viewclass: 'SnippetView'
    SelectableRecycleBoxLayout:
        default_size: None, dp(42)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: True
        touch_multiselect: True
        

<SnippetView>:
    canvas.before:
        Color:
            rgba: (0,0.9,.1,.3) if self.selected else(255,255,255)
        Rectangle:
            pos: self.pos
            size: self.size
    orientation: 'vertical'
    
    Label:
        text: root.heading
        text_size: root.width, None
        size: self.texture_size
        color: 0,0,0,1
''')


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    pass


class SnippetView(BoxLayout,RecycleDataViewBehavior, Label):
    heading = StringProperty()
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
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
        else:
            print("selection removed for {0}".format(rv.data[index]))


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'heading': str(x)} for x in range(10)]


rv = RV()
runTouchApp(rv)
