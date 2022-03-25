import json
import typing
from ex_dataclass import ex_dataclass, asdict, field, EXpack

jdata = '''{
    "result": [
        {
            "id": "ec4872a31c85875ae6c27761bcdac354",
            "name": "tiyagroup.com",
            "status": "active",
            "paused": false,
            "type": "partial",
            "development_mode": 0,
            "verification_key": "761471371-457491622",
            "cname_suffix": "cdn.jcloudcdn.com",
            "original_name_servers": [
                "basin.dnspod.net",
                "boss.dnspod.net"
            ],
            "original_registrar": "alibaba cloud computing (beiji (id: 420)",
            "original_dnshost": null,
            "modified_on": "2021-09-16T06:26:56.466302Z",
            "created_on": "2021-09-16T06:26:19.016388Z",
            "activated_on": "2021-09-16T06:26:56.060749Z",
            "meta": {
                "step": 4,
                "custom_certificate_quota": 1,
                "page_rule_quota": 100,
                "phishing_detected": false,
                "multiple_railguns_allowed": false
            },
            "owner": {
                "id": "545b0cac4dc018f330b199b0a7d73709",
                "type": "organization",
                "name": "jcloud_DIPwvvf"
            },
            "account": {
                "id": "545b0cac4dc018f330b199b0a7d73709",
                "name": "jcloud_DIPwvvf"
            },
            "permissions": [
                "#access:edit",
                "#access:read",
                "#analytics:read",
                "#auditlogs:read",
                "#billing:edit",
                "#billing:read",
                "#cache_purge:edit",
                "#dns_records:edit",
                "#dns_records:read",
                "#lb:edit",
                "#lb:read",
                "#legal:read",
                "#logs:edit",
                "#logs:read",
                "#organization:read",
                "#ssl:edit",
                "#ssl:read",
                "#stream:edit",
                "#stream:read",
                "#subscription:edit",
                "#subscription:read",
                "#teams:edit",
                "#teams:pii",
                "#teams:read",
                "#teams:report",
                "#waf:edit",
                "#waf:read",
                "#worker:edit",
                "#worker:read",
                "#zone:read",
                "#zone_settings:edit",
                "#zone_settings:read"
            ],
            "plan": {
                "id": "94f3b7b768b0458b56d2cac4fe5ec0f9",
                "name": "Enterprise Website",
                "price": 0,
                "currency": "USD",
                "frequency": "",
                "is_subscribed": true,
                "can_subscribe": true,
                "legacy_id": "enterprise",
                "legacy_discount": false,
                "externally_managed": true
            }
        }
    ],
    "result_info": {
        "page": 1,
        "per_page": 20,
        "total_pages": 1,
        "count": 1,
        "total_count": 1
    },
    "success": true,
    "errors": [],
    "messages": []
}'''

ZoneStatus = str
ZoneType = str


@ex_dataclass
class CloudFlareZoneOwner:
    id: str = field(default="df9d0e15f9061a56892e388b88215033")  # ZoneID 根据接入根域不同决定
    type: str = field(default_factory=str)
    name: str = field(default_factory=str)


@ex_dataclass
class CloudFlareZoneResResult:
    id: str = field(default_factory=str)
    name: str = field(default_factory=str)
    status: ZoneStatus = field(default_factory=ZoneStatus)
    paused: bool = field(default_factory=bool)
    type: ZoneType = field(default_factory=ZoneType)
    owner: CloudFlareZoneOwner = field(default_factory=CloudFlareZoneOwner)


# 多个账号信息汇聚，以result列表呈现
@ex_dataclass
class CloudFlareZonesResInfo:
    result: typing.List[CloudFlareZoneResResult] = field(default_factory=list, required=True)
    # result_info: dict = field(default_factory=dict)
    success: bool = field(default_factory=bool)
    errors: list = field(default_factory=list)
    messages: list = field(default_factory=list)


d = CloudFlareZonesResInfo(**json.loads(jdata))
print(d)
print(asdict(d))

import datetime

# dict -> dataclass 类型；
def loads_f(v: str) -> datetime.datetime:
    if v == "":
        return datetime.datetime.now()


    return datetime.datetime.strptime(v, "%Y-%m-%d")


# dataclass类型 -> dict;
def asdict_f(v: datetime.datetime) -> str:
    return v.strftime("%Y-%m-%d")


@ex_dataclass
class Date(EXpack):
    created: datetime.datetime = field(default=None, loads_factory=loads_f, asdict_factory=asdict_f)

d = Date(**{"created": "2022-01-01"})
# Date(created=datetime.datetime(2022, 1, 1, 0, 0))
print(d)
# {'created': '2022-01-01'}
print(asdict(d))
assert isinstance(d.created, datetime.datetime), True
assert asdict(d)["created"] == "2022-01-01", True
