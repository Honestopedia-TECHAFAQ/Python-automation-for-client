import argparse
import paramiko

def update_host_config(host, username, password, config_value):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(host, username=username, password=password)

        command = f"echo '{config_value}' > /path/to/config/file"
        stdin, stdout, stderr = ssh.exec_command(command)

        if stdout.channel.recv_exit_status() == 0:
            print(f"Successfully updated configuration on host {host}")
            return True
        else:
            print(f"Failed to update configuration on host {host}")
            return False
    except Exception as e:
        print(f"Error updating configuration on host {host}: {str(e)}")
        return False
    finally:
        ssh.close()

def main():
    parser = argparse.ArgumentParser(description="Update configuration for hosts in the datacenter")
    parser.add_argument("username", help="SSH username for the hosts")
    parser.add_argument("password", help="SSH password for the hosts")
    parser.add_argument("config_value", help="Configuration value to update")
    parser.add_argument("hosts", nargs="+", help="List of hostnames or IP addresses")

    args = parser.parse_args()

    successful_updates = 0
    failed_updates = 0

    for host in args.hosts:
        if update_host_config(host, args.username, args.password, args.config_value):
            successful_updates += 1
        else:
            failed_updates += 1

    print(f"Successful updates: {successful_updates}")
    print(f"Failed updates: {failed_updates}")

if __name__ == "__main__":
    main()
