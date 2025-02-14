# Psychological Coping Strategies Test Bot 🤖

A Telegram bot designed to assess users' coping strategies through an interactive psychological questionnaire. The bot provides personalized feedback on how individuals handle stressful situations and offers insights into their dominant coping mechanisms.

## Features 🌟

- **Interactive Questionnaire**: 33 carefully crafted questions to assess different coping strategies
- **Real-time Progress Tracking**: Visual progress bar shows test completion status
- **Personalized Results**: Detailed analysis of five coping strategies:
  - ◆ Avoidance Strategy
  - ★ Problem-Solving Strategy
  - ⚘ Positive Reframing Strategy
  - ♡ Emotion-Focused Strategy
  - ⚡ Support-Seeking Strategy
- **Administrative Tools**: Track user engagement and test completion statistics
- **Secure Data Handling**: Anonymized user data for privacy protection

## Technical Requirements 🛠️

- Python 3.8+
- python-telegram-bot library
- JSON for data storage
- Environment Variables:
  - `TELEGRAM_BOT_TOKEN`: Your Telegram Bot API token

## Installation and Setup 🚀

1. Clone the repository:
```bash
git clone [repository-url]
```

2. Install required packages:
```bash
pip install python-telegram-bot
```

3. Set up your environment variables:
```bash
export TELEGRAM_BOT_TOKEN='your_token_here'
```

4. Run the bot:
```bash
python3 bot.py
```

## Usage Guide 📱

### For Users
1. Find the bot on Telegram: @zoyaskobeltsyna_bot
2. Start the interaction with `/start` command
3. Follow the bot's instructions to complete the test
4. Receive personalized results and insights
5. Get additional materials through the provided CTA button

### For Administrators
1. Access admin features using `/admin` command
2. View statistics on user engagement and test completion
3. Monitor bot performance and user interaction

## Project Structure 📁

```
├── bot.py              # Main bot initialization and configuration
├── handlers.py         # Command and callback handlers
├── database.py         # Database operations and user session management
├── utils.py           # Utility functions for calculations and formatting
└── questions.json     # Test questions and strategy descriptions
```

## Features in Detail 🔍

### Test Structure
- 33 questions covering five coping strategies
- 5-point rating scale for each question:
  1. Almost never
  2. Rarely
  3. Sometimes
  4. Often
  5. Almost always

### Results Analysis
- Percentage calculation for each strategy
- Identification of dominant coping mechanism
- Personalized feedback based on user's responses
- Additional resources and recommendations

## Contributing 🤝

We welcome contributions to improve the bot! Please follow these steps:

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Contact Information 📬

- Author: Zoya Skobeltsyna
- Telegram: [@zoyaskobeltsyna](https://t.me/zoyaskobeltsyna)
- Channel: [@walktochange](https://t.me/walktochange)

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.
