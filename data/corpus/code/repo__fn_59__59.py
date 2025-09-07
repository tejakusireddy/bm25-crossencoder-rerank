def consumer(self, conn):
        """"""
        return Consumer(
            connection=conn,
            queue=self.queue.name,
            exchange=self.exchange.name,
            exchange_type=self.exchange.type,
            durable=self.exchange.durable,
            auto_delete=self.exchange.auto_delete,
            routing_key=self.routing_key,
            no_ack=self.no_ack,
        )