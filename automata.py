import pexpect
import getpass

version = raw_input('Version: ')
secret = getpass.getpass('Enter Passphrase: ')
github_username = 'ianjuma'

clean = pexpect.spawn('fab clean')
clean.expect('Passphrase for private key:')
clean.send(secret)

deploy = pexpect.spawn('fab deploy:%s' %(version,))
deploy.expect('Passphrase for private key:')
deploy.sendline(secret)
deploy.expect("Username for 'https://github.com':")
deploy.sendline(github_username)
deploy.expect("Password for 'https://ianjuma@github.com':")
deploy.sendline(secret)
