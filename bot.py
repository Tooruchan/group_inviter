#-*- coding:utf-8 -*-
# An test of inline keyboard markup
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os, json, time, random

if os.path.exists('./config.json'):
    if os.path.getsize('./config.json'):
        pass
    else:
        with open('./config.json', 'w') as write_default:
            default_config = dict(user=[0], token='')
            json.dump(default_config, write_default)
            write_default.close()
else:
    with open('./config.json', 'w') as users:
        default_config = dict(user=[0], token='')
        json.dump(default_config, users)
        users.close()

with open('./config.json', 'r+') as config_file:
    config = json.load(config_file)
    user_lists = config['user']
    token = config['token']

bot = telebot.TeleBot(token)
gen_group_link = bot.export_chat_invite_link(-1001254140605)
msg_page_id = 0


def into_group():
    global gen_group_link
    markup = InlineKeyboardMarkup()
    markup.row_width = 4
    markup.add(
        InlineKeyboardButton('1', callback_data=f'page1'),
        InlineKeyboardButton('2', callback_data=f'page2'),
        InlineKeyboardButton('3', callback_data=f'page3'),
        InlineKeyboardButton('·4·', callback_data=f'a'))
    markup.row_width = 1
    btn_1 = InlineKeyboardButton(
        '我确认我已读完但未理解上述内容', url='https://t.me/joinchat/c2ZzZnN2ZHZzZGZzZHZkc3Y')
    btn_2 = InlineKeyboardButton(
        '我确认我未读完但已理解上述内容',
        url='https://t.me/joinchat/5L2g5piv5LiA5Liq77yB5LiA5Lit')
    btn_3 = InlineKeyboardButton('我确认我已读完并已理解上述内容', url=gen_group_link)
    btn_4 = InlineKeyboardButton(
        '我确认我未读完也未理解上述内容', url='https://t.me/joinchat/5ZO877yB5ZO877yB5ZWK77y')
    markup.add(btn_1, btn_2, btn_3, btn_4)
    return markup


def intro_manual_page1():
    markup = InlineKeyboardMarkup()
    markup.row_width = 4
    markup.add(
        InlineKeyboardButton('·1·', callback_data=f'a'),
        InlineKeyboardButton('2', callback_data=f'page2'),
        InlineKeyboardButton('3', callback_data=f'page3'),
        InlineKeyboardButton('4', callback_data=f'page4'))
    return markup


def intro_manual_page2():
    markup = InlineKeyboardMarkup()
    markup.row_width = 4
    markup.add(
        InlineKeyboardButton('1', callback_data=f'page1'),
        InlineKeyboardButton('·2·', callback_data=f'a'),
        InlineKeyboardButton('3', callback_data=f'page3'),
        InlineKeyboardButton('4', callback_data=f'page4'))
    return markup


def intro_manual_page3():
    markup = InlineKeyboardMarkup()
    markup.row_width = 4
    markup.add(
        InlineKeyboardButton('1', callback_data=f'page1'),
        InlineKeyboardButton('2', callback_data=f'page2'),
        InlineKeyboardButton('·3·', callback_data=f'a'),
        InlineKeyboardButton('4', callback_data=f'page4'))
    return markup


def intro_inline():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton('投稿', url='https://t.me/tooru_post_bot'),
        InlineKeyboardButton('加群', callback_data=f'cb_add_group'))
    return markup

@bot.callback_query_handler(lambda q: q.data == 'a')
def callback_query(call):
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(lambda q: q.data == 'cb_add_group')
def callback_query(call):
    global user_lists, msg_page_id
    if call.from_user.id in user_lists:
        bot.answer_callback_query(call.id, '你已经执行过一遍入群的操作了。', show_alert=True)
    else:
        bot.answer_callback_query(call.id)
        msg_page_id = bot.send_message(
            call.from_user.id,
            """在加入群组之前，请先注意以下事项:
        1.群组为频道[托尔酱的新闻与吐槽](https://t.me/TooruchanNews)的投稿群组与频道主[Tooruchan](https://t.me/tooruchan)的个人群组，以讨论频道消息与投稿为主。
        2.请勿在群内表达自己的政治观点，**牢记我们是一个科技频道**或者是转发各种政治新闻与评论，频道主并不喜欢这种行为，这有可能会导致您被移出群组。
        """,
            reply_markup=intro_manual_page1(),
            parse_mode="markdown").message_id
        


