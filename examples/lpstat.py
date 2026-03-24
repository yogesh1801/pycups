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

  def list_destinations(self, long_status=False):
    dests = self.conn.getDests()

    for dest in dests:
        if dest.instance:
            print(f"{dest.name}/{dest.instance}", end="")
        else:
            print(dest.name, end="")

        if long_status:
            options = dest.options
            _opt = lambda key: (o := options.get(key)) and o.value or None

            printer_uri_supported = _opt("printer-uri-supported")
            printer_is_temporary = _opt("printer-is-temporary")
            device_uri = _opt("device-uri")

            if printer_is_temporary == "true":
                ptype = "temporary"
            elif printer_uri_supported:
                ptype = "permanent"
            else:
                ptype = "network"

            print(f" {ptype} {printer_uri_supported or 'none'} {device_uri or 'none'}")
        else:
            print()

    def show_forms(self, name: Optional[str] = None) -> int:
        if name is None:
            print("lpstat: form name required after '-f'", flush=True)
            return 1

        if name:
            print(f"lpstat: forms are not supported by CUPS (requested: {name})")
        return 0

    def connect_to_host(self, hostname: Optional[str] = None) -> int:
        import sys
        if not hostname:
            print(
                'lpstat: Error - expected hostname after "-h" option.',
                file=sys.stderr,
            )
            return 1

        from cups import setServer
        setServer(hostname)
        return 0

    def show_long_status(self) -> None:
        self.list_destinations(long_status=2)
