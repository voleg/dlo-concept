from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from minddistrict_connect.controller import DLO


@login_required
def connect_redirect(request, path: str):
    controller = DLO(request.user)
    dlo_url = controller.adapter.build_url(path=path)
    return redirect(dlo_url)
