"""Operators: the actual toggle and the shortcut capture modal."""

import bpy

from . import keymap
from .props import available_languages, get_prefs
from .utils import (
    IGNORED_EVENTS,
    MODIFIER_EVENTS,
    refresh_prefs_areas,
    refresh_ui,
    shortcut_label,
)

try:
    from bpy.app.translations import pgettext_iface as _translate
except ImportError:  # very old builds
    def _translate(msgid):
        return msgid


class LANGTOGGLE_OT_toggle(bpy.types.Operator):
    bl_idname = "langtoggle.toggle"
    bl_label = "Toggle Interface Language"
    bl_description = "Switch the interface language on the fly"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return get_prefs(context) is not None

    def execute(self, context):
        prefs = get_prefs(context)
        if prefs is None:
            return {'CANCELLED'}

        view = context.preferences.view

        if prefs.mode == 'INTERFACE':
            state = not view.use_translate_interface
            view.use_translate_interface = state
            if prefs.sync_tooltips:
                view.use_translate_tooltips = state
            if prefs.sync_new_dataname:
                view.use_translate_new_dataname = state
            self.report(
                {'INFO'},
                _translate("Interface translation enabled") if state
                else _translate("Interface translation disabled"),
            )
        else:
            current = view.language
            target = prefs.language_a if current == prefs.language_b else prefs.language_b
            valid = available_languages()
            if valid is not None and target not in valid:
                self.report(
                    {'WARNING'},
                    _translate("Not available in this Blender version: %s") % target,
                )
                return {'CANCELLED'}
            view.language = target
            self.report({'INFO'}, _translate("Language: %s") % target)

        if prefs.save_userpref:
            try:
                bpy.ops.wm.save_userpref()
            except Exception as exc:
                print("[Language Toggle] Could not save preferences: %s" % exc)

        refresh_ui()
        return {'FINISHED'}


class LANGTOGGLE_OT_capture_key(bpy.types.Operator):
    bl_idname = "langtoggle.capture_key"
    bl_label = "Capture Shortcut"
    bl_description = "Press the key combination you want to use for switching languages"
    bl_options = {'INTERNAL'}

    _timer = None

    @classmethod
    def poll(cls, context):
        return get_prefs(context) is not None

    def invoke(self, context, event):
        prefs = get_prefs(context)
        if prefs is None:
            return {'CANCELLED'}

        prefs.is_capturing = True
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.15, window=context.window)
        wm.modal_handler_add(self)
        refresh_prefs_areas()
        return {'RUNNING_MODAL'}

    def _stop(self, context):
        prefs = get_prefs(context)
        if prefs is not None:
            prefs.is_capturing = False
        if self._timer is not None:
            try:
                context.window_manager.event_timer_remove(self._timer)
            except Exception:
                pass
            self._timer = None
        refresh_prefs_areas()

    def modal(self, context, event):
        prefs = get_prefs(context)
        if prefs is None:
            self._stop(context)
            return {'CANCELLED'}

        # Esc cancels; losing the window (alt-tab, closed preferences) must not
        # leave a modal handler dangling.
        if event.type in {'ESC', 'WINDOW_DEACTIVATE'}:
            self._stop(context)
            self.report({'INFO'}, _translate("Shortcut capture cancelled"))
            return {'CANCELLED'}

        if event.type == 'TIMER':
            refresh_prefs_areas()
            return {'RUNNING_MODAL'}

        if event.value != 'PRESS' or event.type in IGNORED_EVENTS:
            return {'RUNNING_MODAL'}

        # Still holding only the modifiers - keep listening for the real key.
        if event.type in MODIFIER_EVENTS:
            return {'RUNNING_MODAL'}

        prefs.use_shortcut = True
        prefs.ctrl = bool(event.ctrl)
        prefs.shift = bool(event.shift)
        prefs.alt = bool(event.alt)
        prefs.oskey = bool(event.oskey)
        prefs.key = event.type

        keymap.register_keymap()

        self._stop(context)
        self.report({'INFO'}, _translate("Shortcut set to %s") % shortcut_label(prefs))
        return {'FINISHED'}
