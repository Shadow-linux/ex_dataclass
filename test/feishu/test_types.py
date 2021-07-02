from ex_dataclass.ex_dataclass import ex_dataclass, field
import typing


@ex_dataclass
class MsgReqContentText:
    text: str = field(default_factory=str)


@ex_dataclass
class MsgReqContentPostTagText:
    text: str = field(default_factory=str)
    un_escape: bool = field(default_factory=bool)


@ex_dataclass
class MsgReqContentPostTagA:
    text: str = field(default_factory=str)
    href: str = field(default_factory=str)


@ex_dataclass
class MsgReqContentPostTagAt:
    user_id: str = field(default_factory=str)
    user_name: str = field(default_factory=str)


@ex_dataclass
class MsgReqContentPostLang:
    title: str = field(default_factory=str)
    content: typing.List[typing.List[
        typing.Union[MsgReqContentPostTagText,
                     MsgReqContentPostTagA,
                     MsgReqContentPostTagAt]]] = field(default_factory=list)


@ex_dataclass
class MsgReqContentPost:
    zh_cn: typing.Type[MsgReqContentPostLang] = field(default_factory=MsgReqContentPostLang)
    en_us: MsgReqContentPostLang = field(default_factory=MsgReqContentPostLang)


@ex_dataclass(ex_debug=False)
class MsgReq:
    receive_id: str = field(default_factory=str)
    msg_type: str = field(default_factory=str)
    content: typing.Union[MsgReqContentText, MsgReqContentPost] = field(default_factory=MsgReqContentText)


body = MsgReq(**{
    "receive_id": "xxxxx",
    "msg_type": "text",
    "content": {
        "zh_cn": {
            "title": "title1",
            "content": [
                [{
                  "user_id": "1",
                    "user_name": "xxx"
                },{
                    "text": "xxx",
                    "href": "xxx",
                }]
            ]
        },
        "en_us": {}
    }
})


print(body)
