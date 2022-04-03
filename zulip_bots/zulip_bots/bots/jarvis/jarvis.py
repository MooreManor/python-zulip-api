# See readme.md for instructions on running this code.
# https://zulip.com/api/writing-bots
from typing import Any, Dict

from zulip_bots.lib import BotHandler

import lib.data as data
import lib.utils as utils


class GearHandler:
    def usage(self) -> str:
        return
        "Jarvis Robot"
    
    def initialize(self, bot_handler: BotHandler) -> None:
        self.name = "Jarvis-Bot"
        self.bot_handler = bot_handler

        self.Invalid_Command_ERROR_MESSAGE = "**Invalid Command.**\n\n"\
               f"Please use `@**{self.name}** help` to see the correct usage."  


    #-----------------------------Generate response----------------------------- 
    def generate_response(self, commands) -> str:
        try:
            instruction = commands[0]
            # only instruction
            if instruction == "help":
                content = data.get_help(self.name)
                return content

            # instruction params >=1
            try:
                if instruction == "paper":
                    assert len(commands)==2
                    try:
                        return data.get_paper(commands[1])
                    except:
                        return "URL must from arxiv or PapersWithCode, "\
                      "or something wrong happeded during the crawl" 
            except:
                return "Invalid Nums of Params for paper."
        except:
            return  self.Invalid_Command_ERROR_MESSAGE

        return  self.Invalid_Command_ERROR_MESSAGE

        


    #-----------------------------Handle Message----------------------------- 
    def handle_message(self, message: Dict[str, Any], bot_handler: BotHandler) -> None:
        # self.bot_handler = bot_handler
        self.message = message
        # print(message["content"])
        try:
            commands = utils.sep_cont(self.message["content"])
        except:
            content = self.Invalid_Command_ERROR_MESSAGE           
            bot_handler.send_reply(message, content)
            return
        
        content = self.generate_response(commands)
        bot_handler.send_reply(message, content)
    
        return


handler_class = GearHandler
