import os
import re
import cloudscraper

class ChatGptEs:
    def __init__(self):
        self.url = "https://chatgpt.es"
        self.api_endpoint = "https://chatgpt.es/wp-admin/admin-ajax.php"
        self.scraper = cloudscraper.create_scraper()  # Bypasses Cloudflare

    def ask_question(self, message: str) -> str:
        """Sends a question to chatgpt.es and returns the response."""
        page_text = self.scraper.get(self.url).text

        # Extract nonce and post_id
        nonce_match = re.search(r'data-nonce="(.+?)"', page_text)
        post_id_match = re.search(r'data-post-id="(.+?)"', page_text)

        if not nonce_match or not post_id_match:
            return "[ERROR] Failed to fetch necessary tokens."

        payload = {
            'check_51710191': '1',
            '_wpnonce': nonce_match.group(1),
            'post_id': post_id_match.group(1),
            'url': self.url,
            'action': 'wpaicg_chat_shortcode_message',
            'message': message,
            'bot_id': '0',
            'chatbot_identity': 'shortcode',
            'wpaicg_chat_client_id': os.urandom(5).hex(),
            'wpaicg_chat_history': None
        }

        response = self.scraper.post(self.api_endpoint, data=payload).json()
        return response.get('data', '[ERROR] No response received.')

# Run the chatbot
chatbot = ChatGptEs()
response = chatbot.ask_question("Hey, who are you?")
print("Response:", response)