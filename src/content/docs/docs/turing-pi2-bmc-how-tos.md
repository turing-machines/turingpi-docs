---
title: "How To's"
description: "The BMC UI uses self-signed certificates. Open a terminal on your computer and execute the following command to regenerate them. ( default password: turing)."
head:
  - tag: title
    content: "How To's | BMC | Turing Pi 2 | Turing Pi Docs"
lastUpdated: 2025-11-12
---

## Regenerate self-signed certificates UI

The BMC UI uses self-signed certificates. Open a terminal on your computer and execute the following command to regenerate them. ( default password: `turing`).

```shell

ssh root@turingpi '/etc/bmcd/generate_self_signedx509.sh && /etc/init.d/S94bmcd restart'
```

(Note: you may need to use `turingpi.local` or the IP address to access the BMC console using SSH)

## Replace certificates

The bmcd daemon, responsible for hosting the BMC-UI, has a configuration file in which alternative certificates can be configured. Replacing the self-signed certificates with one trusted by a CA improves the system's security.

1. On your computer, copy the new certificates to your BMC:

```text
scp my_cert.pem my_key.pem root@turingpi.local:/etc/ssl/certs/ 
```

2. Login to the BMC:

```shell
ssh root@turingpi.local
```

3. Make sure the permissions of the copied certificates are correct.

```shell
chmod 644 /etc/ssl/certs/*.pem
```

4. Edit the bmcd config:

```shell
nano /etc/bmcd/config.yaml
```

5. Find and replace the "tls" section with the pem files we copied earlier:

```yaml
...
tls:
  certificate: /etc/ssl/certs/my_cert.pem
  private_key: /etc/ssl/certs/my_key.pem
```

6. Save the file and exit
7. Restart the bmcd daemon:

```
/etc/init.d/S94bmcd restart
```
