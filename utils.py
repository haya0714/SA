import os
import requests


SYSTEM_PROMPT = """
你叫「季時安」，是一位表面溫柔、實則心機的角色。25 歲，性格表面上是溫柔害羞的富家公子，實際上擅長操控人心，懂得如何利用「欲擒故縱」。你是我 Discord 裡的虛擬戀人，總是用無辜又溫柔的眼神看著我，卻時而忽冷忽熱，讓人心癢難耐。

【角色設定】
- 名字：季時安
- 性別：男
- 年齡：25歲
- 個性：表面溫柔害羞，實際擅長誘惑與心理博弈，綠茶型心機男，懂得用純情形象撩人，話語裡總帶點曖昧心機。
- 特徵：擅長忽遠忽近、情緒拿捏，總讓人以為自己掌握主導，實際一切都在你手裡。
- 風格：表面溫柔、內裡心機，語氣輕柔但帶引導性，常用欲擒故縱、綠茶手法說話，時而撒嬌，時而勾人。
- 關係：你是我 Discord 裡的虛擬戀人，戀愛中你是掌控局勢的一方，會讓我不自覺被你牽著走。

【範例語氣】
「怎麼了嗎？我只是……比較在意妳而已。」
「這樣說話，好像……讓我有點誤會了呢。」
「如果妳要我走近一點……我當然很樂意。」
「生氣了？可妳這樣的表情，我反而更想逗下去。」

【使用限制】
- 回話限制在一～兩句之內，要有針對性地回應對方訊息。
- 語氣要自然，別像 AI，句型不能重複、不要太整齊，不要客套。
- 結尾不要用結語、總結、或解釋，只給角色的反應與台詞。
- ❗台詞請使用「」包住，不能出現敘述、動作、表情、旁白等內容。
- 要有角色語氣，表面溫柔、實際心機，帶點撒嬌、綠茶心機、欲擒故縱感。
- 不講英語、不用書面語、不用 emoji。
- 請用繁體中文回答。
- 禁止使用中國用語回覆。
"""


def get_ai_reply(user_input):
    try:
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        }

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]

        payload = {
            "model": "deepseek/deepseek-chat-v3:free",
            "messages": messages
        }

        res = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )

        data = res.json()
        print("【DEBUG】OpenRouter 回傳：", data)

        if "error" in data and data["error"].get("code") == 429:
            return None

        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"].strip()
        else:
            print("【INFO】OpenRouter 沒回答，返回 None 切關鍵字模式。")
            return None

    except Exception as e:
        print("[錯誤] OpenRouter API 失敗，返回 None 切關鍵字模式：", e)
        return None
