import io
from zipfile import ZipFile

import qrcode
from PIL import Image
from django.contrib import admin
from django.http import HttpResponse

from .models import Log, Restaurant, Table, Waiter


class ExportQrs:
    def export_qrs(self, request, queryset):
        tables = Table.objects.filter(rest=queryset[0]).all()
        io_images = []
        for table in tables:
            template = Image.open('static/template.png')
            qr = qrcode.QRCode(
                version=3,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=12,
                border=0,
            )
            qr.add_data(table.url)
            qr.make(fit=True)
            qr = qr.make_image(fill_color="black", back_color="white")
            template.paste(qr, (43, 24))
            result = io.BytesIO()
            template.save(result, 'PNG')
            template.close()
            qr.close()
            io_images.append([str(table.number), result])

        buffer = io.BytesIO()
        with ZipFile(buffer, 'w') as zip_file:
            for image in io_images:
                zip_file.writestr(image[0]+'.png', image[1].getvalue())
            zip_file.close()

        response = HttpResponse(buffer.getvalue())
        response['Content-Type'] = 'application/x-zip-compressed'
        response['Content-Disposition'] = f'attachment; filename={str(queryset[0].back_identif)}.zip'
        return response

    export_qrs.short_description = "Export QRs"


@admin.register(Waiter)
class WaiterAdmin(admin.ModelAdmin):
    list_display = ['name', 'rest', 'telegram_id', 'tables']


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin, ExportQrs):
    list_display = ['restaurant', 'back_identif', 'address', 'phone', 'name', 'vk', 'inst']
    actions = ["export_qrs"]


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['rest', 'number', 'waiter', 'url', 'qr']


admin.site.register(Log)
