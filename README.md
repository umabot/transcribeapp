# Transcribe python script
This is v.0.0
It is intended to run from the command line in MacOS as a python script, use as input the audio file and an outpu file.

It will call aws transcrive service, pass the audio and get the transcribed text

## Created using LLM
I used Claude Sonet via You.com agent called `Python dev`

Transcript of prompt [here](https://you.com/search?q=let%27s+start+with+a+small+improvement.%0A%0AIn+the+.md+output+file+now+you+have+a+section+that+has%3A%0A%0A%23...&cid=c1_40096e49-c992-4532-99f2-14e0f7859288&tbm=youchat)

## aws settings
It is using a dedicated and limited use in my personal aws account.

The S3 bucket created is `transcribeapp`

And it uses [aws transcribe service](https://eu-west-3.console.aws.amazon.com/transcribe/home?region=eu-west-3#welcome)

# Usage
in the command line, in your local dir:
```
source ~/development/venvs/venv_transcript/bin/activate
cd ~/Documents/code/transcribe_app
python3 ./scripts/mytranscript.py {input_audio_file.mp"} {output_transcript_file.md}