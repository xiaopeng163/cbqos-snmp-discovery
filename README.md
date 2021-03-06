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

```
host= xr1.cisco.com
interface=GigabitEthernet0/0/0/0 direction=output policy_name=cbqos-demo
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃            classmap ┃ policy_index ┃ object_index ┃                               cbQosCMPrePolicyByte64 ┃                               cbQosCMPostPolicyByte64 ┃                                     cbQosCMDropByte64 ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│           cls-voice │   1859430819 │   1141124091 │ 1.3.6.1.4.1.9.9.166.1.15.1.1.6.1859430819.1141124091 │ 1.3.6.1.4.1.9.9.166.1.15.1.1.10.1859430819.1141124091 │ 1.3.6.1.4.1.9.9.166.1.15.1.1.17.1859430819.1141124091 │
│       class-default │   1859430819 │   1192737166 │ 1.3.6.1.4.1.9.9.166.1.15.1.1.6.1859430819.1192737166 │ 1.3.6.1.4.1.9.9.166.1.15.1.1.10.1859430819.1192737166 │ 1.3.6.1.4.1.9.9.166.1.15.1.1.17.1859430819.1192737166 │
│           cls-video │   1859430819 │   1333719002 │ 1.3.6.1.4.1.9.9.166.1.15.1.1.6.1859430819.1333719002 │ 1.3.6.1.4.1.9.9.166.1.15.1.1.10.1859430819.1333719002 │ 1.3.6.1.4.1.9.9.166.1.15.1.1.17.1859430819.1333719002 │
│ cls-network-control │   1859430819 │   1657844269 │ 1.3.6.1.4.1.9.9.166.1.15.1.1.6.1859430819.1657844269 │ 1.3.6.1.4.1.9.9.166.1.15.1.1.10.1859430819.1657844269 │ 1.3.6.1.4.1.9.9.166.1.15.1.1.17.1859430819.1657844269 │
└─────────────────────┴──────────────┴──────────────┴──────────────────────────────────────────────────────┴───────────────────────────────────────────────────────┴───────────────────────────────────────────────────────┘
```


## cfg sample


```
class-map match-any cls-video
 match dscp af41 af42 af43
 end-class-map
!
class-map match-any cls-voice
 match dscp ef
 end-class-map
!
class-map match-any cls-network-control
 match dscp cs6 cs7
 end-class-map
!
policy-map cbqos-demo
 class cls-voice
  priority level 1
 !
 class cls-network-control
  bandwidth remaining percent 1
 !
 class cls-video
  bandwidth remaining percent 20
 !
 class class-default
 !
 end-policy-map
!
interface GigabitEthernet0/0/0/0
 description interface for demo
 service-policy output cbqos-demo
!
```
