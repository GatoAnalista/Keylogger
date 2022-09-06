netsh advfirewall firewall add rule name="Nullsys" dir=in action=allow protocol=TCP localport=42424
netsh advfirewall firewall add rule name="Nullsys" dir=out action=allow protocol=TCP localport=42424