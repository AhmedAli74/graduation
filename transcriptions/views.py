from django.shortcuts import render
from django import forms
import assemblyai as aai
import openai
from django.http import JsonResponse
import os

# Ensure you set your OpenAI API key
openai.api_key = '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'  # Use environment variable or set directly
# Form for uploading audio
class UploadFileForm(forms.Form):
    audio_file = forms.FileField()

# Speech-to-Text using AssemblyAI
def index(request):
    context = None
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {"error": "Provide a valid file"}
            return render(request, "transcriptions/index.html", context)
        
        try:
            # Get file
            file = request.FILES['audio_file']
            
            # Transcribe with AssemblyAI
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(file.file)

            file.close()

            if transcript.error:
                context = {"error": transcript.error}
            else:
                context = {"transcript": transcript.text}
        
        except Exception as e:
            context = {"error": str(e)}
    
    return render(request, "transcriptions/index.html", context)

# New: Text-to-Speech using OpenAI TTS API
def text_to_speech(request):
    if request.method == "POST":
        text = request.POST.get("text", "")

        if not text:
            return JsonResponse({"error": "No text provided"}, status=400)

        try:
            # Use the correct OpenAI TTS method
            response = openai.audio.speech.create(
                model="tts-1",
                input=text,
                voice="alloy"
            )

            # Return the generated speech file
            return JsonResponse({"audio_url": response["url"]})  # OpenAI returns a URL to the generated speech file

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)