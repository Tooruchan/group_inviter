#-*- coding:utf-8 -*-
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os,json

if os.path.exists('./config.json'):
    if os.path.getsize('./config.json'):
        pass
    else:
        with open('./config.json', 'w') as write_default:
            default_config = dict(user=[0], token='')
            json.dump(default_config, write_default)
            write_default.close()
else:
    with open('./config.json','w') as users:
            default_config = dict(user=[0], token='')
            json.dump(default_config, users)
            users.close()

with open('./config.json', 'r+') as config_file:
    config = json.load(config_file)
    user_lists = config['user']
    token = config['token']

bot = telebot.TeleBot(token)

def into_group():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    gen_group_link = bot.export_chat_invite_link(PLACE_YOUR_GROUP_ID)
    markup.add(InlineKeyboardButton('我确认我已读完但未理解上述内容',url = 'http://t.me/inlinekeytest_bot'),InlineKeyboardButton('我确认我未读完但已理解上述内容',url = 'http://t.me/inlinekeytest_bot'),InlineKeyboardButton('我确认我已读完并已理解上述内容',url = gen_group_link),InlineKeyboardButton('我确认我未读完也未理解上述内容',url = 'http://t.me/inlinekeytest_bot'))
    return markup

def intro_inline():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('投稿',url = 'https://t.me/tooru_post_bot'),InlineKeyboardButton('加群',callback_data = f'cb_add_group'))
    return markup

@bot.callback_query_handler(lambda q: q.data == 'cb_add_group')
def callback_query(call):
    global user_lists
    bot.answer_callback_query(call.id)
    if call.from_user.id in user_lists:
        bot.send_message(call.from_user.id,'你已经执行过一遍入群的操作了。')
    else:
        bot.send_message(call.from_user.id,'在加入群组之前，请先注意以下事项:\n1.群组为频道[托尔酱的新闻与吐槽](https://t.me/TooruchanNews)的投稿群组与频道主[Tooruchan](https://t.me/tooruchan)的个人群组，以讨论频道消息与投稿为主。2.请勿在群内表达自己的政治观点，或者是转发各种政治新闻与评论，频道主并不喜欢这种行为，这有可能会导致您被移出群组。\n3.请勿在群内安插各种 userbot，我们会对各种没有 username 和没有头像的用户定时清理。\n4.为了防止 Spammer 对本群的骚扰，群内会放置[CNBlackListR](https://t.me/CNBlackListRBot)和加群验证码机器人，在进群之前，请确认自己有没有被封禁。\n最后一点，请不要在群内撕逼！撕逼的双方将会被管理员移除+ban。\n如果你阅读完了这些关于附属群组的说明，请按下面按钮中的一个加入群组，邀请链接会在5分钟后失效',reply_markup=into_group(),parse_mode = "markdown")
        user_lists.append(call.from_user.id)
        with open('./config.json', 'w+') as write_config:
            now_config = dict(
                user=user_lists, token=token)
            json.dump(now_config, write_config)
            write_config.close()


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    if message.chat.type in ['group', 'channel', 'supergroup']:
        pass
    else:
        msg = bot.reply_to(message, "这个机器人是由 @tooruchan 制作的入群辅助机器人，需要入群或者投稿请按下面的按钮。",reply_markup=intro_inline())

bot.polling(none_stop=True,timeout=114514)
