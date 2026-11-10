"""User facing configuration: stored in the add-on preferences."""

import bpy
from bpy.props import BoolProperty, EnumProperty, StringProperty

ADDON_ID = __package__

# Mirrors bpy.types.PreferencesView.language enum_items (Blender 2.80 - 5.2).
# A static list is required here: an EnumProperty whose 'items' is a callback may
# only use an integer default, and we need real identifiers as defaults.
# The names match Blender's own msgids, so they still get localised by Blender.
_LANGUAGES = [
    ('DEFAULT', 'Automatic', ""),
    ('ab', 'Abkhaz - Аԥсуа бызшәа', ""),
    ('ar_EG', 'Arabic - العربية', ""),
    ('eu_EU', 'Basque - Euskara', ""),
    ('be', 'Belarusian - Беларуская', ""),
    ('bg_BG', 'Bulgarian - Български', ""),
    ('ca_AD', 'Catalan - Català', ""),
    ('zh_HANS', 'Chinese (Simplified) - 简体中文', ""),
    ('zh_HANT', 'Chinese (Traditional) - 繁體中文', ""),
    ('hr', 'Croatian - Hrvatski', ""),
    ('cs_CZ', 'Czech - Čeština', ""),
    ('da', 'Danish - Dansk', ""),
    ('nl_NL', 'Dutch - Nederlands', ""),
    ('en_GB', 'English (UK)', ""),
    ('en_US', 'English (US)', ""),
    ('eo', 'Esperanto - Esperanto', ""),
    ('fi_FI', 'Finnish - Suomi', ""),
    ('fr_FR', 'French - Français', ""),
    ('ka', 'Georgian - ქართული', ""),
    ('de_DE', 'German - Deutsch', ""),
    ('el_GR', 'Greek - Ελληνικά', ""),
    ('he_IL', 'Hebrew - עברית', ""),
    ('hi_IN', 'Hindi - हिन्दी', ""),
    ('hu_HU', 'Hungarian - Magyar', ""),
    ('id_ID', 'Indonesian - Bahasa indonesia', ""),
    ('it_IT', 'Italian - Italiano', ""),
    ('ja_JP', 'Japanese - 日本語', ""),
    ('ko_KR', 'Korean - 한국어', ""),
    ('ky_KG', 'Kyrgyz - Кыргыз тили', ""),
    ('lt', 'Lithuanian - Lietuviškai', ""),
    ('ml', 'Malayalam - മലയാളം', ""),
    ('nb', 'Norwegian (Bokmål) - Norsk bokmål', ""),
    ('fa_IR', 'Persian - فارسی', ""),
    ('pl_PL', 'Polish - Polski', ""),
    ('pt_BR', 'Portuguese (Brazil) - Português brasileiro', ""),
    ('pt_PT', 'Portuguese (Portugal) - Português europeu', ""),
    ('ro_RO', 'Romanian - Român', ""),
    ('ru_RU', 'Russian - Русский', ""),
    ('sr_RS', 'Serbian (Cyrillic) - Српски', ""),
    ('sr_RS@latin', 'Serbian (Latin) - Srpski latinica', ""),
    ('sk_SK', 'Slovak - Slovenčina', ""),
    ('sl', 'Slovenian - Slovenščina', ""),
    ('es', 'Spanish - Español', ""),
    ('sw', 'Swahili - Kiswahili', ""),
    ('sv_SE', 'Swedish - Svenska', ""),
    ('ta', 'Tamil - தமிழ்', ""),
    ('th_TH', 'Thai - ภาษาไทย', ""),
    ('tr_TR', 'Turkish - Türkçe', ""),
    ('uk_UA', 'Ukrainian - Українська', ""),
    ('ur', 'Urdu - اردو', ""),
    ('vi_VN', 'Vietnamese - Tiếng Việt', ""),
]


def available_languages():
    """Identifiers this Blender build actually accepts, or None if unknown."""
    try:
        prop = bpy.types.PreferencesView.bl_rna.properties['language']
        return {e.identifier for e in prop.enum_items}
    except Exception:
        return None


def get_prefs(context=None):
    ctx = context or bpy.context
    prefs_root = getattr(ctx, "preferences", None)
    if prefs_root is None:
        return None
    addon = prefs_root.addons.get(ADDON_ID)
    if addon is None:
        return None
    return getattr(addon, "preferences", None)


