Pending removal in Python 3.19
******************************

* "ctypes":

  * Implicitly switching to the MSVC-compatible struct layout by
    setting "_pack_" but not "_layout_" on non-Windows platforms.