@bot.callback_query_handler(lambda q:q.data == 'used_link')
def callback_query(call):
    bot.answer_callback_query(call.id)
    if call.from_user.id == 393621081:
        pass
    else:
        user_lists.append(call.from_user.id)
        with open('./config.json', 'w+') as write_config:
            now_config = dict(user=user_lists, token=token)
            json.dump(now_config, write_config)
            write_config.close()
@bot.callback_query_handler(lambda q: q.data == 'page1')
def change_page1(call):
    global msg_page_id
    bot.answer_callback_query(call.id)
    msg_page_id = bot.edit_message_text(
        "在加入群组之前，请先注意以下事项:\n1.群组为频道[托尔酱的新闻与吐槽](https://t.me/TooruchanNews)的投稿群组与频道主[Tooruchan](https://t.me/tooruchan)的个人群组，以讨论频道消息与投稿为主。\n2.请勿在群内表达自己的政治观点，**牢记我们是一个科技频道**或者是转发各种政治新闻与评论，频道主并不喜欢这种行为，这有可能会导致您被移出群组。",
        call.from_user.id,
        msg_page_id,
        reply_markup=intro_manual_page1(),
        parse_mode="markdown").message_id

@bot.callback_query_handler(lambda q: q.data == 'page2')
def change_page2(call):
    global msg_page_id
    bot.answer_callback_query(call.id)
    msg_page_id = bot.edit_message_text(
        "\n3.请勿在群内安插各种 userbot，我们会对各种没有 username 和没有头像的用户定时清理。\n4.为了防止 Spammer 对本群的骚扰，群内会放置[CNBlackListR](https://t.me/CNBlackListRBot)机器人，在进群之前，请确认自己有没有被封禁。",
        call.from_user.id,
        msg_page_id,
        reply_markup=intro_manual_page2(),
        parse_mode="markdown").message_id


@bot.callback_query_handler(lambda q: q.data == 'page3')
def change_page3(call):
    global msg_page_id
    bot.answer_callback_query(call.id)
    msg_page_id = bot.edit_message_text(
        "5.群主不喜欢六学/抽象等奇奇怪怪的亚文化，看见了可能会被滥权。\n6.请不要往群里拉各种各样的bot，我知道很多bot功能可能很有趣，但是过多的bot会对群员的交流造成不必要的困难。",
        call.from_user.id,
        msg_page_id,
        reply_markup=intro_manual_page3(),
        parse_mode="markdown").message_id


@bot.callback_query_handler(lambda q: q.data == 'page4')
def change_page4(call):
    global msg_page_id
    bot.answer_callback_query(call.id)
    msg_page_id = bot.edit_message_text(
        "7.不要使用群多多/币用/电报圈/蝴蝶IM等各种各样的所谓的免翻客户端加入本群！这个行为会导致群组成员陷入危险！\n8.我们不欢迎过度的鼓吹，友善交流是你能进入这个群的前提。\n**最后一点，请不要在群内撕逼！如果有人搞事，请看着他搞事，如果你要加入撕逼，撕逼的双方将会被管理员ban。**\n如果你阅读完了这些关于附属群组的说明，请按下面按钮中的一个加入群组。",
        call.from_user.id,
        msg_page_id,
        reply_markup=into_group(),
        parse_mode="markdown").message_id
    if call.from_user.id == 393621081:
        pass
    else:
        user_lists.append(call.from_user.id)
        with open('./config.json', 'w+') as write_config:
            now_config = dict(user=user_lists, token=token)
            json.dump(now_config, write_config)
            write_config.close()


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    if message.chat.type in ['group', 'channel', 'supergroup']:
        pass
    else:
        msg = bot.reply_to(
            message,
            "这个机器人是由 @tooruchan 制作的入群辅助机器人，需要入群或者投稿请按下面的按钮。",
            reply_markup=intro_inline())


@bot.message_handler(commands=['clear'])
def clean_users(message):
    global user_lists, gen_group_link
    if message.chat.id == 393621081:
        user_lists = [0]
        with open('./config.json', 'w+') as write_config:
            now_config = dict(user=[0], token=token)
            json.dump(now_config, write_config)
            write_config.close()
        bot.send_message(message.chat.id, '已清除所有入群用户的状态，并且清空了配置文件。')
    else:
        pass


@bot.message_handler(commands=['revoke'])
def revoke_links(message):
    global gen_group_link
    if message.chat.id == 393621081:
        gen_group_link = bot.export_chat_invite_link(-1001254140605)
        bot.send_message(message.chat.id,
                         '已revoke之前释放出的所有入群链接\n新的入群链接为:' + str(gen_group_link))
    else:
        pass


bot.polling(none_stop=True, timeout=114514)
