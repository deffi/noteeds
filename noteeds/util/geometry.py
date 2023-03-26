from PySide6.QtCore import QRect, Qt


def adjust_size(rect: QRect, dw: int, dh: int, layout_direction: Qt.LayoutDirection) -> None:
    if layout_direction == Qt.RightToLeft:
        rect.adjust(-dw, -dh, 0, 0)
    else:
        rect.adjust(0, 0, dw, dh)
