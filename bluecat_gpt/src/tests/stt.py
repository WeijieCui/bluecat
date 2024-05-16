import whisper

model = whisper.load_model("base")
result = model.transcribe("voice_record.m4a")
print(result["text"])
