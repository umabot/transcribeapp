import os
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

import click
from dotenv import load_dotenv
from src.transcribe.transcriber import AWSTranscriber
from src.storage.local import LocalStorage

# Load environment variables
load_dotenv()

@click.command()
@click.argument('audio_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--language', '-l', help='Language code (e.g., es-ES, en-US). If not provided, automatic detection will be used.')
@click.option('--speakers', '-s', type=int, help='Maximum number of speakers to identify (2-10)', default=2)
@click.option('--diarization/--no-diarization', default=True, help='Enable/disable speaker diarization')
def transcribe(audio_file, output_file, language, speakers, diarization):
    """Transcribe audio file to markdown text"""
    try:
        transcriber = AWSTranscriber()
        storage = LocalStorage()
        
        click.echo(f"Starting transcription of {audio_file}...")
        
        # Process transcription
        text = transcriber.transcribe_file(audio_file, language, enable_diarization=diarization, max_speakers=speakers)
        storage.save_markdown(text, output_file, audio_file, language, speakers, diarization)
        
        click.echo(f"✅ Transcription completed! Output saved to {output_file}")
        
    except ValueError as e:
        # Handle validation and business logic errors
        click.echo(f"❌ {e}", err=True)
        sys.exit(1)
        
    except FileNotFoundError as e:
        click.echo(f"❌ File not found: {e}", err=True)
        sys.exit(1)
        
    except PermissionError as e:
        click.echo(f"❌ Permission error: {e}", err=True)
        sys.exit(1)
        
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        click.echo("Please check your configuration and try again.", err=True)
        sys.exit(1)

if __name__ == '__main__':
    transcribe()