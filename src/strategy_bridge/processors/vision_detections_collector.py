import attr

from strategy_bridge.bus import DataWriter
from strategy_bridge.common import config
from strategy_bridge.processors import BaseProcessor
from strategy_bridge.pb.messages_robocup_ssl_wrapper_pb2 import SSL_WrapperPacket
from strategy_bridge.larcmacs.receiver import ZmqReceiver


@attr.s(auto_attribs=True)
class VisionDetectionsCollector(BaseProcessor):

    max_records_to_persist: int = 30
    records_writer: DataWriter = attr.ib(init=False)
    receiver: ZmqReceiver = attr.ib(init=False)

    def __attrs_post_init__(self) -> None:
        self.records_writer = DataWriter(config.VISION_DETECTIONS_TOPIC, self.max_records_to_persist)
        self.receiver = ZmqReceiver(port=config.VISION_DETECTIONS_SUBSCRIBE_PORT)
        self._ssl_converter = SSL_WrapperPacket()

    async def process(self):
        message = self.receiver.next_message()
        if not message:
            return
        package = self._ssl_converter.FromString(message)
        self.records_writer.write(package)
