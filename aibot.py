import re
import html
import openai
from maubot import Plugin, MessageEvent
from maubot.handlers import command
from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper

class Config(BaseProxyConfig):
  def do_update(self, helper: ConfigUpdateHelper) -> None:
    helper.copy("API_KEY")

class AIBot(Plugin):
    @classmethod
    def get_config_class(cls) -> type[BaseProxyConfig]:
        return Config
    async def start(self) -> None:
        self.config.load_and_update()
    
    MAX_INPUT_LENGTH = 1000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        openai.api_key = self.config["API_KEY"]
        self.conversations = {}

    @command.passive(regex=r".*")
    async def process_message(self, event: MessageEvent, _: str) -> None:
        # Check if the room has only 2 members or 3 members with one bot
        room_members = await self.get_joined_members(event.room_id)
        if len(room_members) == 2 or any(member.endswith("bot:beeper.local") for member in room_members):
            input_text = event.content["body"][:self.MAX_INPUT_LENGTH]
            response_text = self.chat_gpt_3_5(input_text, event.room_id)
            await event.reply(response_text)
        else:
            # Check if the bot is mentioned in the message
            mention_data = self.is_bot_mentioned(event)
            if mention_data:
                start, end, text = mention_data
                print(text)
                if "!clear" in text.lower():
                    self.conversations.pop(event.room_id, None)
                    await event.reply("Conversation history cleared.")
                else:
                    input_text = text[:self.MAX_INPUT_LENGTH]
                    if len(input_text) == self.MAX_INPUT_LENGTH:
                        await event.reply(f"Input text exceeds maximum length of {self.MAX_INPUT_LENGTH} characters.")
                        return
                    response_text = self.chat_gpt_3_5(input_text, event.room_id)
                    await event.reply(response_text)



    async def get_joined_members(self, room_id):
        room_members = []
        response = await self.client.get_joined_members(room_id)
        for user_id, member_info in response.items():
            room_members.append(user_id)
        return room_members

    def is_bot_mentioned(self, event: MessageEvent):
        formatted_body = event.content.get("formatted_body", "")
        print("formatted_body: ", formatted_body)
        mention_pattern = re.compile(rf"<a href=['\"]https://matrix\.to/#/{self.client.mxid}['\"]>")
        match = mention_pattern.search(formatted_body)
        if match:
            start, end = match.start(), match.end()
            text = formatted_body[end:]
            text = re.sub('<[^<]+?>', '', text)
            text = html.unescape(text).strip()
            return start, end, text
        return None

    def chat_gpt_3_5(self, text: str, room_id: str) -> str:
        try:
            if len(text) > self.MAX_INPUT_LENGTH:
                return f"Input text exceeds maximum length of {self.MAX_INPUT_LENGTH} characters."

            if room_id not in self.conversations: 
                self.conversations[room_id] = [{"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI. Carefully heed the user's instructions. Respond using Markdown."}]

            self.conversations[room_id].append({"role": "user", "content": text.strip()})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.conversations[room_id],
                max_tokens=200,
                n=1,
                stop=None,
                temperature=0.7,
            )
            assistant_message = response.choices[0].message["content"]
            self.conversations[room_id].append({"role": "assistant", "content": assistant_message})
            return assistant_message.strip()
        except Exception as e:
            self.log.error(f"Error in GPT-3.5-turbo API call: {e}")
            return "An error occurred while processing your request. Please check the logs for more information."
