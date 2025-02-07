import os
import ctypes

def reset_wallpaper():
    default_wallpaper = os.path.join(os.getenv("SystemRoot"), "Web", "Wallpaper", "Windows", "img0.jpg")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, default_wallpaper, 3)

def reset_mouse_settings():
    ctypes.windll.user32.SystemParametersInfoW(113, 0, 15, 0)  # Сброс чувствительности мыши

def reset_mouse_cursor():
    default_cursor = "%SystemRoot%\\Cursors\\aero_arrow.cur"
    os.system("reg add HKEY_CURRENT_USER\\Control Panel\\Cursors /v Arrow /t REG_SZ /d " + default_cursor + " /f")
    os.system("reg add HKEY_CURRENT_USER\\Control Panel\\Cursors /v Hand /t REG_SZ /d " + default_cursor + " /f")
    os.system("reg add HKEY_CURRENT_USER\\Control Panel\\Cursors /v Help /t REG_SZ /d " + default_cursor + " /f")
    os.system("reg add HKEY_CURRENT_USER\\Control Panel\\Cursors /v AppStarting /t REG_SZ /d " + default_cursor + " /f")
    os.system("reg add HKEY_CURRENT_USER\\Control Panel\\Cursors /v Wait /t REG_SZ /d " + default_cursor + " /f")
    os.system("reg add HKEY_CURRENT_USER\\Control Panel\\Cursors /v Crosshair /t REG_SZ /d " + default_cursor + " /f")
    os.system("reg add HKEY_CURRENT_USER\\Control Panel\\Cursors /v IBeam /t REG_SZ /d " + default_cursor + " /f")
    os.system("reg add HKEY_CURRENT_USER\\Control Panel\\Cursors /v NO /t REG_SZ /d " + default_cursor + " /f")
    os.system("reg add HKEY_CURRENT_USER\\Control Panel\\Cursors /v SizeAll /t REG_SZ /d " + default_cursor + " /f")
    os.system("reg add HKEY_CURRENT_USER\\Control Panel\\Cursors /v SizeNESW /t REG_SZ /d " + default_cursor + " /f")
    os.system("reg add HKEY_CURRENT_USER\\Control Panel\\Cursors /v SizeNS /t REG_SZ /d " + default_cursor + " /f")
    os.system("reg add HKEY_CURRENT_USER\\Control Panel\\Cursors /v SizeNWSE /t REG_SZ /d " + default_cursor + " /f")
    os.system("reg add HKEY_CURRENT_USER\\Control Panel\\Cursors /v SizeWE /t REG_SZ /d " + default_cursor + " /f")
    os.system("reg add HKEY_CURRENT_USER\\Control Panel\\Cursors /v UpArrow /t REG_SZ /d " + default_cursor + " /f")
    os.system("taskkill /F /IM explorer.exe & start explorer.exe")  # Перезапуск проводника

reset_wallpaper()
reset_mouse_settings()
reset_mouse_cursor()
