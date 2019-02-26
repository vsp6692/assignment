# IIS Debug Steps

1. Checked the http://localhost whether its reachable and got response "503 service unavailable"

2. Restarted IIS service and then rebooted the machine. Both steps didnt work out.

3. Checked the logs of IIS service in server manager. I came across three events with two warnings and one error. Then debugged the log could see DefaultAppPool is not able to start. 

## Issue

Identity for DefaultAppPool was missing. It was started with invalid custom account. So service was not able to start.

## Fixes

1. Search "inetmgr" in start bar and open IIS in administrator mode.

2. Click DefaultAppPool in open Advanced Settings.

3. Change identity from CustomAccount to Built-in account (Local System) which have admin access.

4. Then start application pool.

5. Check http://localhost and you can see the page.