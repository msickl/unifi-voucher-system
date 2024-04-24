[Unit]
Description=Run Voucher Service Daily at Midnight

[Timer]
OnCalendar=*-*-* {{ data.hour }}:{{ data.minute }}:{{ data.second }}
Persistent=true

[Install]
WantedBy=timers.target