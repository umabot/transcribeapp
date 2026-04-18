#!/usr/bin/env python3
"""
Multi-Cloud Transcription CLI

Transcribe audio files using AWS Transcribe, GCP Speech-to-Text, 
Azure AI Speech, or local Whisper.
"""

import os
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

import click
from dotenv import load_dotenv

from src.transcribe.factory import TranscriberFactory
from src.storage.local import LocalStorage
from src.errors import (
    ErrorHandler,
    TranscriptionError,
    ValidationError,
    AuthenticationError,
)

# Load environment variables
load_dotenv()

# Provider configuration
PROVIDER_ENV_VARS = {
    'aws': ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_REGION', 'AWS_S3_BUCKET'],
    'gcp': ['GCP_STORAGE_BUCKET'],  # Auth uses ADC or GOOGLE_APPLICATION_CREDENTIALS
    'azure': ['AZURE_SPEECH_KEY', 'AZURE_SPEECH_REGION'],
    'local': [],  # No env vars required
}


def validate_provider_env(provider: str) -> list:
    """
    Validate that required environment variables are set for the provider.
    
    Returns:
        List of missing environment variable names
    """
    required = PROVIDER_ENV_VARS.get(provider, [])
    return [var for var in required if not os.getenv(var)]


def show_provider_help(ctx, param, value):
    """Show provider-specific help."""
    if not value:
        return
    
    click.echo("\n📋 Available Transcription Providers\n")
    click.echo("=" * 60)
    
    info = TranscriberFactory.get_provider_info()
    
    for name, details in info.items():
        status = "✅ Available" if details['available'] else "❌ Not installed"
        click.echo(f"\n{name.upper()} - {details['name']}")
        click.echo(f"  Status: {status}")
        
        if details['env_vars']:
            click.echo(f"  Environment Variables:")
            for var in details['env_vars']:
                is_set = "✓" if os.getenv(var) else "✗"
                click.echo(f"    [{is_set}] {var}")
        else:
            click.echo(f"  Environment Variables: None required")

        if name == 'gcp':
            click.echo(
                "  Authentication: ADC via 'gcloud auth application-default login' "
                "(recommended) or GOOGLE_APPLICATION_CREDENTIALS"
            )
        
        click.echo(f"  Language Format: {details['language_format']}")
        click.echo(f"  Diarization: {details['diarization_support']}")
        
        if 'hardware_requirements' in details:
            click.echo(f"  Hardware: {details['hardware_requirements']}")
    
    click.echo("\n")
    ctx.exit(0)


def show_language_help(ctx, param, value):
    """Show language code format help."""
    if not value:
        return
    
    click.echo("\n🌐 Language Code Formats by Provider\n")
    click.echo("=" * 60)
    
    click.echo("""
┌───────────┬─────────────┬─────────────────────────────────┐
│ Provider  │ Format      │ Examples                        │
├───────────┼─────────────┼─────────────────────────────────┤
│ AWS       │ BCP-47      │ en-US, fr-FR, es-ES, de-DE     │
│ GCP       │ BCP-47      │ en-GB, zh-CN, ja-JP, pt-BR     │
│ Azure     │ BCP-47      │ en-AU, it-IT, ko-KR, nl-NL     │
│ Local     │ ISO-639-1   │ en, fr, es, de, ja, zh         │
└───────────┴─────────────┴─────────────────────────────────┘

BCP-47 Format: language-REGION (e.g., en-US for English - United States)
ISO-639-1: Two-letter language code (e.g., en for English)

Note: 
- Cloud providers (AWS/GCP/Azure) require the full BCP-47 format
- Local Whisper uses simpler 2-letter codes
- If language is omitted, automatic detection will be used
""")
    ctx.exit(0)


def show_speakers_help(ctx, param, value):
    """Show speaker diarization help."""
    if not value:
        return
    
    click.echo("\n👥 Speaker Diarization Guide\n")
    click.echo("=" * 60)
    
    click.echo("""
Speaker diarization identifies and labels different speakers in audio.

Provider Support:
┌───────────┬────────────────────┬───────────────────────────────┐
│ Provider  │ Max Speakers       │ Notes                         │
├───────────┼────────────────────┼───────────────────────────────┤
│ AWS       │ 2-10               │ Full diarization support      │
│ GCP       │ 2-10               │ Full diarization support      │
│ Azure     │ 2-10               │ Uses ConversationTranscriber  │
│ Local     │ N/A                │ Limited (requires pyannote)   │
└───────────┴────────────────────┴───────────────────────────────┘

Usage:
  --speakers N        Set maximum expected speakers (2-10)
  --diarization       Enable speaker separation (default)
  --no-diarization    Disable speaker labels

Tips:
- Set --speakers to match actual number for best results
- Diarization adds processing time
- Local Whisper doesn't support native diarization
""")
    ctx.exit(0)


