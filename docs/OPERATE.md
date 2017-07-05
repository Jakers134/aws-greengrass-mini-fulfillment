## Operating the Mini Fulfillment center example
### Preparation
From your development machine open two command line terminals per host, for a 
total of six. The following instructions assume you have open and connected:
* `master-pi` terminal `01` and `02`
* `sort_arm-pi` terminals `01` and `02`
* `inv_arm-pi` terminals `01` and `02`

### To start device operations of the Master host `master-pi`
**Start GG Core** -- in `master-pi` Terminal `01` execute:
1. `cd /greengrass`
1. `sudo ./greengrassd start`
You should now see `syncmanager`, `connmanager`, `certmanager`, `spectre` or other 
processes owned by `ggc_user` in the process list, by using the command `top -u ggc_user`.

**Start GG Devices** -- in `master-pi` Terminal `02` execute:

1. `cd ~/mini-fulfillment/groups/`
1. `chmod 755 master/start_master.sh master/stop_master.sh`
1. `./master/start_master.sh`

**Note:** you should see the white button light turn on

After starting the master devices, to determine success you should see four 
entries in the list of processes, similar to the following:
```
master-pi$ screen -ls
There are screens on:
	8281.web	(11/19/2016 05:53:42 PM)	(Detached)
	8278.heartbeat	(11/19/2016 05:53:42 PM)	(Detached)
	8275.button	(11/19/2016 05:53:42 PM)	(Detached)
	8269.belt	(11/19/2016 05:53:42 PM)	(Detached)
4 Sockets in /var/run/screen/S-pi.
```
To view the output of any of the Greengrass Devices attach to the 
`screen` by using the command `screen -r <pid>`. Example that 
re-attaches to the `web` device process in the above list:
```
screen -r 8281
```
:warning: Remember to detach from the screen using `Ctrl-A, D` **not** `Ctrl-C`. 
Using `Ctrl-C` will exit the process being viewed.

If the `button` device started successfully the physical button lights will turn on.
If the `belt` device started successfully you'll see `[btt.__init__] frequency:<value>` 
in the output.

### To stop device operations of the Master host
**Stop GG Devices** -- in a `master-pi` Terminal execute:
1. `cd ~/mini-fulfillment/groups/master`
1. `./stop_master.sh`

### To start device operations of Arm host `sort_arm-pi`
**Start GG Core** -- in Terminal `01` execute:
1. `cd /greengrass`
1. `sudo ./greengrassd start`
You should now see `syncmanager`, `connmanager`, `certmanager`, `spectre` or other 
processes owned by `ggc_user` in the process list, by using the command `top -u ggc_user`.

**Start GG Devices** -- in Terminal `02` execute:

1. `cd ~/mini-fulfillment/groups/arm`
1. `chmod 755 arm/start_sort_arm.sh arm/stop_arm.sh`
1. `./start_sort_arm.sh`

After starting the arm, to determine success you should see two entries in the 
list of processes, similar to the following:
```
$ screen -ls
There are screens on:
	4961.heartbeat	(19/11/16 18:10:51)	(Detached)
	4958.arm	(19/11/16 18:10:51)	(Detached)
2 Sockets in /var/run/screen/S-pi.
```
To view the output of any of the Greengrass Devices attach to the 
`screen` by using the command `screen -r <pid>`. For example, the following command 
attaches to the `arm` device process in the above list:
```
screen -r 4958
```
:warning: Remember to detach from the screen using `Ctrl-A, D` **not** `Ctrl-C`. 
Using `Ctrl-C` will exit the process being viewed.

### To start device operations of Arm host `inv_arm-pi`
**Start GG Core** -- in Terminal 01 execute:
1. `cd /greengrass`
1. `sudo ./greengrassd start`
You should now see `syncmanager`, `connmanager`, `certmanager`, `spectre` or other 
processes owned by `ggc_user` in the process list, by using the command `top -u ggc_user`.

**Start GG Devices** -- in Terminal 02 execute:

1. `cd ~/mini-fulfillment/groups/arm`
1. `chmod 755 arm/start_inv_arm.sh arm/stop_arm.sh`
1. `./start_inv_arm.sh`

After starting the arm, to determine success you should see two entries in the 
list of processes, similar to the following:
```
$ screen -ls
There are screens on:
	4961.heartbeat	(19/11/16 18:10:51)	(Detached)
	4958.arm	(19/11/16 18:10:51)	(Detached)
2 Sockets in /var/run/screen/S-pi.
```
To view the output of any of the Greengrass Devices attach to the 
`screen` by using the command `screen -r <pid>`. For example, the following command 
attaches to the `arm` device process in the above list:
```
screen -r 4958
```
:warning: Remember to detach from the screen using `Ctrl-A, D` **not** `Ctrl-C`. 
Using `Ctrl-C` will exit the process being viewed.

### To stop device operations of an Arm host
**Stop GG Devices** -- in the Arm's terminal, execute:
1. `cd ~/mini-fulfillment/groups/arm/`
1. `./stop_arm.sh`

### To start overall example operations
Push the **`green`** button to start both robot arms and the conveyor belt.

### To stop overall example operations
Push the **`red`** button to stop. 

### Using the white toggle button
The **`white`** button is a manual override that interacts with the Master 
Greengrass Core's local shadow to reverse the current direction of the conveyor 
belt. During normal operation this button is unnecessary; however, this button 
can be useful when demonstrating interactivity with the mini fulfillment center. 