#!/usr/bin/env python3
import sys
import os
import re

# 1. Fork FIRST! We must detach into the background before GLib 
# starts any worker threads to avoid deadlocks.
if os.fork() != 0:
    sys.exit(0)

# Now it is safe to import GTK
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

# 2. Read HTML from stdin
html_data = sys.stdin.read()
if not html_data:
    sys.exit(0)

# Ensure UTF-8 meta tag is present for Electron/Chromium apps
if '<meta charset="utf-8">' not in html_data.lower() and '<meta http-equiv=' not in html_data.lower():
    html_data = '<meta charset="utf-8">\n' + html_data

# Create a basic plain text fallback (Slack needs this to validate the paste)
plain_data = re.sub(r'<[^>]+>', '', html_data)
plain_data = re.sub(r'\n\s*\n', '\n\n', plain_data).strip()

# 3. Create an invisible widget to act as the clipboard owner
window = Gtk.Invisible()
window.realize() # Must be realized to interact with the display server

# Callback when an app (like Slack) pastes and requests the data
def on_selection_get(widget, selection_data, info, time):
    if info == 0:
        selection_data.set(Gdk.Atom.intern("text/html", False), 8, html_data.encode('utf-8'))
    else:
        selection_data.set_text(plain_data, -1)

# Callback when you copy something new (releases the background process)
def on_selection_clear(widget, event):
    Gtk.main_quit()

window.connect("selection-get", on_selection_get)
window.connect("selection-clear-event", on_selection_clear)

# 4. Define our multi-target formats
# The 'info' integer maps to the info parameter in on_selection_get
targets = [
    Gtk.TargetEntry.new("text/html", 0, 0),
    Gtk.TargetEntry.new("UTF8_STRING", 0, 1),
    Gtk.TargetEntry.new("STRING", 0, 1),
    Gtk.TargetEntry.new("text/plain", 0, 1)
]

# 5. Take ownership of the system clipboard
clipboard_atom = Gdk.Atom.intern("CLIPBOARD", False)

# Note: In PyGObject, selection API is mapped to the Gtk module level, not the widget instance
Gtk.selection_add_targets(window, clipboard_atom, targets)
Gtk.selection_owner_set(window, clipboard_atom, Gdk.CURRENT_TIME)

# 6. Start the event loop to serve the data
Gtk.main()
