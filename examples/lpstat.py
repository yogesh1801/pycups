from .base import _Base
from cups.types.cups import cupsDest, IPPRequest
from cups.types.ipp import IPPAttribute
from cups.enums import IPPOp, IPPTag, IPPStatus
from cups.generic import getUser
from cups import _cups
from typing import Optional, Dict
from datetime import datetime

_ffi = _cups.ffi
_lib = _cups.lib

PATTRS = [
    "printer-name",
    "printer-state",
    "printer-state-message",
    "printer-state-reasons",
    "printer-state-change-time",
    "printer-type",
    "printer-info",
    "printer-location",
    "printer-make-and-model",
    "printer-uri-supported",
    "requesting-user-name-allowed",
    "requesting-user-name-denied",
]

JATTRS = ["job-id", "job-state"]


class Lpstat(_Base):
    def show_default_printer(self) -> Optional[cupsDest]:
        default_printer = self.conn.getNamedDest()
        if default_printer is None:
            print("no system default destination")
        else:
            print(f"system default destination: {default_printer.name}")
        return default_printer