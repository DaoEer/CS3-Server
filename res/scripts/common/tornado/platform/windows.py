# NOTE: win32 support is currently experimental, and not recommended
# for production use.


from __future__ import absolute_import, division, print_function, with_statement
#@TODO(phw): import ctypes
#@TODO(phw): import ctypes.wintypes

# See: http://msdn.microsoft.com/en-us/library/ms724935(VS.85).aspx
#@TODO(phw): SetHandleInformation = ctypes.windll.kernel32.SetHandleInformation
#@TODO(phw): SetHandleInformation.argtypes = (ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD, ctypes.wintypes.DWORD)
#@TODO(phw): SetHandleInformation.restype = ctypes.wintypes.BOOL

HANDLE_FLAG_INHERIT = 0x00000001


def set_close_exec(fd):
    success = SetHandleInformation(fd, HANDLE_FLAG_INHERIT, 0)
    if not success:
        raise ctypes.GetLastError()
