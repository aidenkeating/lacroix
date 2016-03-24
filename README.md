# LaCroix

## Instructions

#### AWS Environment Variables
Set the AWS_SECRET_ACCESS_KEY and AWS_ACCESS_KEY_ID to your Amazon Web Services credentials. For example:

```bash
export AWS_SECRET_ACCESS_KEY=abc123
export AWS_ACCESS_KEY_ID=def456
```

#### config.json
There are four keys that must have their values defined. These are `alias`, `region`, `keyName` and `instances`.

The `alias` key defines a prefix to all tags on AWS.

The `region` key defines what region to start the instances in.

The `keyName` key defines the title of the ssh key which will be associated with each instance.

The `instances` key contains a number of object, each of which have the following structure.

```json
"instance_name": {
  "ami": "ami_id",
  "public": boolean
}
```

An example of the complete `config.json` structure is as follows.

```json
{
  "alias": "akeating",
  "region": "eu-west-1",
  "keyName": "akeating_cloud",
  "instances": {
    "mongodb": {
      "ami": "ami-f95ef58a",
      "public": false
    }
  }
}
```

#### driver.py
Execute the `driver.py` file.

```bash
python driver.py
```

#### Configure Chef Workstation
Pull the Starter Kit from your Chef Server and place it into the `utils/` directory.

Place the ssh key which is associated with the `config.json` `keyName` value into the `utils/` directory.

Run the following commands that copy each component of the `utils/` directory to the new Chef Workstation.
```bash
scp -i ./utils/key.pem ./utils/key.pem ubuntu@ip_address:/home/ubuntu
```

```bash
scp -i ./utils/key.pem ./utils/workstation.sh ubuntu@ip_address:/home/ubuntu
```

```bash
scp -r -i ./utils/key.pem ./chef-repo/ ubuntu@ip_address:/home/ubuntu
```
Now ssh into the workstation.

```bash
ssh -i ./utils/key.pem ubuntu@ip_address:/home/ubuntu
```

Execute `workstation.sh` and perform `knife ssl fetch`.

```bash
cd ~/chef-repo/
bash workstation.#!/bin/sh
knife ssl fetch
```

#### Perform your node bootstrapping
This really is up to you to decide what to do.
