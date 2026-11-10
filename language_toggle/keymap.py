"""Registers the shortcut in the add-on keymap so it works everywhere in Blender."""

import bpy

from .props import get_prefs

# (keymap, keymap_item) currently owned by this add-on.
_HANDLE = None
_REBUILD_PENDING = False

_TOGGLE_OP = "langtoggle.toggle"


def _get_window_keymap():
    """The 'Window' keymap of the add-on keyconfig - active in every editor."""
    wm = getattr(bpy.context, "window_manager", None)
    if wm is None:
        return None
    kc = getattr(wm.keyconfigs, "addon", None)
    if kc is None:
        return None

    km = kc.keymaps.get("Window")
    if km is not None:
        return km
    try:
        return kc.keymaps.new(name="Window", space_type='EMPTY')
    except Exception as exc:
        print("[Language Toggle] Cannot create Window keymap: %s" % exc)
        return None


def unregister_keymap():
    global _HANDLE
    if _HANDLE is None:
        return
    km, kmi = _HANDLE
    _HANDLE = None
    try:
        km.keymap_items.remove(kmi)
    except Exception:
        pass


def register_keymap():
    """(Re)build the shortcut. Returns False when the keymap is not available yet."""
    global _HANDLE
    unregister_keymap()

    prefs = get_prefs()
    if prefs is None or not prefs.use_shortcut:
        return True

    key = prefs.key or 'NONE'
    if key in {'NONE', ''}:
        return True

    km = _get_window_keymap()
    if km is None:
        return False

    try:
        kmi = km.keymap_items.new(
            _TOGGLE_OP,
            key,
            'PRESS',
            any=False,
            ctrl=prefs.ctrl,
            shift=prefs.shift,
            alt=prefs.alt,
            oskey=prefs.oskey,
        )
    except Exception as exc:
        print("[Language Toggle] Cannot register shortcut '%s': %s" % (key, exc))
        return True

    _HANDLE = (km, kmi)
    return True


def register_delayed(delay=1.0):
    """Retry once after startup - the add-on keyconfig may not exist that early."""
    def _retry():
        if not register_keymap():
            print("[Language Toggle] Keymap still unavailable, shortcut not bound.")
        return None

    try:
        bpy.app.timers.register(_retry, first_interval=delay)
    except Exception:
        pass


def schedule_refresh():
    """Rebuild the shortcut once, shortly after the last preference change."""
    global _REBUILD_PENDING
    if _REBUILD_PENDING:
        return
    _REBUILD_PENDING = True

    def _run():
        global _REBUILD_PENDING
        _REBUILD_PENDING = False
        register_keymap()
        return None

    try:
        bpy.app.timers.register(_run, first_interval=0.05)
    except Exception:
        _REBUILD_PENDING = False
        register_keymap()
