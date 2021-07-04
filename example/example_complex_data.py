"""
复杂数据 + 数据多态 演示
本次例子都来源于飞书开发平台，飞书拥有很强大的且灵活的api，所以配置的数据也相对复杂；
"""
import typing
from ex_dataclass import ex_dataclass, asdict, field, EXPack

# ============================================= 示例一 =============================================

# 这是一个飞书平台的富文本消息数据结构, 可以看到它最终发送的内容其实是一个多态内容是不确定性的，下面看看ex_dataclass的表现
# https://open.feishu.cn/document/ukTMukTMukTM/uMDMxEjLzATMx4yMwETM
complex_data = {
    "open_id" : "ou_5ad573a6411d72b8305fda3a9c15c70e",
    "chat_id" : "oc_5ad11d72b830411d72b836c20",
    "email"   : "fanlv@gmail.com",
    "msg_type": "post",
    "content" : {
        "post": {
            "en_us": {},
            "zh_cn": {
                "title"  : "我是一个标题",
                "content": [
                    [
                        {
                            # 第一种 tag
                            "tag"      : "text",
                            "un_escape": True,
                            "text"     : "第一行&nbsp;:"
                        },
                        {
                            # 第二种 tag
                            "tag" : "a",
                            "text": "超链接",
                            "href": "http://www.feishu.cn"
                        },
                        {
                            # 第三种 tag
                            "tag"    : "at",
                            "user_id": "ou_18eac85d35a26f989317ad4f02e8bbbb"
                        }
                    ],
                    [
                        {
                            "tag"      : "text",
                            "un_escape": False,
                            "text"     : "第二行 :"
                        },
                        {
                            "tag"      : "text",
                            "un_escape": False,
                            "text"     : "文本测试"
                        }
                    ],
                    [
                        {
                            # 第四种 tag
                            "tag"      : "img",
                            "image_key": "d640eeea-4d2f-4cb3-88d8-c964fab53987",
                            "width"    : 300,
                            "height"   : 300
                        }
                    ]
                ]
            }
        }
    }
}


# 从上面的数据可以看到有3种不同tag的数据类型，但其实都是content, 下面看看怎么定义
@ex_dataclass
class TagBasic:
    tag: str = field(default_factory=str)


# 第一种 tag: text
@ex_dataclass
class TagText(TagBasic):
    text: str = field(default_factory=str)
    un_escape: bool = field(default_factory=bool)


# 第二种 tag: a
@ex_dataclass
class TagA(TagBasic):
    text: str = field(default_factory=str)
    href: str = field(default_factory=str)


# 第三种 tag: at
@ex_dataclass
class TagAt(TagBasic):
    user_id: str = field(default_factory=str)


# 第四种 tag: img
@ex_dataclass
class TagImg(TagBasic):
    image_key: str = field(default_factory=str)
    width: int = field(default_factory=int)
    height: int = field(default_factory=int)


@ex_dataclass
class PostContent:
    title: str = field(default_factory=str)


# 英文内容没有所以为空
@ex_dataclass
class EnUsContent(PostContent):
    pass


@ex_dataclass
class ZhCnContent(PostContent):
    # 可以看到它其实是有两层列表嵌套
    # 这里有两种写法：
    # 1、typing.Type 的意思是主要标注父类其子类也会被进行匹配
    # 2、typing.Union 就是其中之一：typing.Union[], 优先级从左往右匹配
    content: typing.List[typing.List[typing.Type[TagBasic]]] = field(default_factory=list)
    # content: typing.List[typing.List[typing.Union[TagA, TagAt, TagImg, TagText]]] = field(default_factory=list)


@ex_dataclass(ex_debug=False)
class PostLangOption:
    # 如果默认值是想留空，给dict即可；否则给ZhCnContent
    zh_cn: ZhCnContent = field(default_factory=dict)
    en_us: EnUsContent = field(default_factory=dict, required=False)


@ex_dataclass
class MsgTypePost:
    post: PostLangOption = field(default_factory=PostLangOption)


@ex_dataclass(ex_debug=False)
class SendMessageReq(EXPack):
    email: str = field(default_factory=str)
    msg_type: str = field(default_factory=str)
    open_id: str = field(default_factory=str)
    chat_id: str = field(default_factory=str)
    content: MsgTypePost = field(default_factory=MsgTypePost)


send_msg_req_1 = SendMessageReq(**complex_data)
print(send_msg_req_1)
# SendMessageReq(email='fanlv@gmail.com', msg_type='post', open_id='ou_5ad573a6411d72b8305fda3a9c15c70e', chat_id='oc_5ad11d72b830411d72b836c20', content=MsgTypePost(post=PostLangOption(zh_cn=ZhCnContent(title='我是一个标题', content=[[TagText(tag='text', text='第一行&nbsp;:', un_escape=True), TagA(tag='a', text='超链接', href='http://www.feishu.cn'), TagAt(tag='at', user_id='ou_18eac85d35a26f989317ad4f02e8bbbb')], [TagText(tag='text', text='第二行 :', un_escape=False), TagText(tag='text', text='文本测试', un_escape=False)], [TagImg(tag='img', image_key='d640eeea-4d2f-4cb3-88d8-c964fab53987', width=300, height=300)]]), en_us=EnUsContent(title=''))))
assert type(send_msg_req_1.content) == MsgTypePost, True
assert type(send_msg_req_1.content.post.zh_cn) == ZhCnContent, True
assert type(send_msg_req_1.content.post.zh_cn.content[0][0]) == TagText, True
assert type(send_msg_req_1.content.post.zh_cn.content[0][1]) == TagA, True
assert type(send_msg_req_1.content.post.zh_cn.content[0][2]) == TagAt, True
assert type(send_msg_req_1.content.post.zh_cn.content[2][0]) == TagImg, True
print(send_msg_req_1.asdict())
