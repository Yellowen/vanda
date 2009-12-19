from django.shortcuts import render_to_response as rr


def show (request):
    return rr ('test/brainstorm.html')


