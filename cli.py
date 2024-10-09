from typing import Literal

import fire
from core import DLOAdapter


def build_dlo_url(
    *,
    shared_secret: str,
    base_url: str,
    user_type: Literal["client", "careprovider"],
    user_id: str,
    redirect_url: str = None,
):
    adapter = DLOAdapter(
        secret_key=shared_secret,
        base_url=base_url,
        userid=user_id,
        usertype=user_type,
    )

    return adapter.build_url(redirect=redirect_url)


if __name__ == "__main__":
    fire.Fire(build_dlo_url)
