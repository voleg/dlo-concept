from django.contrib.auth import get_user_model

from minddistrict_connect.dlo import DLOAdapter
from minddistrict_connect.models import PlatformConfig, PlatformProfile

User = get_user_model()


class DLO:
    adapter_class = DLOAdapter

    def __init__(self, user: User) -> None:
        self.user = user
        profile: PlatformProfile = self.user.platformprofile
        self.userid = profile.platform_user_id
        self.usertype = profile.platform_user_type
        self._build()

    def get_config(self):
        config: PlatformConfig = PlatformConfig.objects.first()
        if not config:
            raise ValueError('Improperly configured: Please provide base_url and shared_seret')

        if self.usertype == PlatformProfile.PlatformUserType.UNSPECIFIED or not self.userid:
            raise ValueError('Improperly configured: Please check third party userid and usertype')

        return {
            'base_url': config.base_url,
            'secret_key': config.secret_key,
            'usertype': self.usertype,
            'userid': self.userid,
        }

    def _build(self):
        self.adapter = self.adapter_class(**self.get_config())

    def get_resources(self):
        return self.adapter.discover_resources(str(self.usertype))
