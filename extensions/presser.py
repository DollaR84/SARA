"""
Emulation pressing hotkeys.

Created on 13.11.2016

@author: Ruslan Dolovanyuk

"""

import logging

import win32api

import win32con


def check(ptr, config, text):
    """Check need actions for use."""
    if 'open_computer' == text:
        open_computer()
    elif 'open_run' == text:
        open_run()
    elif 'open_charms' == text:
        open_charms()
    elif 'open_settings' == text:
        open_settings()
    elif 'open_share' == text:
        open_share()
    elif 'open_devices' == text:
        open_devices()
    elif 'find_application' == text:
        find_application()
    elif 'find_file' == text:
        find_file()
    elif 'find_setting' == text:
        find_setting()
    elif 'settings_2monitor' == text:
        settings_2monitor()
    elif 'open_menu' == text:
        open_menu()
    elif 'menu_system_tools' == text:
        menu_system_tools()
    elif 'open_specifical_abbilities' == text:
        open_specifical_abbilities()
    elif 'turn_all' == text:
        turn_all()
    elif 'lock_computer' == text:
        lock_computer()


def __down(vkey):
    win32api.keybd_event(vkey, 0, 0, 0)


def __up(vkey):
    win32api.keybd_event(vkey, 0, win32con.KEYEVENTF_KEYUP, 0)


def __press_hotkey(vkey, *vmods):
    for vmod in vmods:
        __down(vmod)

    __down(vkey)
    __up(vkey)

    for vmod in vmods:
        __up(vmod)


def open_computer():
    """Open computer window."""
    log = logging.getLogger()
    log.info('press hotkey: open computer')
    __press_hotkey(0x45, win32con.VK_LWIN)


def open_run():
    """Open run bar."""
    log = logging.getLogger()
    log.info('press hotkey: open run bar')
    __press_hotkey(0x52, win32con.VK_LWIN)


def open_charms():
    """Open charms bar."""
    log = logging.getLogger()
    log.info('press hotkey: open charms bar')
    __press_hotkey(0x43, win32con.VK_LWIN)


def open_settings():
    """Open settings bar."""
    log = logging.getLogger()
    log.info('press hotkey: open settings bar')
    __press_hotkey(0x49, win32con.VK_LWIN)


def open_share():
    """Open share bar."""
    log = logging.getLogger()
    log.info('press hotkey: open share bar')
    __press_hotkey(0x48, win32con.VK_LWIN)


def open_devices():
    """Open devices bar."""
    log = logging.getLogger()
    log.info('press hotkey: open devices bar')
    __press_hotkey(0x4B, win32con.VK_LWIN)


def find_application():
    """Open find application bar."""
    log = logging.getLogger()
    log.info('press hotkey: find application bar')
    __press_hotkey(0x51, win32con.VK_LWIN)


def find_file():
    """Open find file bar."""
    log = logging.getLogger()
    log.info('press hotkey: find file bar')
    __press_hotkey(0x46, win32con.VK_LWIN)


def find_setting():
    """Open find setting bar."""
    log = logging.getLogger()
    log.info('press hotkey: find setting bar')
    __press_hotkey(0x57, win32con.VK_LWIN)


def settings_2monitor():
    """Open settings 2 monitor."""
    log = logging.getLogger()
    log.info('press hotkey: settings 2 monitor')
    __press_hotkey(0x50, win32con.VK_LWIN)


def open_menu():
    """Open menu bar."""
    log = logging.getLogger()
    log.info('press hotkey: open menu bar')
    __press_hotkey(0x5A, win32con.VK_LWIN)


def menu_system_tools():
    """Open menu system tools."""
    log = logging.getLogger()
    log.info('press hotkey: menu system tools')
    __press_hotkey(0x58, win32con.VK_LWIN)


def open_specifical_abbilities():
    """Open specifical abbilities."""
    log = logging.getLogger()
    log.info('press hotkey: open specifical abbilities')
    __press_hotkey(0x55, win32con.VK_LWIN)


def turn_all():
    """Turn all."""
    log = logging.getLogger()
    log.info('press hotkey: turn all')
    __press_hotkey(0x4D, win32con.VK_LWIN)


def lock_computer():
    """Lock computer."""
    log = logging.getLogger()
    log.info('press hotkey: lock computer')
    __press_hotkey(0x4C, win32con.VK_LWIN)