class HelpOption(click.Option):
    """Custom option that supports sub-topic help."""
    
    def handle_parse_result(self, ctx, opts, args):
        if self.name in opts:
            value = opts[self.name]
            if value in ('provider', 'providers'):
                show_provider_help(ctx, None, True)
            elif value in ('language', 'languages', 'lang'):
                show_language_help(ctx, None, True)
            elif value in ('speaker', 'speakers', 'diarization'):
                show_speakers_help(ctx, None, True)
        return super().handle_parse_result(ctx, opts, args)


@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.argument('audio_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option(
    '--provider', '-p',
    type=click.Choice(['aws', 'gcp', 'azure', 'local'], case_sensitive=False),
    default='aws',
    help='Transcription provider to use'
)
@click.option(
    '--language', '-l',
    help='Language code (BCP-47 for cloud, ISO-639-1 for local). Omit for auto-detection.'
)
@click.option(
    '--speakers', '-s',
    type=int,
    default=2,
    help='Maximum number of speakers (2-10)'
)
@click.option(
    '--diarization/--no-diarization',
    default=True,
    help='Enable/disable speaker diarization'
)
@click.option(
    '--error-file', '-e',
    type=click.Path(),
    help='Path to write detailed error logs'
)
@click.option(
    '--model', '-m',
    default='base',
    help='Whisper model size (local only): tiny, base, small, medium, large'
)
@click.option(
    '--help-topic',
    cls=HelpOption,
    is_eager=True,
    expose_value=False,
    help='Show help for: provider, language, speakers'
)
def transcribe(audio_file, output_file, provider, language, speakers, diarization, error_file, model):
    """
    Transcribe audio files to markdown text.
    
    Supports multiple providers: AWS Transcribe, GCP Speech-to-Text,
    Azure AI Speech, and local Whisper.
    
    \b
    Examples:
      mytranscript.py audio.mp3 output.md
      mytranscript.py audio.wav output.md --provider gcp --language en-US
      mytranscript.py audio.m4a output.md --provider local --model small
      mytranscript.py audio.mp3 output.md --no-diarization
    
    \b
    For detailed help on specific topics:
      mytranscript.py --help-topic provider
      mytranscript.py --help-topic language
      mytranscript.py --help-topic speakers
    """
    # Initialize error handler
    error_handler = ErrorHandler(error_file=error_file)
    
    try:
        # Validate provider environment
        missing_vars = validate_provider_env(provider)
        if missing_vars:
            details = f"Set: {', '.join(missing_vars)}. See docs/env.md for configuration."
            if provider == 'gcp':
                details = (
                    f"Set: {', '.join(missing_vars)}. "
                    "Authentication can use Application Default Credentials "
                    "(recommended) or GOOGLE_APPLICATION_CREDENTIALS. "
                    "See docs/gcp_config.md for setup."
                )

            raise AuthenticationError(
                f"Missing required environment variables for {provider.upper()}",
                details=details
            )
        
        # Check provider availability
        if not TranscriberFactory.is_provider_available(provider):
            raise ValidationError(
                f"Provider '{provider}' is not available",
                details="Install required dependencies. Use --help-topic provider for details."
            )
        
        click.echo(f"🎙️  Starting transcription with {provider.upper()}...")
        click.echo(f"   Input: {audio_file}")
        click.echo(f"   Output: {output_file}")
        
        # Create transcriber with provider-specific options
        transcriber_kwargs = {}
        if provider == 'local':
            transcriber_kwargs['model_name'] = model
        
        transcriber = TranscriberFactory.get_transcriber(provider, **transcriber_kwargs)
        
        # Run transcription
        transcript_data = transcriber.transcribe(
            file_path=audio_file,
            language_code=language,
            enable_diarization=diarization,
            max_speakers=speakers
        )
        
        # Get provider name for storage
        provider_name = transcript_data.get('metadata', {}).get('provider', provider.upper())
        
        # Save to markdown
        LocalStorage.save_markdown(
            transcript_data=transcript_data,
            output_file=output_file,
            input_file=audio_file,
            language=language,
            speakers=speakers,
            diarization=diarization,
            provider=provider_name
        )
        
        click.echo(f"✅ Transcription completed!")
        sys.exit(0)
        
    except TranscriptionError as e:
        error_handler.handle(e, exit_on_error=True)
        
    except KeyboardInterrupt:
        click.echo("\n⚠️  Transcription cancelled by user", err=True)
        sys.exit(130)
        
    except Exception as e:
        # Wrap unexpected errors
        from src.errors import wrap_provider_exception
        wrapped = wrap_provider_exception(e, provider)
        error_handler.handle(wrapped, exit_on_error=True)


if __name__ == '__main__':
    transcribe()