### Network Detection Design Logic

#### All Redis Cache Key Definitions for Network Detection

```plaintext
"network:query:queue" is a list type, storing all network detection task information. A scheduled task periodically retrieves data from lpop, value type: ["network&tcp_query_ports&udp_query_ports", ...]
"network&tcp_query_ports&udp_query_ports" is a list type. Before each scheduled task is added to "network:query:queue", a list of "network&tcp_query_ports&udp_query_ports" is generated, value type: [ip1, ip2, ...]
"network:crontab:task:time" is a hash type, storing all scheduled task information as follows, field is the detection task, value is the timestamp of the detection date
127.0.0.1:4580[1]> HGETALL "network:crontab:task:time"
1) "10.1.107.0/24&&"
2) "[1599397501, 1599397201]"
3) "10.2.0.0/24&22,443&53,67,546"
4) "[1599398701]"
```

#### Logic for Directly Starting Network Detection from the Frontend

- Flowchart

![Network Detection Process](https://github.com/charl-z/network_manage/blob/issue03/docs/image/%E7%BD%91%E7%BB%9C%E6%8E%A2%E6%B5%8B%E6%B5%81%E7%A8%8B.jpg)

- Code as follows:

```python
# Traverse the network, adding IPs in the network to Redis cache:
ips = IP(network)
    for ip in ips:
        ip = str(ip)
        r.rpush(network_scan_redis_info, ip)  # Add each IP address's detection info in the network to Redis, key value is network_scan_redis_info
r.rpush(conf_data['NETWORK_QUERY_QUEUE'], network_scan_redis_info)
# Network detection scheduled service, periodically reads tasks from the network detection queue:
while True:
    time.sleep(10)
    thread_list = []
    for i in range(10):
        if r.llen(conf_data['NETWORK_QUERY_QUEUE']) != 0:
            network = r.lpop(conf_data['NETWORK_QUERY_QUEUE'])
            t = threading.Thread(target=call_exec_network_query, args=(network,))
            thread_list.append(t)
        else:
            break
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()
# Read values from the network detection queue as keys to retrieve all values for network detection
while True:
    try:
        thread_list = []
        for i in range(ips):
            if r.llen(redis_network_info) != 0:
                ip = r.lpop(redis_network_info)
                t = threading.Thread(target=self.exec_port_scan, args=(ip, tcp_scan_ports, udp_scan_ports, network))
                thread_list.append(t)
            else:
                break
        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()

    except Exception as e:
        pass

    if r.llen(redis_network_info) == 0:
        logging.info("Network detection task completed: {0}".format(redis_network_info))
        sql = "select count(1) from network_query_result where network = '{0}'".format(network)
        self.cur_psql.execute(sql)
        online_ip_num = int(self.cur_psql.fetchall()[0][0])
        sql = "update network_query_task SET online_ip_num={0}, query_status=2 where network='{1}';".format(online_ip_num, network)
        self.cur_psql.execute(sql)
        self.conn_psql.commit()
        break
```

#### Logic for Scheduled Start of Network Detection

- Flowchart

![Scheduled Network Detection Process](https://github.com/charl-z/network_manage/blob/issue03/docs/image/%E7%BD%91%E7%BB%9C%E5%AE%9A%E6%97%B6%E6%8E%A2%E6%B5%8B%E6%B5%81%E7%A8%8B.jpg)

- Code as follows:

```python
# Create a new network detection
if auto_enable:  # If the scheduled task is enabled, then update the scheduled task data in the Redis hash table
    crontab_task_dict = dict()
    crontab_task_dict["{0}&{1}&{2}".format(network, tcp_query_ports, udp_query_ports)] = crontab_task.replace("'", '"')
    add_crontab_task_to_redis(crontab_task_dict, conf_data["NETWORK_QUETY_CRONTAB_HASH"])
# The scheduled task process periodically checks the network:crontab:task:time hash table for network detection information timestamps
all_crontab_tasks = r.hgetall(conf_data["NETWORK_QUETY_CRONTAB_HASH"])
    now = int(datetime.datetime.now().timestamp())
    for network_info in all_crontab_tasks:
        crontab_times = json.loads(all_crontab_tasks[network_info])
        for crontab_time in crontab_times:
            if now > int(crontab_time): # Timestamp is greater than the current time
                network_info = network_info.split("&")
                network, tcp_query_ports, udp_query_ports = network_info[0], network_info[1], network_info[2]
                network_scan_redis_info = "{0}&{1}&{2}".format(network, tcp_query_ports, udp_query_ports)
                ips = IP(network)
                # Add each IP address's detection info in the network to Redis, key value is network_scan_redis_info
# Traverse the network, adding IPs in the network to Redis cache
                for ip in ips:
                    ip = str(ip)
                    r.rpush(network_scan_redis_info, ip)
# Add network detection info to Redis's network detection cache queue
                r.rpush(conf_data['NETWORK_QUERY_QUEUE'], network_scan_redis_info)
                logging.info("{0}&{1}&{2}, added to Redis network detection task list".format(network, tcp_query_ports, udp_query_ports))
# Update the timestamp in the network:crontab:task:time hash table
                # todo After adding the scheduled task to the cache list, update the scheduled task's hash table again
                network_query_crontab_task_info = get_network_query_crontab_task(network=network)
                add_crontab_task_to_redis(network_query_crontab_task_info, conf_data["NETWORK_QUETY_CRONTAB_HASH"])
                logging.info("Scheduled task updated: {0}".format(network_query_crontab_task_info))
# Network detection scheduled service, periodically reads tasks from the network detection queue:
while True:
    time.sleep(10)
    thread_list = []
    for i in range(10):
        if r.llen(conf_data['NETWORK_QUERY_QUEUE']) != 0:
            network = r.lpop(conf_data['NETWORK_QUERY_QUEUE'])
            t = threading.Thread(target=call_exec_network_query, args=(network,))
            thread_list.append(t)
        else:
            break
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()
# Read values from the network detection queue as keys to retrieve all values for