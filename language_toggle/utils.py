"""Small shared helpers: UI refresh and shortcut label formatting."""

import bpy

# Event types that are modifier keys themselves - we keep waiting while they are held.
MODIFIER_EVENTS = {
    'LEFT_CTRL', 'RIGHT_CTRL',
    'LEFT_SHIFT', 'RIGHT_SHIFT',
    'LEFT_ALT', 'RIGHT_ALT',
    'LEFT_OSKEY', 'RIGHT_OSKEY',
}

# Event types that can never be used as a shortcut key.
IGNORED_EVENTS = {
    'NONE', 'TIMER', 'TIMER_REPORT',
    'MOUSEMOVE', 'INBETWEEN_MOUSEMOVE', 'MOUSEROTATE',
    'LEFTMOUSE', 'RIGHTMOUSE', 'MIDDLEMOUSE', 'BUTTON4MOUSE', 'BUTTON5MOUSE',
    'WHEELUPMOUSE', 'WHEELDOWNMOUSE', 'WHEELINMOUSE', 'WHEELOUTMOUSE',
    'TRACKPADPAN', 'TRACKPADZOOM',
    'NDOF_MOTION', 'NDOF_BUTTON_MENU',
    'WINDOW_DEACTIVATE', 'WINDOW_ACTIVATE',
}

_KEY_NAMES = {
    'SPACE': 'Space',
    'TAB': 'Tab',
    'RET': 'Enter',
    'ESC': 'Esc',
    'BACK_SPACE': 'Backspace',
    'DEL': 'Delete',
    'HOME': 'Home',
    'END': 'End',
    'PAGE_UP': 'PageUp',
    'PAGE_DOWN': 'PageDown',
    'UP_ARROW': 'Up',
    'DOWN_ARROW': 'Down',
    'LEFT_ARROW': 'Left',
    'RIGHT_ARROW': 'Right',
    'COMMA': 'Comma',
    'PERIOD': 'Period',
    'SLASH': 'Slash',
    'BACK_SLASH': 'Backslash',
    'SEMI_COLON': 'Semicolon',
    'QUOTE': 'Quote',
    'MINUS': 'Minus',
    'EQUAL': 'Equal',
    'LEFT_BRACKET': 'LeftBracket',
    'RIGHT_BRACKET': 'RightBracket',
    'ACCENT_GRAVE': 'Grave',
}


def pretty_key(key):
    """Turn a Blender key identifier into something readable."""
    if not key or key == 'NONE':
        return "\u2014"
    if len(key) == 1:
        return key.upper()
    if key in _KEY_NAMES:
        return _KEY_NAMES[key]
    if key.startswith('NUMPAD_'):
        return "Numpad " + key[7:].replace('_', ' ').title()
    return key.replace('_', ' ').title()


def shortcut_label(prefs):
    """Readable shortcut string, e.g. 'Ctrl + Alt + L'."""
    parts = []
    if prefs.ctrl:
        parts.append("Ctrl")
    if prefs.shift:
        parts.append("Shift")
    if prefs.alt:
        parts.append("Alt")
    if prefs.oskey:
        parts.append("Cmd/Win")
    parts.append(pretty_key(prefs.key))
    return " + ".join(parts)


def refresh_ui():
    """Redraw every editor so a language change becomes visible immediately."""
    wm = getattr(bpy.context, "window_manager", None)
    if wm is None:
        return
    for window in wm.windows:
        screen = getattr(window, "screen", None)
        if screen is None:
            continue
        for area in screen.areas:
            try:
                area.tag_redraw()
            except Exception:
                pass
    # A swapped redraw forces strings that are cached in the header/menus to update.
    try:
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
    except Exception:
        pass


def refresh_prefs_areas():
    """Redraw only the preferences editors (used while capturing a shortcut)."""
    wm = getattr(bpy.context, "window_manager", None)
    if wm is None:
        return
    for window in wm.windows:
        screen = getattr(window, "screen", None)
        if screen is None:
            continue
        for area in screen.areas:
            if area.type == 'PREFERENCES':
                try:
                    area.tag_redraw()
                except Exception:
                    pass
