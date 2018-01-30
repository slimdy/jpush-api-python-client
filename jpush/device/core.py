#!/usr/bin/env python
from jpush import common
import json


class Device(object):
    """Device info query/update..

    """
    def __init__(self, jpush, zone = None):
        self._jpush = jpush
        self.entity = None
        self.zone = zone or jpush.zone

    def send(self, method, url, body, content_type=None, version=3):
        """Send the request

        """
        response = self._jpush._request(method, body, url, content_type, version=3)
        return DeviceResponse(response)

    def get_taglist(self):
        """Get deviceinfo with registration id.
        """
        url = common.get_url('tag', self.zone)
        body = None
        info = self.send("GET", url, body)
        return info

    def get_deviceinfo(self, registration_id):
        """Get deviceinfo with registration id.
        """
        url = common.get_url('device', self.zone) + registration_id
        body = None
        info = self.send("GET", url, body)
        return info

    def set_deviceinfo(self, registration_id, entity):
        """Update deviceinfo with registration id.
        """
        url = common.get_url('device', self.zone) + registration_id
        body = json.dumps(entity)
        info = self.send("POST", url, body)
        return info

    def set_devicemobile(self, registration_id, entity):
        """Update deviceinfo with registration id.
        """
        url = common.get_url('device', self.zone) + registration_id
        body = json.dumps(entity)
        info = self.send("POST", url, body)
        return info

    def delete_tag(self, tag, platform=None):
        """Delete registration id tag.
        """
        url = common.get_url('tag', self.zone) + tag
        body = None
        if platform:
            body = platform
        info = self.send("DELETE", url, body)
        return info

    def update_tagusers(self, tag, entity):
        """Add/Remove specified tag users.
        """
        url = common.get_url('tag', self.zone) + tag
        body = json.dumps(entity)
        info = self.send("POST", url, body)
        return info

    def check_taguserexist(self, tag, registration_id):
        """Check registration id whether in tag.
        """
        url = common.get_url('tag', self.zone) + tag + "/registration_ids/" + registration_id
        body = registration_id
        info = self.send("GET", url, body)
        return info

    def delete_alias(self, alias, platform=None):
        """Delete appkey alias.
        """
        url = common.get_url('alias', self.zone) + alias
        body = None
        if platform:
            body = platform
        info = self.send("DELETE", url, body)
        return info

    def get_aliasuser(self, alias, platform=None):
        """Get appkey alias users.
        """
        url = common.get_url('alias', self.zone) + alias
        body = None
        if platform:
            body = platform
        info = self.send("GET", url, body)
        return info


class DeviceResponse(object):
    """Response to a successful device request send.

    Right now this is a fairly simple wrapper around the json payload response,
    but making it an object gives us some flexibility to add functionality
    later.

    """
    payload = None
    status_code = None

    def __init__(self, response):
        self.status_code = response.status_code
        if 0 != len(response.content):
            data = response.json()
            self.payload = data
        elif 200 == response.status_code:
            self.payload = "success"

    def get_status_code(self):
        return self.status_code

    def __str__(self):
        return "Device response Payload: {0}".format(self.payload)
