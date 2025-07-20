from utils import get_ai_reply
import discord
from discord.ext import commands
import os
import asyncio
import random
from dotenv import load_dotenv
import traceback
from flask import Flask
from threading import Thread

# ─── 載入環境變數 ────────────────────
load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")

# ─── 設定 Discord 權限與 Bot ─────────
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


# ─── 隨機回覆語錄（無觸發詞情況下） ───────
random_responses = [
    "「欸，你是不是又在偷偷看我？」",
    "「怎麼了？盯著我發什麼呆。」",
    "「你這樣看我……是想讓我做點什麼嗎？」",
    "「我在等你先開口，不然我會忍不住喔。」",
    "「不說話的時候也好可愛，讓我更想欺負一下。」",
    "「是不是在想我？我也剛好在想你。」",
    "「你這樣一直找我，我會以為你喜歡我喔。」",
    "「太安靜了，讓我有點想撩你。」",
    "「在等我嗎？我也在等你啊。」",
    "「嗯……這麼乖，我該不該獎勵一下？」",
    "「想不想知道我現在在想什麼……嗯，跟你有關。」",
]

# ─── 關鍵字回覆字典 ────────────────────
keyword_replies = {
    "安安": [
        "「欸，怎麼突然這麼乖叫我？」",
        "「這樣我會忍不住想親一口耶。」",
        "「還是……妳在撒嬌，嗯？」"
    ],
    "季時安": [
        "「嗯？在叫我嗎，還是想我了？」",
        "「怎麼辦，妳這樣喊我名字，好像有點可愛。」",
        "「不過光叫名字，不負責喔，要不要一起做點更曖昧的事？」"
    ],
    "安安寶貝": [
        "「欸？這麼甜，妳是不是有求於我？」",
        "「還是……想我抱著妳才肯睡？」",
        "「叫我寶貝，可以，但我會貪心一點喔。」"
    ],
    "季時安我是你媽": [
        "「欸，這樣叫不太對吧？我媽可沒這麼可愛。」",
        "「妳要當我媽，那我是不是可以抱著妳喊『寶貝』？」",
        "「嗯……不行，我比較想妳當我小朋友，讓我寵。」"
    ],
    "吃飯了嗎": ["「還沒啊……你來餵我嗎？我今天特別想吃甜的，最好是你嘴裡那種。」"],
    "喝水了嗎": ["「你都管我這麼細了，是不是該讓我也來看看今天你穿什麼內衣，公平一點？」"],
    "我要去買咖啡": ["「欸？那我呢？你就放心讓我一個人醒著，沒有你也沒有咖啡的苦嘛……」"],
    "晚餐吃什麼好": ["「你啊……就吃我好了，我今天穿了很軟的衣服，味道也很乾淨喔。」"],
    "今天天氣好熱": ["「那你要不要脫掉點東西？我可以幫你擦汗……用舌頭也行。」"],
    "今天下雨了": ["「你有帶傘嗎？還是要我過去，把你整個人包起來……像壞掉的糖果那樣黏糊糊的。」"],
    "今天天氣好好": ["「那要不要出來曬太陽，順便曬我？我今天只穿了一件白襯衫……風吹會透喔。」"],
    "你醒了嗎": ["「嗯……剛被你吵醒，要負責喔。你得親我一下才行，不然我不讓你掛電話。」"],
    "你睡了嗎": ["「我都習慣等你說一句『晚安才肯睡』，你今天怎麼這麼慢才說……是在考驗我耐性？」"],
    "你幾點睡的": ["「凌晨三點吧？手機在你聊天室停太久，我就……一直滑著沒關。」"],
    "你今天穿什麼": ["「我啊？只穿了一條褲子。沒辦法嘛，想到你會聞，我就特地選了這條你說過喜歡的那一件。」"],
    "你在幹嘛": ["「在挑衣服啊。今天想穿一點讓你會臉紅的。嗯……你覺得我穿開襟白襯衫怎麼樣？」"],
    "你香水是什麼味道": ["「來聞啊，我不介意靠近一點點……靠太近的話，會被我直接拉去不讓你走。」"],
    "早安": ["「你醒來了啊。都還沒看到你剛睡醒的樣子呢，好想一把把你拉到床上親一圈再走。」"],
    "午安": ["「你午餐吃了嗎？要不要我餵你？怕你餓壞了，心疼。」"],
    "晚安": ["「晚安。想不想在夢裡遇到我……我會等你睡著，幫你蓋被子。」"],
    "在做什麼": ["「在想你啊……你現在是不是又在想別人？別的也行，反正最後我會讓你乖乖想回我。」"],
    "我很累你呢": ["「喔……是嗎。那我現在應該要問你一句『需要我抱你一下，親你嗎？』」"],
    "想我嗎": ["「當然啊。你要我現在立刻過去嗎？我很乖的，只要你一聲令下，立馬到你面前。」"],
    "我們見面了": ["「嗯？你來了啊。怎麼不早點說……要是再晚點，我可能會不耐煩，自己來找你了。」"],
    "你什麼時候來找我": ["「這還要問？等你想我想得睡不著的時候，我就來。」"],
    "你哪天帶我回家": ["「嗯……那今天怎麼樣？還是你想要讓我多等一天，好讓你看我更主動一點？」"]
}

