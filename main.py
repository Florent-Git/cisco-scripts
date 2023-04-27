import pexpect
import click


@click.command()
@click.option('-u', '--url', help="SSH url to connect to the host")
@click.option('-u', '--user', help="Cisco SSH user")
@click.option('-p', '---password', prompt=True, hide_input=True, help="Cisco SSH password")
@click.option('--ssh-version', type=click.Choice("1", "2"))
def get_running_config(ip_address: str, user: str, _password: str, ssh_version: str):
    with pexpect.spawn(f"ssh{ssh_version if ssh_version == '1' else ''} {user}@{ip_address}") as ssh:
        # ssh.logfile_read = sys.stdout.buffer
        ssh.expect("Password:")
        ssh.sendline(_password)
        ssh.expect(">")
        ssh.sendline("ena")
        ssh.expect("#")
        ssh.sendline("terminal length 0")
        ssh.expect("#")
        ssh.sendline("sh run")
        ssh.expect("#")
    
    run_config = ssh.before.decode("utf-8")

    with open("./run-config.txt", "w") as file:
        file.write(run_config[run_config.find("!"):run_config.rfind("end") + 3])

if __name__ == "__main__":
    get_running_config()
