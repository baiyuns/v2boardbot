from telegram import InlineKeyboardButton

start_keyboard_text = """
💰 我的钱包 - 回复 /wallet     
📃 流量查询 - 回复 /traffic
📒 我的订阅 - 回复 /sub
📅 签 到 - 回复 /checkin

"""

keyboard_admin_text = """
⚙ Bot设置 - 回复 /bot_settings 
🔄 重载配置 - 回复 /setting_reload
🎮 游戏设置 - 回复 /game_settings
✈ 机场管理 - 回复 /v2board_settings
"""

start_keyboard_admin_text = keyboard_admin_text + "\n" + start_keyboard_text

return_keyboard_text = "返回菜单 - 回复 /start_over"
