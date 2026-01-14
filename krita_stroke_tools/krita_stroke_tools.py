from krita import *
from PyQt5.QtCore import QObject
from .stroke_event_filter import StrokeEventFilter


class KritaStrokeTools(Extension):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Allow the user to turn the plugin off.
        # If enabled is false, on_stroke() will do nothing.
        self.enabled = False

        # Create a StrokeEventFilter which will call our on_stroke() method
        # every time the user finishes a stroke
        self.event_filter = StrokeEventFilter(self)

    def setup(self):
        QApplication.instance().installEventFilter(self.event_filter)
    
    def createActions(self, window):
        # Creates an action that toggles this plugin on and off.
        action = window.createAction(
            "krita_stroke_tools_toggle",
            "Toggle Krita Stroke Tools",
            "tools/scripts"   # appears in Tools → Scripts menu
        )
        action.setCheckable(True)
        action.triggered.connect(self.toggle_enabled)

    # Toggle the plugin, ie. create or clean up the stroke layer.
    def toggle_enabled(self, checked):
        self.enabled = checked
        if checked: 
            self.create_stroke_layer()
        else:
            self.clean_up_stroke_layer()

    def create_stroke_layer(self):
        doc = Krita.instance().activeDocument()
        if not doc:
            return
        root = doc.rootNode()

        # Remember the previously selected layer.
        self.base_layer = doc.activeNode()

        # Create a new layer, the stroke layer.
        self.stroke_layer = doc.createNode("Stroke Layer", "paintLayer")
        root.addChildNode(self.stroke_layer, None)

    def clean_up_stroke_layer(self):
        parent = self.stroke_layer.parentNode()
        parent.removeChildNode(self.stroke_layer)

    def on_stroke(self):
        if not self.enabled:
            return
        print("on_stroke called")