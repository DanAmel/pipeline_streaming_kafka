from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import happybase as hb
import hbase
import json



def connectDB():
    #connection = hb.Connection( host='localhost')
    connection = hb.Connection('localhost')
    #print(connection.tables())
    table = connection.table('streaming_db')
    print(table)
    return table




def consumeData():
    consumer = KafkaConsumer("data", group_id="daniel", bootstrap_servers=['localhost:9092'])
    table = connectDB()


    for message in consumer:
        # message value and key are raw bytes -- decode if necessary!
        # e.g., for unicode: `message.value.decode('utf-8')`
        print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                            message.offset, message.key,
                                            json.loads(message.value)))
        value = json.loads(message.value)
        table.put(value["customer"], {'device': value["device"], 'action': value["action"], 'time': value["time"] })
        #with hbase.ConnectionPool("localhost:2182").connect() as conn:
        #    table = conn['customer']
        #    print(table)
        #    table.put(hbase.Row(
        #        value["customer"], {
        #            'device': value["device"],
        #            'action': value["action"],
        #            'time': value["time"],
        #        }
        #    ))
        #exit()
        
        
consumeData()