How to use this template:

1. Go to the AWS CloudFormation console.
2. Click "Create stack" and upload the template file.
3. Review and create the stack.

After the stack is created:

1. Access the WordPressAdminURL from the CloudFormation Outputs tab. Default username is 'user'.

2. Retrive your wordpress password by opening your Lightsail console (https://lightsail.aws.amazon.com/ls/webapp/home/instances), selecting the new instance and following the instructions from the 'Retrieve default password' section executing commands on CloudShell similar to this:

```
cat <<'EOT' >~/lightsail_connect

set -eu -o pipefail

instance=$1

giad=$(aws lightsail get-instance-access-details --protocol ssh --instance-name $instance | jq '.accessDetails')
userhost=$(jq -r '.ipAddress' <<<$giad)
username=$(jq -r '.username' <<<$giad)

work_dir=$(mktemp -d)
trap "{ rm -rf $work_dir; }" EXIT

kh_lines=$(jq -r --arg arg_host $userhost '.hostKeys[] | $arg_host+" "+.algorithm+" "+.publicKey' <<<$giad)
while read kh_line; do
  echo "$kh_line" >> $work_dir/hostkeys
done <<<"$kh_lines"

jq -r '.certKey'    <<<$giad > "$work_dir/key-cert.pub"
jq -r '.privateKey' <<<$giad > "$work_dir/key"
chmod 600 "$work_dir/key"

shift
ssh \
  -o StrictHostKeyChecking=yes \
  -o UserKnownHostsFile=$work_dir/hostkeys \
  -i $work_dir/key \
  $username@$userhost \
  $@
EOT

chmod +x ~/lightsail_connect
AWS_REGION=us-east-1 ~/lightsail_connect MyWordPresssite 
cat bitnami_application_password
```

<img width="832" alt="Screenshot 2024-07-29 at 4 07 53 PM" src="https://github.com/user-attachments/assets/e4b16b8f-66bb-40fe-b69b-a6058277287d">

