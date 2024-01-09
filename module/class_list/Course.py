from typing import List


class Course:
    headers = ["STT", "Loại", "Mã LHP", "Số lượng", "Lịch học", "Ghi chú"]

    def __init__(
        self,
        order: int = -1,
        type: str = "",
        code: str = "",
        remain: str = "",
        schedule: str = "",
        note: str = "",
        id: str = "",
    ):
        self.order = order
        self.type = type
        self.code = code
        self.remain = remain
        self.schedule = schedule
        self.note = note
        self.id = id

    def getArrayData(self) -> List:
        return [self.order, self.type, self.code, self.remain, self.schedule, self.note]
