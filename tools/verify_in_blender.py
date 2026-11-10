"""Blender 内验收脚本 —— 改完插件后重跑一遍确认没有回归。

用法（在项目根目录）：
    "D:/blender-5.2.1-windows-x64/blender.exe" -b --factory-startup ^
        --python tools/verify_in_blender.py

脚本会自动安装 dist/language_toggle-1.0.0-ext.zip 到临时目录并启用，
不会污染你真实的 Blender 配置。
"""

import os
import sys
import tempfile

import bpy

MODULE = "bl_ext.user_default.language_toggle"
HERE = os.path.dirname(os.path.abspath(__file__))
ZIP = os.path.join(os.path.dirname(HERE), "dist", "language_toggle-1.0.0-ext.zip")

failures = []


def check(label, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    print("[%s] %s %s" % (status, label, detail))
    if not condition:
        failures.append(label)


def main():
    print("ZIP:", ZIP)
    if not os.path.exists(ZIP):
        print("缺少安装包，先打包 dist/language_toggle-1.0.0-ext.zip")
        return

    bpy.ops.extensions.package_install_files(
        filepath=ZIP, repo='user_default', enable_on_install=True
    )
    check("扩展安装并启用", MODULE in bpy.context.preferences.addons)

    prefs = bpy.context.preferences.addons[MODULE].preferences
    view = bpy.context.preferences.view

    # --- 模式一：界面翻译开关 ---
    prefs.mode = 'INTERFACE'
    start = view.use_translate_interface

    bpy.ops.langtoggle.toggle()
    check("翻转 #1", view.use_translate_interface is (not start),
          "iface=%s" % view.use_translate_interface)
    check("工具提示联动", view.use_translate_tooltips == view.use_translate_interface)
    check("新建数据名联动", view.use_translate_new_dataname == view.use_translate_interface)

    bpy.ops.langtoggle.toggle()
    check("翻转 #2 复原", view.use_translate_interface is start)

    # --- 模式二：切换语言 ---
    prefs.mode = 'LANGUAGE'
    prefs.language_a = 'en_US'
    prefs.language_b = 'zh_HANS'
    view.language = 'en_US'

    bpy.ops.langtoggle.toggle()
    check("语言 A -> B", view.language == 'zh_HANS', view.language)
    bpy.ops.langtoggle.toggle()
    check("语言 B -> A", view.language == 'en_US', view.language)

    # --- 键位 ---
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.get("Window")
    items = [k for k in km.keymap_items if k.idname == "langtoggle.toggle"] if km else []
    check("addon 键位层已注册", len(items) == 1, "%d 条" % len(items))
    if items:
        k = items[0]
        check("键位为 L+Ctrl+Alt",
              k.type == 'L' and k.ctrl and k.alt and not k.shift and not k.oskey,
              "%s ctrl=%s alt=%s" % (k.type, k.ctrl, k.alt))

    # --- 翻译 ---
    view.language = 'zh_HANS'
    zh = bpy.app.translations.pgettext_iface("Switching Mode")
    check("中文翻译生效", zh == "切换方式", repr(zh))
    view.language = 'en_US'
    en = bpy.app.translations.pgettext_iface("Switching Mode")
    check("英文界面不误译", en == "Switching Mode", repr(en))

    # --- 清理 ---
    bpy.ops.preferences.addon_disable(module=MODULE)
    km2 = wm.keyconfigs.addon.keymaps.get("Window")
    left = [k for k in km2.keymap_items if k.idname == "langtoggle.toggle"] if km2 else []
    check("禁用后键位清除", len(left) == 0)

    print("-" * 60)
    if failures:
        print("FAILED:", ", ".join(failures))
    else:
        print("ALL CHECKS PASSED")


main()
