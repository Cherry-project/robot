host=$( cat config/conf.json | jq '.ssh .host' )
ssh-keygen -t rsa
ssh-copy-id -i ~/.ssh/id_rsa.pub $host
#en user
eval $(ssh-agent -s)
ssh-add ~/.ssh/id_rsa.pub