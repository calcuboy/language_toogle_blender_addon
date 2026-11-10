bl_info = {
    "name": "Quick Language Toggle",
    "author": "WorkBuddy",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "Edit > Toggle Interface Language / Preferences > Add-ons > Quick Language Toggle",
    "description": "Flip the interface language (or its translation) with a configurable "
                   "shortcut, without restarting Blender",
    "category": "System",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
}

import bpy

# Reload support for quick iterative development inside Blender.
if "utils" in locals():
    import importlib
    importlib.reload(utils)
    importlib.reload(props)
    importlib.reload(keymap)
    importlib.reload(operators)
    importlib.reload(i18n)
else:
    from . import utils, props, keymap, operators, i18n

_CLASSES = (
    props.LANGTOGGLE_preferences,
    operators.LANGTOGGLE_OT_toggle,
    operators.LANGTOGGLE_OT_capture_key,
)


def _draw_edit_menu(self, context):
    self.layout.operator(
        "langtoggle.toggle",
        text="Toggle Interface Language",
        icon='WORLD_DATA',
    )


def register():
    for cls in _CLASSES:
        bpy.utils.register_class(cls)

    i18n.register()
    keymap.register_keymap()
    # The add-on keyconfig may not be ready during startup - rebuild once shortly after.
    keymap.register_delayed()

    try:
        bpy.types.TOPBAR_MT_edit.append(_draw_edit_menu)
    except Exception as exc:
        print("[Language Toggle] Could not add Edit menu entry: %s" % exc)


def unregister():
    try:
        bpy.types.TOPBAR_MT_edit.remove(_draw_edit_menu)
    except Exception:
        pass

    keymap.unregister_keymap()
    i18n.unregister()

    for cls in reversed(_CLASSES):
        try:
            bpy.utils.unregister_class(cls)
        except Exception:
            pass
