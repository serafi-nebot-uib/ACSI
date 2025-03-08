#!/bin/bash

prev_line=$(grep '^cpu ' /proc/stat)

# time_start and time_end are used to calculate the amount of time it takes to execute the monitor
time_start=$(date +%s%3N)

# loop 1440 times (2 hours / 5 seconds per iteration = 7200 / 5 = 1440)
for i in $(seq 1 1440); do
	# calculate the time to sleep taking into account monitor execution time
	time_end=$(date +%s%3N)
	time_sleep=$(echo "scale=3; 5 - ($time_end - $time_start) / 1000" | bc)
	sleep $time_sleep

	time_start=$(date +%s%3N)

	current_line=$(grep '^cpu ' /proc/stat)
	# sum all fields from user time onward (skip "cpu" label at $1)
	prev_total=$(echo "$prev_line" | awk '{sum=0; for(i=2; i<=NF; i++) sum+=$i; print sum}')
	# idle time is the 4th field after "cpu" (field $5)
	prev_idle=$(echo "$prev_line" | awk '{print $5}')

	# calculate total cpu time for current reading
	current_total=$(echo "$current_line" | awk '{sum=0; for(i=2; i<=NF; i++) sum+=$i; print sum}')
	current_idle=$(echo "$current_line" | awk '{print $5}')

	# compute differences between current and previous readings
	diff_total=$((current_total - prev_total))
	diff_idle=$((current_idle - prev_idle))

	# calculate cpu usage percentage
	# usage = ((total - idle) / total) * 100
	if [ "$diff_total" -gt 0 ]; then
		cpu_usage=$(echo "scale=2; ($diff_total - $diff_idle) * 100 / $diff_total" | bc)
	else
		cpu_usage=0
	fi

	# get ram usage in bytes from free command
	ram_line=$(free --bytes | sed -n '2p')
	ram_abs=$(echo $ram_line | awk '{print $3}')
	ram_percent=$(echo $ram_line | awk '{print $3/$2*100}')

	# print timestamp, cpu and ram usage
	printf "%s,%.4f,%u,%.4f\n" "$(date '+%Y-%m-%d %H:%M:%S')" $cpu_usage $ram_abs $ram_percent

	# update previous reading for the next iteration
	prev_line="$current_line"
done
