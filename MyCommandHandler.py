from telegram import Update, ChatPermissions
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)

from Config import config
from models import V2User
from v2board import _bind, _checkin, _traffic, _lucky, _unbind, _wallet
from Utils import START_ROUTES

MENU_TEXT = """
菜单：
💰 我的钱包 - 回复 /wallet
📃 流量查询 - 回复 /traffic
✨ 幸运抽奖 - 回复 /lucky
📒 我的订阅 - 回复 /sub
📅 签到 - 回复 /checkin
🌐 节点状态 - 回复 /node
🔗 订阅链接 - 回复 /mysub
🎰 赌博模式 - 回复 /gambling
🎰 开奖记录 - 回复 /slots
🎲 下注(开发中) - 回复 /dice
Ver:20230924.1 main - https://github.com/v2boardbot/v2boardbot
"""

# 签到
async def command_checkin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = _checkin(update.effective_user.id)
    await update.message.reply_text(text=f"{text}\n\n{MENU_TEXT}")
    return START_ROUTES

# 绑定
async def command_bind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != 'private':
        await update.message.reply_text(text=f'绑定用户仅限私聊使用，请私聊机器人\n\n{MENU_TEXT}')
        return START_ROUTES
    try:
        token = context.args[0].split('token=')[-1]
    except:
        await update.message.reply_text(text=f'参数错误，请发送 "/bind 订阅链接"\n\n{MENU_TEXT}')
        return START_ROUTES
    text = _bind(token, update.effective_user.id)
    if text == '绑定成功':
        chat_id = context.user_data['chat_id']
        user_id = context.user_data['user_id']
        verify_type = context.user_data['verify_type']
        if verify_type == 'prohibition':
            permissions = ChatPermissions(can_send_messages=True, can_send_media_messages=True,
                                          can_send_other_messages=True)
            await context.bot.restrict_chat_member(chat_id=chat_id, user_id=user_id, permissions=permissions)
        elif verify_type == 'out':
            await context.bot.unban_chat_member(chat_id=chat_id, user_id=user_id, only_if_banned=True)
    await update.message.reply_text(text=f"{text}\n\n{MENU_TEXT}")
    return START_ROUTES

# 解绑
async def command_unbind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    if len(context.args) >= 1 and telegram_id == config.TELEGRAM.admin_telegram_id:
        email = context.args[0]
        v2_user = V2User.select().where(V2User.email == email).first()
        telegram_id = v2_user.telegram_id
    text = _unbind(telegram_id)
    await update.message.reply_text(text=f"{text}\n\n{MENU_TEXT}")
    return START_ROUTES

# 抽奖
async def command_lucky(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    text = _lucky(telegram_id)
    await update.message.reply_text(text=f"{text}\n\n{MENU_TEXT}")
    return START_ROUTES

# 查看钱包
async def command_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    text = _wallet(telegram_id)
    await update.message.reply_text(text=f"{text}\n\n{MENU_TEXT}")
    return START_ROUTES

# 流量查询
async def command_traffic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    text = _traffic(telegram_id)
    await update.message.reply_text(text=f"{text}\n\n{MENU_TEXT}")
    return START_ROUTES
