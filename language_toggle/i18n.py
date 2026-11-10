"""Bilingual UI strings - the add-on follows whatever the interface language is."""

import bpy

# Blender expects translations grouped by locale: {"<locale>": {(context, msgid): msgstr}}
_ZH_HANS = {
    # --- add-on name --------------------------------------------------------
    ("*", "Quick Language Toggle"): "快捷语言切换",

    # --- preferences: behaviour --------------------------------------------
    ("*", "Switching Mode"): "切换方式",
    ("*", "What the shortcut actually flips"): "快捷键真正切换的内容",
    ("*", "Interface Translation"): "界面翻译开关",
    ("*", "Flip 'Translate Interface' - keeps your language setting and toggles between English and that language"):
        "切换“翻译界面”，保留语言设置，在英文与该语言之间来回切换",
    ("*", "Switch Language"): "切换语言",
    ("*", "Flip the language itself between Language A and Language B"):
        "在语言 A 与语言 B 之间切换语言本身",
    ("*", "Language A"): "语言 A",
    ("*", "First language of the A/B toggle"): "A/B 切换中的第一种语言",
    ("*", "Language B"): "语言 B",
    ("*", "Second language of the A/B toggle"): "A/B 切换中的第二种语言",
    ("*", "Also Switch Tooltips"): "同时切换工具提示",
    ("*", "Keep tooltip translation in sync with the interface"): "工具提示的翻译与界面保持一致",
    ("*", "Also Switch New Data Names"): "同时切换新建数据名",
    ("*", "Keep automatic name translation (objects, materials...) in sync"):
        "自动翻译新建数据名（物体、材质等）与界面保持一致",
    ("*", "Save Preferences After Switching"): "切换后保存偏好设置",
    ("*", "Write the new state to the user preferences file so it survives a restart"):
        "把切换结果写入用户偏好设置文件，重启后保持",
    ("*", "Keeps the language setting untouched and"): "不改动界面语言设置，",
    ("*", "only flips 'Translate Interface'."): "只切换“翻译界面”开关。",
    ("*", "Alternates between language A and B."): "在语言 A 与 B 之间往返切换。",

    # --- preferences: shortcut ---------------------------------------------
    ("*", "Shortcut"): "快捷键",
    ("*", "Enable Global Shortcut"): "启用全局快捷键",
    ("*", "Register the shortcut in Blender's Window keymap (works in any editor)"):
        "注册到 Blender 的 Window 键位映射，任何编辑器窗口中都有效",
    ("*", "Key"): "按键",
    ("*", "Blender key identifier, captured with the button below"):
        "Blender 按键标识符，用下面的按钮直接捕获",
    ("*", "Listening... press keys (Esc to cancel)"): "监听中…请按下组合键（Esc 取消）",
    ("*", "(click to change)"): "（点击修改）",
    ("*", "Hold the modifiers, then press the main key."):
        "按住修饰键，再按主键；",
    ("*", "The whole combination is recorded at once."):
        "整组组合键会被一次记录。",
    ("*", "Also available in the Edit menu."): "也可以在「编辑」菜单里找到它。",

    # --- operators ----------------------------------------------------------
    ("*", "Toggle Interface Language"): "切换界面语言",
    ("*", "Switch the interface language on the fly"): "即时切换界面语言",
    ("*", "Capture Shortcut"): "捕获快捷键",
    ("*", "Press the key combination you want to use for switching languages"):
        "按下你想用来切换语言的组合键",
    ("*", "Shortcut capture cancelled"): "已取消快捷键录制",
    ("*", "Shortcut set to %s"): "快捷键已设为 %s",
    ("*", "Interface translation enabled"): "界面翻译已开启",
    ("*", "Interface translation disabled"): "界面翻译已关闭",
    ("*", "Language: %s"): "语言：%s",
    ("*", "Not available in this Blender version: %s"): "当前 Blender 版本不支持该语言：%s",
}


MESSAGES = {
    "zh_HANS": _ZH_HANS,
}


def register():
    try:
        bpy.app.translations.register(__package__, MESSAGES)
    except Exception as exc:
        print("[Language Toggle] Translation registration failed: %s" % exc)


def unregister():
    try:
        bpy.app.translations.unregister(__package__)
    except Exception:
        pass
