# cbqos-snmp-discovery

Auto discovery cisco class based QoS SNMP configuration, Please use Python3.7.x+

## Usage

```
$ pip install -r requirements.txt
```

change the device list and snmp community in `device.yml`

```
$ python main.py
```

the results located in `output` folder with json format.

and also print the table for class map snmp stats
