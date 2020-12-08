from aiohttp.web import Request

from opsdroid.skill import Skill
from opsdroid.matchers import match_webhook
from opsdroid.events import Message

import logging
import pprint

_LOGGER = logging.getLogger(__name__)



class EventManager(Skill):
    @match_webhook('webhook')
    async def eventmanager(self, event: Request):
        payload = await event.json()
        _LOGGER.debug('payload received by eventmanager: ' +
                      pprint.pformat(payload))

        for alert in payload["alerts"]:
            if alert["status"].upper() == "RESOLVED":
                continue
            msg = ""
            if "message" in alert["annotations"]:
                msg = alert["annotations"]["message"]
            elif "description" in alert["annotations"]:
                msg = alert["annotations"]["description"]
            await self.opsdroid.send(Message(str(
                "{severity} {name}: {message}".format(
                    name=alert["labels"]["alertname"],
                    severity=alert["labels"]["severity"].upper(),
                    message=msg)
                ))
            )