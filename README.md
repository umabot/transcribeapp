# Transcribe python script
This application transcribes audio files to text using AWS Transcribe. It supports various audio file formats and allows for language specification.

It is intended to run from the command line in MacOS as a python script, use as input the audio file and an output file.

It will call aws transcribe service, pass the audio and get the transcribed text in a markdown file (*.md)

## Version
v.0.1

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

## Testing AWS Configuration

The script `test_aws.py` helps to check that your AWS configuration is working:

```sh
python3 ./scripts/test_aws.py
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

[licenseLink]: ./LICENSE