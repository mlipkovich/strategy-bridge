import json

import attr

from strategy_bridge.bus import DataWriter
from strategy_bridge.common import config
from strategy_bridge.model.referee import RefereeCommand
from strategy_bridge.processors import BaseProcessor
from strategy_bridge.larcmacs.receiver import ZmqReceiver


@attr.s(auto_attribs=True)
class RefereeCommandsCollector(BaseProcessor):

    max_records_to_persist: int = 30
    records_writer: DataWriter = attr.ib(init=False)
    receiver: ZmqReceiver = attr.ib(init=False)

    def __attrs_post_init__(self) -> None:
        self.records_writer = DataWriter(config.REFEREE_COMMANDS_TOPIC, self.max_records_to_persist)
        self.receiver = ZmqReceiver(port=config.REFEREE_COMMANDS_SUBSCRIBE_PORT)

    async def process(self):
        message = self.receiver.next_message()
        if not message:
            return
        parsed_message = json.loads(bytes(message))
        command = RefereeCommand(
            state=parsed_message['state'],
            commandForTeam=parsed_message['team'],
            isPartOfFieldLeft=parsed_message['is_left'],
        )
        self.records_writer.write(command)
