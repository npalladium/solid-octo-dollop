import logging
from subprocess import check_output
from typing import Optional

import gradio as gr
import jc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

COMMANDS = [
    "arp",
    "cksum",
    "date",
    "df",
    "dig",
    "du",
    "env",
    "file",
    "finger",
    "gpg",
    "hash",
    "id",
    "ifconfig",
    "jobs",
    "last",
    "lsof",
    "mount",
    "netstat",
    "passwd",
    "postconf",
    "ps",
    "route",
    "time",
    "traceroute",
    "uname",
    "uptime",
    "w",
    "wc",
    "who",
    "zipinfo",
]


def run(cmd: str, arguments: Optional[str] = None):
    full_cmd = [cmd] + (arguments.split() if arguments is not None else [])
    logger.info(f"Running {full_cmd}")
    try:
        cmd_output = check_output(full_cmd, text=True)
        data, error = jc.parse(cmd, cmd_output), ""
    except Exception as e:
        data, error = None, str(e)
        logger.exception(repr(e))
    finally:
        return data, error


def main():
    app = gr.Interface(
        fn=run,
        inputs=[
            gr.Dropdown(choices=COMMANDS, label="Command"),
            gr.Textbox(label="Additional Arguments"),
        ],
        outputs=[
            gr.JSON(label="Command Output"),
            gr.Textbox(label="Error"),
        ],
    )
    app.launch(server_port=7860)


if __name__ == "__main__":
    main()
