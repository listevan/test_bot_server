import json
import os

import lark_oapi as lark
from lark_oapi.api.im.v1 import *

if __name__ == "__main__":
    main()
# SDK 使用说明: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/server-side-sdk/python--sdk/preparations-before-development
# 以下示例代码默认根据文档示例值填充，如果存在代码问题，请在 API 调试台填上相关必要参数后再复制代码使用
# 复制该 Demo 后, 需要将 "YOUR_APP_ID", "YOUR_APP_SECRET" 替换为自己应用的 APP_ID, APP_SECRET.
def get_message_value(your_app_id: str, your_app_secret: str):
    # 创建client
    client = lark.Client.builder() \
        .app_id(your_app_id) \
        .app_secret(your_app_secret) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    request: GetMessageRequest = GetMessageRequest.builder() \
        .message_id("om_dc13264520392913993dd051dba21dcf") \
        .user_id_type("open_id") \
        .build()

    # 发起请求
    response: GetMessageResponse = client.im.v1.message.get(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.im.v1.message.get failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))

if __name__ == "__main__":
    get_message_value(os.environ["YOUR_APP_ID"], os.environ["YOUR_APP_SECRET"])



