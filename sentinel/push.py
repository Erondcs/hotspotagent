#!/usr/bin/env python3
"""
sentinel push — 推送简报到 Lark 群
用法: python3 push.py <report.md 路径> "<卡片标题>"
SECRET 为空则不签名(当前机器人未开启签名校验)。返回码 0 = 成功(含一次重试)。
"""
import hmac, hashlib, base64, time, json, sys, urllib.request
from pathlib import Path

URL = "REPLACE_ME_WEBHOOK"  # 真实地址在云端容器与本地备份 zip 中,勿提交到公开仓库
SECRET = ""   # 机器人若开启签名校验,把密钥填这里

def send(text, title):
    card = {"config": {"wide_screen_mode": True},
            "header": {"template": "blue",
                       "title": {"tag": "plain_text", "content": title}},
            "elements": [{"tag": "markdown", "content": text}]}
    payload = {"msg_type": "interactive", "card": card}
    if SECRET:
        ts = str(int(time.time()))
        sign = base64.b64encode(hmac.new(f"{ts}\n{SECRET}".encode(), b"",
                                         hashlib.sha256).digest()).decode()
        payload.update({"timestamp": ts, "sign": sign})
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    resp = json.loads(urllib.request.urlopen(req, timeout=20).read().decode())
    if resp.get("code") != 0:
        raise RuntimeError(f"lark error: {resp}")
    return resp

if __name__ == "__main__":
    text = Path(sys.argv[1]).read_text()
    title = sys.argv[2] if len(sys.argv) > 2 else "📡 DCS 竞对雷达"
    for attempt in (1, 2):
        try:
            print(send(text, title))
            sys.exit(0)
        except Exception as e:
            print(f"attempt {attempt} failed: {e}", file=sys.stderr)
            time.sleep(3)
    sys.exit(1)
