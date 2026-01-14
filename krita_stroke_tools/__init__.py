from krita import *
from .krita_stroke_tools import KritaStrokeTools
Krita.instance().addExtension(KritaStrokeTools(Krita.instance()))
