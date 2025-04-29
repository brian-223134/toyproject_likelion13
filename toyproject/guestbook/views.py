from django.shortcuts import render
from django.http import JsonResponse 
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.decorators.http import require_http_methods
from .models import *
import json


@require_http_methods(["GET", "POST"])
def guestbook_view(request):
    if request.method == "GET":
        entries = GuestbookStructure.objects.all().order_by('-created')

        entries_all = []

        for data in entries:
            data_json = {
                "id" : data.id,
                "title" : data.title,
                "author" : data.author,
                "body" : data.body
            }

            entries_all.append(data_json)
        
        return JsonResponse(entries_all, safe = False)

    if request.method == "POST":
        try:
            request_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "올바르지 않은 JSON 형식입니다."}, status=400)
        
        title = request_data.get('title')
        author = request_data.get('author')
        content = request_data.get('body') # 명명이 헷갈릴 것 같아 이렇게 정의함
        password = request_data.get('password')

        if not (title and author and content and password):
            return JsonResponse({"error": "모든 내용을 작성해야 합니다."}, status=400)

        entry = GuestbookStructure.objects.create(
            title = title,
            author = author,
            body = content,
            password = password
        )

        return JsonResponse({"message" : "Guestbook이 생성되었습니다.", "id": entry.id}, status=201)
    
@require_http_methods(["DELETE"])
def guestbook_delete(request, pk): # id를 받아오자
    try:
        entry = GuestbookStructure.objects.get(pk=pk) # [pk = 인자로 들어온 pk]과 같은 형식으로 변함
    except GuestbookStructure.DoesNotExist:
        return JsonResponse({"error": "존재하지 않는 방명록입니다."}, status=404)
    
    try:
        content = json.loads(request.body)
    except:
        return JsonResponse({"error": "올바르지 않은 JSON 형식입니다."}, status=400)
    
    password = content.get('password').strip() # db에서 비번 가져오기
    db_password = entry.password.strip()
    
    if not password:
        return JsonResponse({"error": "password를 작성해주세요."}, status=400)
    
    if password != db_password:
        return JsonResponse({"error": "잘못된 password입니다."}, status=403)
    
    entry.delete()
    return JsonResponse({"message": "방명록이 삭제되었습니다."}, status=204)

