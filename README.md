# Transcribe python script

## Table of Contents

- [About](#about)
- [Version & Release Notes](#version--release-notes)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Error Handling](#error-handling)
- [Testing AWS Configuration](#testing-aws-configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---
# About
This application transcribes audio files to text using AWS Transcribe. It supports various audio file formats and allows for language specification. Also it includes *diarization* (supported by [Partitioning speakers (diarization)](https://docs.aws.amazon.com/transcribe/latest/dg/diarization.html))

It is intended to run from the command line in MacOS as a python script, use as input the audio file and an output file.

It will call aws transcribe service, pass the audio and get the transcribed text in a markdown file (*.md)

## Version & Release Notes

### v.0.4 - release date 2025-07-19

- **Improved Error Handling**: Enhanced error validation and user experience
  - Added file format validation before AWS API calls
  - Converts AWS `ClientError` exceptions to user-friendly messages
  - Validates speaker count range (1-10) with clear error messages
  - Added graceful exit with `sys.exit(1)` instead of raw exceptions
  - Clear error messages with specific guidance on how to fix issues
  - Visual indicators using ❌ emoji for error messages
  - Supported formats: `amr`, `flac`, `wav`, `ogg`, `mp3`, `mp4`, `webm`, `m4a`

> For detailed release notes and technical changes, see [CHANGELOG.md](CHANGELOG.md)

### v.0.3 - release date 2025-01-07

- added diarization functionality
- user can define the number of speakers in the audio file (default=2)
- with option --no-diarization the script will not do diarization

### v.0.2 - release date 2024-12-22

- added automatic language identification
- added optional parameter to define the language of the audio (supports ISO code like es-ES, fr-FR, en-US, etc)

### v.0.1 - release date 2024-11-21

- takes an audio file and transcribes it, output format of the transcription in *markdown*

## Prerequisites

- Python 3.x
- AWS account with appropriate permissions for AWS Transcribe and S3
- Virtual environment (recommended)

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/transcribe_app.git
    cd transcribe_app
    ```

2. Create and activate a virtual environment:

    ```sh
    python3 -m venv venv_transcribe
    source venv_transcribe/bin/activate
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

# Usage

## Usage

In the command line, in your local directory:

1. Activate the virtual environment:

    ```sh
    source ~/development/venvs/venv_transcribe/bin/activate
    ```

2. Navigate to the project directory:

    ```sh
    cd ~/Documents/code/transcribe_app
    ```

3. Run the transcription script:

    ```sh
    python3 ./scripts/mytranscript.py {input_audio_file.mp3} {output_transcript_file.md} --language en-US
    ```

4. Run with --help for more options

    ```sh
    % python3 ./scripts/mytranscript.py --help
    Usage: mytranscript.py [OPTIONS] AUDIO_FILE OUTPUT_FILE

    Transcribe audio file to markdown text

    Options:
    -l, --language TEXT             Language code (e.g., es-ES, en-US). If not
                                    provided, automatic detection will be used.
    -s, --speakers INTEGER          Maximum number of speakers to identify
                                    (2-10)
    --diarization / --no-diarization
                                    Enable/disable speaker diarization
    --help                          Show this message and exit.
    ```

## Error Handling

The application now provides improved error handling with clear, user-friendly messages:

- **File Format Validation**: Automatically checks if your audio file format is supported before uploading
- **Clear Error Messages**: Instead of technical AWS errors, you'll see helpful messages like:
  ```
  ❌ Unsupported file format: 'mov'. AWS Transcribe supports: amr, flac, m4a, mp3, mp4, ogg, wav, webm
  ```
- **Parameter Validation**: Validates input parameters (e.g., speaker count must be between 2-10)
- **AWS Error Translation**: Converts complex AWS error codes into understandable messages
- **Visual Indicators**: Uses ❌ and ✅ emojis to clearly indicate success or failure

## Testing AWS Configuration

The script `test_aws.py` helps to check that your AWS configuration is working:

```sh
python3 ./scripts/test_aws.py
Successfully connected to AWS
Available buckets: [<your-list-of-s3-buckets>]
```

# Troubleshooting

If you encounter issues, check the following:

- Ensure your AWS credentials are correct and have the necessary permissions.
- Verify that the input audio file exists and is in a supported format.
- Check the AWS Transcribe service limits and quotas.

# Contributing

Contributions are welcome! Please open an issue or submit a pull request.

# License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

### Read more

Go to the DIR `./docs` to check for more configuration settings
