import winreg
import inspect
import ctypes


# 强行杀死线程
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    return res
    '''
    if res == 0: raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
    '''

# 强行杀死线程
def stop_thread(thread):
    if hasattr(thread,"ident") and thread.ident != None:
        _async_raise(thread.ident, SystemExit)


def edit_system_proxy(open_or_close, host=None, port=None):
    """
    修改系统代理函数
    :param open_or_close: 是否开启 bool
    :param host: IP
    :param port: 端口
    :return:
    """
    proxy = f"{host}:{port}"
    root = winreg.HKEY_CURRENT_USER
    proxy_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
    kv_Enable = [
        (proxy_path, "ProxyEnable", 1, winreg.REG_DWORD),
        (proxy_path, "ProxyServer", proxy, winreg.REG_SZ),
    ]

    kv_Disable = [
        (proxy_path, "ProxyEnable", 0, winreg.REG_DWORD),
        # (proxy_path, "ProxyServer", proxy, winreg.REG_SZ),
    ]
    if open_or_close:
        kv = kv_Enable
    else:
        kv = kv_Disable
    for keypath, value_name, value, value_type in kv:
        hKey = winreg.CreateKey(root, keypath)
        winreg.SetValueEx(hKey, value_name, 0, value_type, value)