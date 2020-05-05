How 2 run:
---
1. run docker-compose up -d
   two docker containers will be up and running if everything went smooth
   one of them will have localhost:9092 port exposed
   
2. run:

   2.1 in 1st console: 
   ./KafkaTest.py --cp=p --addr=localhost:9092 --topic=test

   2.2 in 2nd console 
   ./KafkaTest.py --cp=c --addr=localhost:9092 --topic=test
   
3. see messages are going from (p)roducer to (c)onsumer

   
Some problems found (dont want to investigate for now):
---
1. raised localhost:9092 is not seen from other comp in local network
2. only 1 consumer could consume messages 
