from krita import *
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QTabletEvent

# Calls the plugin's on_stroke() everytime the user has finished painting a stroke.
# Note: Only strokes drawn with a drawing tablet are supported.
class StrokeEventFilter(QObject):
    def __init__(self, plugin):
        super().__init__()
        self.plugin = plugin    # the plugin that gets called
        self.stroke_in_progress = False

    def eventFilter(self, obj, event):
        # Only react to events on a canvas.
        if obj.metaObject().className() != "KisCanvasController":
            return False

        # Make sure an actual tablet pen event is happening.
        # Notice that this does not exclude the buttons on the pen.
        is_pen_event = isinstance(event, QTabletEvent) \
                and event.pointerType() == QTabletEvent.Pen
        if not is_pen_event:
            return False # allow Krita to handle the event normally

        # To distinguish tip press events from button press events,
        # we exploit that only tip events have pressure.
        is_tip_press_event = event.type() == QTabletEvent.TabletPress \
                and event.pressure() > 0.0
        
        # Unfortunately, this does not work for release events.
        # In practise, we just ignore this, 
        # since you don't generally release a button during a stroke.
        is_pen_release_event = event.type() == QTabletEvent.TabletRelease

        if is_tip_press_event and not self.stroke_in_progress:
            self.stroke_in_progress = True
        elif is_pen_release_event:
            self.stroke_in_progress = False
            # End of stroke, call plugin.
            self.plugin.on_stroke()

        return False  # allow Krita to handle the event normally