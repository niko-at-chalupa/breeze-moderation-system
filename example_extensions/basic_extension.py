# Copy to plugins/breeze/extensions/ folder!

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from extensions import BreezeExtensionAPI #type: ignore

# on_load runs when Breeze loads your plugin 
def on_load(bea: 'BreezeExtensionAPI'):
    bea.logger.info("Basic extension loaded!!")

    # note: this method can be renamed or placed whatever you want, as long as it's registered as a listener
    def on_chat_processed(event, handler_output: "BreezeExtensionAPI.HandlerOutput", is_bad, plugin):
        if is_bad:
            plugin.logger.info(f"[OutwardsChatRelay] player {event.player.name} sent a censored message: {handler_output['finished_message']}")
    
    # register event as a listener
    bea.eventbus.on("on_breeze_chat_processed", on_chat_processed)
