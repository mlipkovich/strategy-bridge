from strategy_bridge.bus import data_bus
from strategy_bridge.common import config
from strategy_bridge.processors import VisionDetectionsCollector, RobotCommandsSender
from strategy_bridge.processors.matlab_controller import MatlabController
from strategy_bridge.processors.referee_commands_collector import RefereeCommandsCollector
from strategy_bridge.runner import Runner


config.init_logging()


processors = [
    VisionDetectionsCollector(),
    RefereeCommandsCollector(),
    MatlabController(),
    RobotCommandsSender()
]

runner = Runner(processors=processors)
runner.run()


ssl_packages = data_bus.read_all(config.VISION_DETECTIONS_TOPIC)
referee_commands = data_bus.read_all(config.REFEREE_COMMANDS_TOPIC)
control = data_bus.read_all(config.ROBOT_COMMANDS_TOPIC)
