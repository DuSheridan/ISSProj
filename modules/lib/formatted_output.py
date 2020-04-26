from enum import Enum, unique
import json
import traceback

from modules.lib.decimal_encoder import DecimalEncoder


@unique
class Status(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"
    UNKNOWN = "unknown"

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


class Output:
    def __init__(
            self,
            status=Status.UNKNOWN,
            title="",
            message="",
            code="",
            data="",
            trace=False,
            optional={},
    ):
        self.status = status
        self.title = title
        self.message = message
        self.code = code
        self.data = data
        self.enable_trace = trace
        self.optional = optional

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if isinstance(value, Status):
            if value in Status:
                self._status = value
            else:
                self._status = Status.UNKNOWN
        else:
            for status in Status:
                if value == status.value:
                    self._status = status
                    break
            else:
                self._status = Status.UNKNOWN

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = str(value)

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = str(value)

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = str(value)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if not value:
            self._data = ""
        elif type(value) is dict or type(value) is list:
            self._data = json.loads(json.dumps(value, cls=DecimalEncoder), encoding='utf-8')
        else:
            try:
                self._data = json.loads(value, encoding='utf-8')
            except json.decoder.JSONDecodeError:
                raise

    @property
    def trace(self):
        trace = traceback.format_exc()
        return trace

    @property
    def optional(self):
        return self._optional

    @optional.setter
    def optional(self, value):
        if type(value) is dict:
            self._optional = value
        else:
            try:
                self._optional = self.optional
            except AttributeError:
                self._optional = {}

    def as_dict(self, optional=False, trace=None):
        temp = {
            "status": {
                "name": self.status.value,
                "title": self.title,
                "message": self.message,
                "code": self.code,
                "trace": None,
            },
            "data": {},
            "optional": None,
        }
        if self.data:
            temp["data"] = self.data
        if optional:
            temp["optional"] = self.optional
        if (trace is not None and trace) or (
                trace is None and self.enable_trace
        ):
            temp["status"]["trace"] = self.trace.encode('UTF-8')
        else:
            temp["status"]["trace"] = None
        return temp

    def __str__(self):
        return str(self.as_dict(optional=True))

    def __repr__(self):
        return "{}({},{},{},{},{},{})".format(
            self.__class__.__name__,
            self.status,
            self.title,
            self.message,
            self.code,
            self.data,
            self.enable_trace,
            self.optional,
        )