def _on_shortcut_changed(self, context):
    from . import keymap
    keymap.schedule_refresh()


class LANGTOGGLE_preferences(bpy.types.AddonPreferences):
    bl_idname = ADDON_ID

    # ---------------------------------------------------------------- behaviour
    mode: EnumProperty(
        name="Switching Mode",
        description="What the shortcut actually flips",
        items=[
            ('INTERFACE', "Interface Translation",
             "Flip 'Translate Interface' - keeps your language setting and toggles "
             "between English and that language"),
            ('LANGUAGE', "Switch Language",
             "Flip the language itself between Language A and Language B"),
        ],
        default='INTERFACE',
    )

    language_a: EnumProperty(
        name="Language A",
        description="First language of the A/B toggle",
        items=_LANGUAGES,
        default='en_US',
    )

    language_b: EnumProperty(
        name="Language B",
        description="Second language of the A/B toggle",
        items=_LANGUAGES,
        default='zh_HANS',
    )

    sync_tooltips: BoolProperty(
        name="Also Switch Tooltips",
        description="Keep tooltip translation in sync with the interface",
        default=True,
    )

    sync_new_dataname: BoolProperty(
        name="Also Switch New Data Names",
        description="Keep automatic name translation (objects, materials...) in sync",
        default=True,
    )

    save_userpref: BoolProperty(
        name="Save Preferences After Switching",
        description="Write the new state to the user preferences file so it survives a restart",
        default=False,
    )

    # ----------------------------------------------------------------- shortcut
    use_shortcut: BoolProperty(
        name="Enable Global Shortcut",
        description="Register the shortcut in Blender's Window keymap (works in any editor)",
        default=True,
        update=_on_shortcut_changed,
    )

    ctrl: BoolProperty(name="Ctrl", default=True, update=_on_shortcut_changed)
    shift: BoolProperty(name="Shift", default=False, update=_on_shortcut_changed)
    alt: BoolProperty(name="Alt", default=True, update=_on_shortcut_changed)
    oskey: BoolProperty(name="Cmd/Win", default=False, update=_on_shortcut_changed)

    key: StringProperty(
        name="Key",
        description="Blender key identifier, captured with the button below",
        default='L',
        update=_on_shortcut_changed,
    )

    # runtime only
    is_capturing: BoolProperty(default=False, options={'SKIP_SAVE'})

    # --------------------------------------------------------------------- draw
    def draw(self, context):
        from .utils import shortcut_label

        layout = self.layout

        # --- what to switch ---------------------------------------------------
        box = layout.box()
        box.label(text="Switching Mode", icon='FILE_REFRESH')
        box.row().prop(self, "mode", expand=True)

        if self.mode == 'INTERFACE':
            help_box = box.column(align=True)
            help_box.label(text="Keeps the language setting untouched and", icon='INFO')
            help_box.label(text="only flips 'Translate Interface'.")
        else:
            row = box.row(align=True)
            row.prop(self, "language_a")
            row.prop(self, "language_b")
            box.label(text="Alternates between language A and B.", icon='INFO')

        row = box.row(align=True)
        row.prop(self, "sync_tooltips")
        row.prop(self, "sync_new_dataname")

        # --- shortcut ---------------------------------------------------------
        box = layout.box()
        box.label(text="Shortcut", icon='KEYINGSET')
        box.prop(self, "use_shortcut")

        if self.use_shortcut:
            row = box.row(align=True)
            row.scale_y = 1.6
            if self.is_capturing:
                row.operator(
                    "langtoggle.capture_key",
                    text="Listening... press keys (Esc to cancel)",
                    icon='REC',
                    depress=True,
                )
            else:
                row.operator(
                    "langtoggle.capture_key",
                    text=shortcut_label(self),
                    icon='REC',
                )
                row.label(text="(click to change)")
            col = box.column(align=True)
            col.label(text="Hold the modifiers, then press the main key.", icon='BLANK1')
            col.label(text="The whole combination is recorded at once.", icon='BLANK1')

        box = layout.box()
        box.prop(self, "save_userpref")

        layout.label(text="Also available in the Edit menu.", icon='MENU_PANEL')
