#!/usr/bin/env python

import sys, subprocess
import xapi, replace, tui, grub, networking, iptables, storage

def reboot():
	print >>sys.stderr, "Triggering an immediate reboot"
	cmd = [ "/sbin/reboot" ]
	x = subprocess.call(cmd)
	if x <> 0:
		print >>sys.stderr, "FAILED: to trigger a reboot (%s)" % (" ".join(cmd))

def stop_xend():
	print >>sys.stderr, "Permanently stopping xend"
	if subprocess.call(["/sbin/chkconfig", "--level", "345", "xend", "off"]) <> 0:
		print >>sys.stderr, "FAILED: to disable xend"
	if subprocess.call(["/sbin/service", "xend", "stop"]) <> 0:
		print >>sys.stderr, "FAILED: to stop xend"

if __name__ == "__main__":
	stop_xend ()
	xapi.start ()
	need_to_reboot = False
	r = grub.analyse()
	if r:
		need_to_reboot = True
		replace.file(r[0], r[1])
	r = networking.analyse()
	if r:
		need_to_reboot = True
		for change in r:
			replace.file(change[0], change[1])
		networking.restart()
	r = iptables.analyse()
	if r:
		replace.file(r[0], r[1])
		iptables.restart()
	storage.analyse()
	print "Welcome to XenServer!"
	if need_to_reboot:
		if tui.yesno("A reboot is needed to fully activate XenServer. Would you like to reboot now?"):
			reboot()
	
