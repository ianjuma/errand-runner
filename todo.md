#### [ server ]


codrops button features - CSS
flask app
tune linux vm
tune iptables, ufw
dDos
dropping packets intelligently - iptables
nginx tuning + load balancing
apparmor, selinux
rkhunter tuning + rootkits

#### [ app ]

new relic
log watching + control - logrotate
celery - logging
elastic search + mongoDB river
celery periodic tasks - newsletter
in app logging - celery, flask
add exceptions on req/rep cycle
decomposition - class - file
subdomains - nginx
sessions -> redis, mongo
stats -> redis
task queue backend -> mongo, amqp

#### [ docker-container ]

smtp server container - mailing
rabbitmq + backends -> amqp
mongoDB replica set
mongod --master --port 27017 --dbpath /var/lib/mongodb --replSet rs0
mongod --slave --port 27018 --dbpath /var/lib/mongodb2 --replSet rs0
mongod --master --port 27017 --dbpath /var/lib/mongodb --replSet rs0
mongod --master --port 27017 --dbpath /var/lib/mongodb &
mongod --slave --port 27018 --source 127.0.0.1:27017 --dbpath /var/lib/mongodb2
mongod --slave --port 27018 --source synod:27017 --dbpath /var/lib/mongodb2




# stats with redis
# logins - sinups
# app features freq
# times app being used
# task creation time