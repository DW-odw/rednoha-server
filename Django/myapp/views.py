from django.conf import settings
from django.views import View
from django.http import JsonResponse, FileResponse
from django.core.files.storage import FileSystemStorage
import hashlib

from myapp.models import Gui, Fw

class get_latest_gui_ver(View):
    def get(self, request):
        latest_ver = Gui.objects.order_by('-version')[0]
        response = {
            'latest_ver' : latest_ver.version
        }
        return JsonResponse(response)

class download_gui_updater(View):
    def get(self, request):
        request_ver = request.GET.get('version', None)
        ver_info = Gui.objects.get(version=request_ver)
        file_path = ver_info.filepath
        fs = FileSystemStorage(settings.MEDIA_ROOT)
        response = FileResponse(fs.open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename={file_path}'        
        return response

class get_gui_using_fw_ver(View):
    def get(self, request):
        gui_ver = request.GET.get('version', None)
        ver_info = Gui.objects.get(version=gui_ver)
        response = {
            'fw_ver' : ver_info.fw_version.version,
        }
        return JsonResponse(response)

class download_fw(View):
    def get(self, request):
        request_ver = request.GET.get('version', None)
        ver_info = Fw.objects.get(version=request_ver)
        file_path = ver_info.filepath
        fs = FileSystemStorage(settings.MEDIA_ROOT)
        f = fs.open(file_path, 'rb')
        hash_data = f.read()
        hash_digest = hashlib.sha256(hash_data).hexdigest()
        f.seek(0)
        response = FileResponse(f)
        response['Content-Disposition'] = f'attachment; filename={file_path}'
        response['Digest'] = 'sha-256=' + hash_digest
        return response
