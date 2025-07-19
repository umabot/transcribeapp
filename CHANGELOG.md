# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2025-07-19

### Added
- File format validation before AWS API calls
- Comprehensive error handling with user-friendly messages
- Parameter validation for speaker count range (2-10)
- Visual indicators using ❌ and ✅ emojis for error and success messages
- Graceful error handling with specific guidance on how to fix issues

### Changed
- AWS `ClientError` exceptions are now converted to user-friendly `ValueError` messages
- Error messages now provide clear guidance instead of raw AWS stack traces
- Script exits gracefully with `sys.exit(1)` instead of raising exceptions

### Fixed
- Prevents unnecessary AWS API calls for unsupported file formats
- Better handling of S3 upload errors with specific error codes
- Improved transcription job failure messages

### Technical Details
- Added `SUPPORTED_FORMATS` constant: `amr`, `flac`, `wav`, `ogg`, `mp3`, `mp4`, `webm`, `m4a`
- Added `_validate_file_format()` method to `AWSTranscriber` class
- Added `_validate_parameters()` method for input validation
- Enhanced error handling in `upload_to_s3()` and `transcribe_file()` methods

## [0.3.0] - 2025-01-07

### Added
- Diarization functionality with speaker identification
- User-configurable number of speakers (default=2, range 2-10)
- `--diarization/--no-diarization` option to enable/disable speaker separation

### Technical Details
- Integrated AWS Transcribe speaker diarization capabilities
- Added speaker labels and timestamps to output

## [0.2.0] - 2024-12-22

### Added
- Automatic language identification when no language is specified
- Optional `--language` parameter to define audio language
- Support for ISO language codes (es-ES, fr-FR, en-US, etc.)

### Technical Details
- AWS Transcribe automatic language detection integration
- Language parameter validation

## [0.1.0] - 2024-11-21

### Added
- Initial release
- Basic audio file transcription using AWS Transcribe
- Markdown output format
- Command-line interface with Click
- S3 file upload functionality
- Basic AWS integration

### Technical Details
- Core transcription pipeline
- S3 storage integration
- Basic error handling
