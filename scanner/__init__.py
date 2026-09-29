from ctypes.wintypes import tagRECT
from api_scanner.scanner import ALL_CHECKS


for check_class in ALL_CHECKS:
    check = check_class()
    findings = check.run(tagRECT)
