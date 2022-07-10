# See readme.md for instructions on running this code.
# https://zulip.com/api/writing-bots
from typing import Any, Dict

from zulip_bots.lib import BotHandler

import lib.data as data
import lib.utils as utils


class JarvisHandler:
    def usage(self) -> str:
        return
        "Jarvis Robot"

    def initialize(self, bot_handler: BotHandler) -> None:
        self.name = "Jarvis-Bot"
        self.bot_handler = bot_handler

        self.Invalid_Command_ERROR_MESSAGE = "**Invalid Command.**\n\n"\
               f"Please use `@**{self.name}** -h` or `@**{self.name}** --help` to see the correct usage."


    #-----------------------------Generate response-----------------------------
    def generate_response(self, commands) -> str:
        try:
            instruction = commands[0]
        except:
            return "Please type something.\n You can use `@**{self.name}** -h` or `@**{self.name}** --help` to get more info."
        # if instruction == "server":
        #     return data.get_cpolar(sender_email=self.message['sender_email'], server_id=commands[1])
        try:
            instruction = commands[0]
            # only instruction
            if instruction == "--help" or instruction == "-h":
                content = data.get_help(self.name)
                return content

            if "http" in instruction or "com" in instruction or "www" in instruction:
                assert len(commands)==1
                try:
                    return data.get_paper(commands[0])
                except:
                    return "URL must from arxiv or PapersWithCode or iccv or cvpr, "\
                    "or something wrong happeded during the crawl"
            # instruction params >=1
            try:
                if instruction == "--paper" or instruction == "-p":
                    assert len(commands)>=2
                    param = commands[1]
                    if "http" in param or "com" in param or "www" in param:
                        assert len(commands)==2 
                        try:
                            return data.get_paper(commands[1])
                        except:
                            return "URL must from arxiv or PapersWithCode or iccv or cvpr, "\
                        "or something wrong happeded during the crawl"

                    else:
                        try:
                            title = commands[1:]
                            title = ' '.join(title)
                            return data.get_paper(title, type=1)
                        except:
                            return "Something wrong happeded during the crawl. Please check the paper title, or no paper is found in PapersWithCode."
            except:
                return "Invalid Nums of Params for paper."
            # cpolar
            try:
                if instruction == "--server" or instruction == "-s":
                    assert len(commands)==2
                    try:
                        cmd_out_prompt = "Without ECNU VPN. Please use:\n"
                        cmd_vpn_prompt = "With ECNU VPN. Please use:\n"
                        cmd_out, cmd_vpn = data.get_cpolar(sender_email=self.message['sender_email'], server_id=commands[1])
                        return cmd_out_prompt + f"`{cmd_out}`\n\n" + cmd_vpn_prompt + f"`{cmd_vpn}`\n"
                    except:
                        return "server_id currently is 0, 1. \
                        Please choose right server_id or something wrong happened."
            except:
                return "Invalid Nums of Params for server."


        except:
            return  self.Invalid_Command_ERROR_MESSAGE

        return  self.Invalid_Command_ERROR_MESSAGE




    #-----------------------------Handle Message-----------------------------
    def handle_message(self, message: Dict[str, Any], bot_handler: BotHandler) -> None:
        # self.bot_handler = bot_handler
        self.message = message
        # print(message["content"])
        print(message)
        try:
            commands = utils.sep_cont(self.message["content"])
        except:
            content = self.Invalid_Command_ERROR_MESSAGE
            bot_handler.send_reply(message, content)
            return

        content = self.generate_response(commands)
        bot_handler.send_reply(message, content)

        return


handler_class = JarvisHandler
