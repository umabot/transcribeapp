# Scripts

Under `./scripts` you will find the 2 scripts:

- `test_aws.py` -> to test the aws configuration and connectivity from your command line
- `mytranscript.py` -> actual script to transcribe an audio file to text

## Basic usage

```sh
python3 mytranscript.py input.wav output.md
```

### With options

```sh
python3 mytranscript.py input.wav output.md --language fr-FR --speakers 3
```

### Get help

```sh
python3 mytranscript.py --help
```

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

The output will be something like:

```text
Successfully connected to AWS
Available buckets: ['bucket_1', 'bucket_1', '...', 'bucket_n']
```
