import json
import os
import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)
LOG_FILE_PATH = '/mnt/extra-addons/estate_sample/inquiries.txt'

class EstateAPI(http.Controller):
    @http.route('/api/estate/inquiry', type='json', auth='public', methods=['POST'], csrf=False)
    def receive_inquiry(self, **post):
        try:
            # محاولة سحب البيانات بأكثر من طريقة لضمان عدم حدوث الخطأ
            if hasattr(request, 'jsonrequest'):
                data = request.jsonrequest.get('params', {})
            else:
                # لو أودو مشايف الـ jsonrequest بنسحبها من الـ Data الخام
                raw_data = request.httprequest.data.decode('utf-8')
                data = json.loads(raw_data).get('params', {})

            if not data:
                return {'status': 'error', 'message': 'No data received'}

            # تجهيز نص الملاحظات
            log_entry = (
                f"--- New Inquiry ---\n"
                f"Name: {data.get('client_name')}\n"
                f"Phone: {data.get('client_phone')}\n"
                f"Address: {data.get('address')}\n"
                f"Property: {data.get('property_name')}\n"
                f"Price: {data.get('price')}\n"
                f"URL: {data.get('url')}\n"
                f"-------------------\n"
            )

            # 1. الكتابة في الملف النصي
            with open(LOG_FILE_PATH, 'a', encoding='utf-8') as f:
                f.write(log_entry)

            # 2. إنشاء Lead في الـ CRM (اختياري)
            request.env['crm.lead'].sudo().create({
                'name': f"طلب من الموقع: {data.get('property_name')}",
                'contact_name': data.get('client_name'),
                'phone': data.get('client_phone'),
                'description': log_entry,
            })

            return {'status': 'success'}

        except Exception as e:
            _logger.error(f"Inquiry API Error: {str(e)}")
            return {'status': 'error', 'message': str(e)}