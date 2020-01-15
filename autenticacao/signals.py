from django.db.models.signals import post_save
from django.dispatch import receiver
from lancamento.models import Lancamento
from .models import RegistroMovimento
import sys
import asyncio
from aio_pika import connect, Message, DeliveryMode, ExchangeType
import json

async def main(loop, msg):
    # Perform connection
    connection = await connect(
        "amqp://guest:guest@localhost/", loop=loop
    )

    # Creating a channel
    channel = await connection.channel()

    topic_logs_exchange = await channel.declare_exchange(
        'topic_logs', ExchangeType.TOPIC
    )

    routing_key = (
        sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
    )

    message_body = json.dumps(msg).encode('utf-8')

    message = Message(
        message_body,
        delivery_mode=DeliveryMode.PERSISTENT
    )

    # Sending the message
    await topic_logs_exchange.publish(
        message, routing_key=routing_key
    )

    print(" [x] Sent %r" % message)

    await connection.close()
   
@receiver(post_save, sender=Lancamento)
def update_registro(sender, instance, created,**kwargs):
    if created:
        # wrap_dict = {'id_objeto':instance.id,
        #              'processo':'Lançamento',
        #              'valor':instance.valor}
    
        # loop = asyncio.new_event_loop()
        # loop.run_until_complete(main(loop,wrap_dict))    
        RegistroMovimento.objects.create(id_objeto=instance.id,
                                         processo='Lançamento',
                                         valor=instance.valor)