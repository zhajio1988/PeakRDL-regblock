from typing import TYPE_CHECKING

from systemrdl.walker import WalkerAction

from .forloop_generator import RDLForLoopGenerator

if TYPE_CHECKING:
    from .exporter import RegblockExporter
    from systemrdl.node import AddressableNode


class ExternalWriteAckGenerator(RDLForLoopGenerator):
    def __init__(self, exp: 'RegblockExporter') -> None:
        super().__init__()
        self.exp = exp

    def get_implementation(self) -> str:
        content = self.get_content(self.exp.top_node)
        if content is None:
            return ""
        return content

    def enter_AddressableComponent(self, node: 'AddressableNode') -> WalkerAction:
        super().enter_AddressableComponent(node)

        if node.external:
            self.add_content(f"wr_ack |= {self.exp.hwif.get_external_wr_ack(node)};")
            return WalkerAction.SkipDescendants

        return WalkerAction.Continue


class ExternalReadAckGenerator(RDLForLoopGenerator):
    def __init__(self, exp: 'RegblockExporter') -> None:
        super().__init__()
        self.exp = exp

    def get_implementation(self) -> str:
        content = self.get_content(self.exp.top_node)
        if content is None:
            return ""
        return content

    def enter_AddressableComponent(self, node: 'AddressableNode') -> WalkerAction:
        super().enter_AddressableComponent(node)

        if node.external:
            self.add_content(f"rd_ack |= {self.exp.hwif.get_external_rd_ack(node)};")
            return WalkerAction.SkipDescendants

        return WalkerAction.Continue