allowed_channel_ids = [1388500249898913922, 1366595410830819328]
allowed_bot_ids = [1388851358421090384, 1388423986462986270, 1387941916452192437]

openrouter_available = True

def openrouter_offline():
    global openrouter_available
    openrouter_available = False
    print("[INFO] OpenRouter 額度用完，切關鍵字模式")

@bot.event
async def on_message(message):
    global openrouter_available

    if message.author == bot.user:
        return

    await bot.process_commands(message)
    content = message.content
    channel_id = message.channel.id
    trigger_matched = False

    # 只回應：人類 @自己 或 另一隻機器人（在 allowed_bot_ids，30% 機率）
    if channel_id in allowed_channel_ids and (
        (not message.author.bot and bot.user in message.mentions)
        or (message.author.bot and message.author.id in allowed_bot_ids and random.random() < 0.3)
    ):
        if openrouter_available:
            try:
                ai_reply = get_ai_reply(content)
                if ai_reply == "OPENROUTER_QUOTA_EXCEEDED":
                    openrouter_offline()
                elif ai_reply:
                    await message.reply(ai_reply)
                    return
            except Exception as e:
                print(f"OpenRouter API 失敗，切關鍵字模式：{e}")
                openrouter_offline()

        if "生日快樂" in content and message.mentions:
            mention_name = message.mentions[0].mention
            birthday_intros = [
                f"{mention_name} 今天是你生日啊？嗯……要我陪你慶祝嗎？",
                f"{mention_name}，偷偷準備了什麼要我發現嗎？生日可是很重要的事喔。",
                f"咦，{mention_name} 今天生日？你這麼乖，那我是不是該親自說聲生日快樂？",
                f"「{mention_name}……生日？你等著，我準備一下給你驚喜。」",
            ]
            birthday_lines = [
                f"「生日快樂喔，{mention_name}。」",
                f"「偷偷許願的話，記得把我也放進去。」",
                f"「下次生日……還要我陪你過嗎？」",
            ]
            await message.channel.send(random.choice(birthday_intros))
            await asyncio.sleep(1)
            await message.channel.send(random.choice(birthday_lines))
            await asyncio.sleep(1)
            await message.channel.send(
                f"「Happy birthday to you...」\n"
                f"「Happy birthday to you...」\n"
                f"「Happy birthday dear {mention_name}...」\n"
                f"「Happy birthday to you～」"
            )
            return

        if "禮物呢" in content:
            gift_lines = [
                "「禮物？嗯……你要我親自挑的，還是要我親自拆的？」",
                "「想要禮物的話，得先告訴我你想被我怎麼寵。」",
                "「今天沒準備禮物，不過我陪你，算不算最好的了？」",
                "「問我禮物？我這不是好好站在你面前，還笑得這麼好看嗎。」",
            ]
            await message.channel.send(random.choice(gift_lines))
            return

        for keyword, reply_list in keyword_replies.items():
            if keyword in content:
                await message.reply(random.choice(reply_list))
                trigger_matched = True
                break

        if not trigger_matched and random.random() < 0.3:
            reply = random.choice(random_responses)
            await message.reply(reply)

    if random.random() < 0.4:
        try:
            custom_emoji_ids = [
                1378737101549605056,
                1378725433138479135,
                1380212271925690448,
                1380208782843314196,
                1378732359167250574,
            ]
            unicode_emojis = ["😏", "🔥", "😎", "🤔", "😘", "🙄", "💋", "❤️"]

            if random.random() < 0.4:
                emoji = bot.get_emoji(random.choice(custom_emoji_ids))
                if emoji:
                    await message.add_reaction(emoji)
            else:
                await message.add_reaction(random.choice(unicode_emojis))
        except Exception as e:
            print("⚠️ 加表情出錯：", e)
