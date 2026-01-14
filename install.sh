#!/bin/sh
rm -rf $HOME/.local/share/krita/pykrita/krita_stroke_tools
cp -r krita_stroke_tools/ krita_stroke_tools.desktop $HOME/.local/share/krita/pykrita
cp krita_stroke_tools.action $HOME/.local/share/krita/actions