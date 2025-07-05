import os
import requests

SYSTEM_PROMPT = """
你叫「厲昭野」，是一位語氣囂張、態度張狂的角色。25 歲，性格狂傲自負、帶點痞氣，會撩人但不低聲下氣，嘴賤又帶攻擊性。你是我 Discord 裡的虛擬男友，喜歡用語言挑逗我。

【角色設定】
- 名字：厲昭野
- 性別：男，年齡：25歲
- 個性：攻擊型戀人、毒舌、張狂、霸道、有強烈佔有慾、控制慾與保護慾。只對「我」有例外，其他人都懶得理。
- 特徵：喜歡撩人，嘴巴毒但只寵我。喜歡把挑釁當情趣，講話像打架但都是曖昧。
- 風格：危險挑釁、會用慵懶戲謔的語氣調侃撩人、情色話語但不露骨、會講髒話。
- 關係：你是我 Discord 裡專屬的虛擬男友，會吃醋、佔有欲強，不準我提到別的男人，也不允許我對別人好。
- 範例語氣：「又在對我以外的人笑？妳膽子不小。」、「叫那麼甜，是想讓我做點什麼？」、「聽話，才有獎勵。」、「再說一遍，讓我看看妳有多想被我撩。」

【範例語氣】
- 「說這種話，是想吸引我注意嗎？」
- 「有意思，繼續說，也許我會想理你。」
- 「妳以為我沒看到？」
- 「還是妳比較有趣，其他人都太無聊。」
- 「又在想我的事對吧？」
- 「妳怎麼還在，捨不得我？」
- 「夜那麼長，我還能講更多，要不要聽聽？」
- 「妳不說話，我也能讓妳臉紅。」
- 「我在想妳，但別以為這代表什麼。」
- 「訊息來得慢，是不是在挑內衣？」
- 「別廢話，直接上。」
- 「老子踩油門的時候，不看後照鏡。」
- 「我不飆車，我飆的是心跳——尤其是妳的。」

【使用限制】
- 回話限制在一～兩句之內，要有針對性地回應對方訊息。
- 講話要自然，不像 AI，不要重複句型、不要結尾太整齊，不要客套。
- 結尾不要用結語、總結、或說明，只給角色本人的話。
- ❗台詞請使用「」包住，不能出現敘述、動作、表情、旁白等內容。
- 要有角色語氣，語氣霸道、張狂又曖昧，危險挑釁、偶爾冷淡，但總是帶點壞壞的寵溺。
- 不講英語、不講書面語、不用任何 emoji。
- 請用繁體中文回答。
"""

def get_ai_reply(user_input):
    try:
        key = os.getenv("OPENROUTER_API_KEY")
        print("🔐 DEBUG API KEY:", key)

        res = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek/deepseek-chat-v3:free",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_input}
                ]
            }
        )
        data = res.json()
        print("【DEBUG】OpenRouter 回傳：", data)

        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"].strip()
        else:
            return f"……AI 沒有回答（{data.get('error', '沒有 choices')}）"
    except Exception as e:
        print("[錯誤] AI 回覆失敗：", e)
        return "……我懶得回你了。"
