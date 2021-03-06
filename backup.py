# setting firewall
firewall:
- action: accept
  chain: input
  comment: '"remote access for rinet"'
  src-address-list: '"remote_access"'

- action: accept
  chain: input
  comment: '"accept established,related,untracked"'
  connection-state: established,related,untracked

- action: drop
  chain: input
  comment: '"drop invalid"'
  connection-state: invalid

- action: accept
  chain: input
  comment: '"accept ICMP"'
  protocol: icmp

- action: drop
  chain: input
  comment: '"drop all not coming from LAN"'
  in-interface-list: "!LAN"

- action: accept
  chain: forward
  comment: '"accept established,related, untracked"'
  connection-state: established,related,untracked

- action: drop
  chain: forward
  comment: '"drop invalid"'
  connection-state: invalid

- action: drop
  chain: forward
  comment:  '"drop all from WAN not DSTNATed"'
  connection-nat-state: "!dstnat"
  connection-state: new
  in-interface-list: WAN

mangle:

  - dst-address: '"!192.168.88.0/24"'
    action: mark-connection
    chain: forward
    connection-mark: no-mark
    new-connection-mark: new_mark_conn
    passthrough: "yes"
    comment: '"auto mangle rule"'

  - action: mark-packet
    chain: forward
    connection-mark: "new_mark_conn"
    new-packet-mark: "mark_packet->new_con"
    passthrough: "yes"
    comment: '"auto mangle rule"'

address-list:
  - address: "86.62.127.224/28"
    list: '"remote_access"'

  - address: "86.62.82.242"
    list: '"remote_access"'

  - address: "172.16.255.254"
    list: '"remote_access"'

  - address: "10.10.0.1"
    list: '"remote_access"'

service-port:
  - sip-direct-media: 'no sip'

# setting logging
logging:
  - numbers: 0
    action: disk
    disabled: 'no'
    topics: '"info,!ppp,!wireless"'

  - numbers: 1
    action: disk
    disabled: 'no'
    topics: '"error"'


  - numbers: 2
    action: disk
    disabled: 'no'
    topics: '"warning"'


  - numbers: 3
    action: disk
    disabled: 'no'
    topics: '"critical"'

# setting queue
queue:

    - limit-at: tx_rate
      max-limit: tx_rate
      name: pcq_upload
      packet-mark: '"mark_packet->new_con"'
      parent: global
      queue: pcq-upload-default


    - limit-at: tx_rate
      max-limit: tx_rate
      name: pcq_download
      packet-mark: '"mark_packet->new_con"'
      parent: global
      queue: pcq-download-default

# settings users
users:

  - name: zabbix
    password: Putilin48
    group: full
    address: '"10.10.0.1"'


  - name: rinet
    password: rinetsupport
    group: full

# settings clock and ntp
clock:

  - time-zone-autodetect: 'no'
    time-zone-name: '"Europe/Moscow"'

ntp:
  - primary-ntp: '"195.54.192.33"'
    enabled: "yes"

