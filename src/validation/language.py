"""Language code validation utilities for different providers."""

import re
from typing import Optional, Set

from src.errors import ValidationError


# BCP-47 pattern: language-REGION (e.g., en-US, fr-FR)
BCP47_PATTERN = re.compile(r'^[a-z]{2,3}-[A-Z]{2}$')

# ISO 639-1 pattern: two-letter language code (e.g., en, fr)
ISO639_PATTERN = re.compile(r'^[a-z]{2}$')


# AWS Transcribe supported languages (subset of most common)
AWS_SUPPORTED_LANGUAGES: Set[str] = {
    'en-US', 'en-GB', 'en-AU', 'en-IN', 'en-IE', 'en-AB', 'en-WL', 'en-ZA',
    'es-ES', 'es-US', 'es-MX',
    'fr-FR', 'fr-CA',
    'de-DE', 'de-CH',
    'it-IT',
    'pt-BR', 'pt-PT',
    'nl-NL',
    'ja-JP',
    'ko-KR',
    'zh-CN', 'zh-TW',
    'ar-SA', 'ar-AE',
    'hi-IN',
    'ru-RU',
    'pl-PL',
    'sv-SE',
    'da-DK',
    'fi-FI',
    'no-NO',
    'he-IL',
    'id-ID',
    'ms-MY',
    'th-TH',
    'tr-TR',
    'vi-VN',
    'uk-UA',
    'cs-CZ',
    'el-GR',
    'hu-HU',
    'ro-RO',
    'ta-IN',
    'te-IN',
    'af-ZA',
}

# GCP Speech-to-Text supported languages (subset of most common)
GCP_SUPPORTED_LANGUAGES: Set[str] = {
    'en-US', 'en-GB', 'en-AU', 'en-IN', 'en-CA', 'en-NZ', 'en-SG', 'en-ZA',
    'es-ES', 'es-US', 'es-MX', 'es-AR', 'es-CL', 'es-CO',
    'fr-FR', 'fr-CA', 'fr-BE', 'fr-CH',
    'de-DE', 'de-AT', 'de-CH',
    'it-IT',
    'pt-BR', 'pt-PT',
    'nl-NL', 'nl-BE',
    'ja-JP',
    'ko-KR',
    'zh-CN', 'zh-TW', 'zh-HK',
    'ar-SA', 'ar-EG', 'ar-AE', 'ar-MA',
    'hi-IN',
    'ru-RU',
    'pl-PL',
    'sv-SE',
    'da-DK',
    'fi-FI',
    'nb-NO',
    'he-IL',
    'id-ID',
    'ms-MY',
    'th-TH',
    'tr-TR',
    'vi-VN',
    'uk-UA',
    'cs-CZ',
    'el-GR',
    'hu-HU',
    'ro-RO',
    'ta-IN',
    'te-IN',
    'bn-IN',
    'gu-IN',
    'mr-IN',
    'ml-IN',
    'kn-IN',
    'fil-PH',
    'bg-BG',
    'hr-HR',
    'sk-SK',
    'sl-SI',
    'ca-ES',
    'eu-ES',
    'gl-ES',
}

# Azure Speech supported languages (subset of most common)
AZURE_SUPPORTED_LANGUAGES: Set[str] = {
    'en-US', 'en-GB', 'en-AU', 'en-IN', 'en-CA', 'en-NZ', 'en-SG', 'en-ZA', 'en-IE',
    'es-ES', 'es-MX', 'es-AR', 'es-CL', 'es-CO', 'es-US',
    'fr-FR', 'fr-CA', 'fr-BE', 'fr-CH',
    'de-DE', 'de-AT', 'de-CH',
    'it-IT',
    'pt-BR', 'pt-PT',
    'nl-NL', 'nl-BE',
    'ja-JP',
    'ko-KR',
    'zh-CN', 'zh-TW', 'zh-HK',
    'ar-SA', 'ar-EG', 'ar-AE', 'ar-BH', 'ar-KW', 'ar-QA',
    'hi-IN',
    'ru-RU',
    'pl-PL',
    'sv-SE',
    'da-DK',
    'fi-FI',
    'nb-NO',
    'he-IL',
    'id-ID',
    'ms-MY',
    'th-TH',
    'tr-TR',
    'vi-VN',
    'uk-UA',
    'cs-CZ',
    'el-GR',
    'hu-HU',
    'ro-RO',
    'ta-IN',
    'te-IN',
    'bn-IN',
    'gu-IN',
    'mr-IN',
    'ml-IN',
    'kn-IN',
    'fil-PH',
    'bg-BG',
    'hr-HR',
    'sk-SK',
    'sl-SI',
    'ca-ES',
    'cy-GB',
    'et-EE',
    'lv-LV',
    'lt-LT',
    'mt-MT',
}

# Whisper supported languages (ISO 639-1 codes)
WHISPER_SUPPORTED_LANGUAGES: Set[str] = {
    'en', 'es', 'fr', 'de', 'it', 'pt', 'nl', 'ja', 'ko', 'zh',
    'ar', 'hi', 'ru', 'pl', 'sv', 'da', 'fi', 'no', 'he', 'id',
    'ms', 'th', 'tr', 'vi', 'uk', 'cs', 'el', 'hu', 'ro', 'ta',
    'te', 'bn', 'gu', 'mr', 'ml', 'kn', 'bg', 'hr', 'sk', 'sl',
    'ca', 'cy', 'et', 'lv', 'lt', 'mt', 'af', 'sq', 'am', 'hy',
    'az', 'eu', 'be', 'bs', 'my', 'km', 'ceb', 'ny', 'co', 'ht',
    'haw', 'hmn', 'is', 'ig', 'ga', 'jw', 'kk', 'lo', 'la', 'lb',
    'mk', 'mg', 'mi', 'mn', 'ne', 'ps', 'fa', 'pa', 'sm', 'gd',
    'sr', 'st', 'sn', 'sd', 'si', 'so', 'su', 'sw', 'tg', 'tt',
    'tl', 'ur', 'uz', 'xh', 'yi', 'yo', 'zu',
}


def validate_bcp47(language_code: str, provider: str = "cloud") -> str:
    """
    Validate a BCP-47 language code.
    
    Args:
        language_code: The language code to validate (e.g., "en-US")
        provider: Provider name for error messages
        
    Returns:
        The validated language code
        
    Raises:
        ValidationError: If the code is invalid
    """
    if not language_code:
        raise ValidationError("Language code cannot be empty")
    
    # Normalize: ensure correct case (xx-YY)
    parts = language_code.split('-')
    if len(parts) != 2:
        raise ValidationError(
            f"Invalid language code format: '{language_code}'. "
            f"{provider} requires BCP-47 format (e.g., en-US, fr-FR)"
        )
    
    normalized = f"{parts[0].lower()}-{parts[1].upper()}"
    
    if not BCP47_PATTERN.match(normalized):
        raise ValidationError(
            f"Invalid language code format: '{language_code}'. "
            f"{provider} requires BCP-47 format (e.g., en-US, fr-FR)"
        )
    
    return normalized


def validate_iso639(language_code: str) -> str:
    """
    Validate an ISO 639-1 language code.
    
    Args:
        language_code: The language code to validate (e.g., "en")
        
    Returns:
        The validated language code (lowercase)
        
    Raises:
        ValidationError: If the code is invalid
    """
    if not language_code:
        raise ValidationError("Language code cannot be empty")
    
    normalized = language_code.lower()
    
    if not ISO639_PATTERN.match(normalized):
        raise ValidationError(
            f"Invalid language code format: '{language_code}'. "
            f"Local Whisper requires ISO-639-1 format (2-letter code, e.g., en, fr, es)"
        )
    
    return normalized


def validate_aws_language(language_code: Optional[str]) -> Optional[str]:
    """
    Validate language code for AWS Transcribe.
    
    Args:
        language_code: BCP-47 code or None for auto-detect
        
    Returns:
        Validated code or None
        
    Raises:
        ValidationError: If invalid
    """
    if language_code is None:
        return None
    
    normalized = validate_bcp47(language_code, "AWS Transcribe")
    
    if normalized not in AWS_SUPPORTED_LANGUAGES:
        supported_sample = ', '.join(sorted(list(AWS_SUPPORTED_LANGUAGES))[:10])
        raise ValidationError(
            f"Language '{normalized}' is not supported by AWS Transcribe. "
            f"Examples of supported codes: {supported_sample}..."
        )
    
    return normalized


def validate_gcp_language(language_code: Optional[str]) -> Optional[str]:
    """
    Validate language code for GCP Speech-to-Text.
    
    Args:
        language_code: BCP-47 code or None for auto-detect
        
    Returns:
        Validated code or None
        
    Raises:
        ValidationError: If invalid
    """
    if language_code is None:
        return None
    
    normalized = validate_bcp47(language_code, "GCP Speech-to-Text")
    
    if normalized not in GCP_SUPPORTED_LANGUAGES:
        supported_sample = ', '.join(sorted(list(GCP_SUPPORTED_LANGUAGES))[:10])
        raise ValidationError(
            f"Language '{normalized}' is not supported by GCP Speech-to-Text. "
            f"Examples of supported codes: {supported_sample}..."
        )
    
    return normalized


def validate_azure_language(language_code: Optional[str]) -> Optional[str]:
    """
    Validate language code for Azure AI Speech.
    
    Args:
        language_code: BCP-47 code or None for auto-detect
        
    Returns:
        Validated code or None
        
    Raises:
        ValidationError: If invalid
    """
    if language_code is None:
        return None
    
    normalized = validate_bcp47(language_code, "Azure AI Speech")
    
    if normalized not in AZURE_SUPPORTED_LANGUAGES:
        supported_sample = ', '.join(sorted(list(AZURE_SUPPORTED_LANGUAGES))[:10])
        raise ValidationError(
            f"Language '{normalized}' is not supported by Azure AI Speech. "
            f"Examples of supported codes: {supported_sample}..."
        )
    
    return normalized


def validate_whisper_language(language_code: Optional[str]) -> Optional[str]:
    """
    Validate language code for local Whisper.
    
    Args:
        language_code: ISO-639-1 code or None for auto-detect
        
    Returns:
        Validated code or None
        
    Raises:
        ValidationError: If invalid
    """
    if language_code is None:
        return None
    
    normalized = validate_iso639(language_code)
    
    if normalized not in WHISPER_SUPPORTED_LANGUAGES:
        supported_sample = ', '.join(sorted(list(WHISPER_SUPPORTED_LANGUAGES))[:15])
        raise ValidationError(
            f"Language '{normalized}' is not supported by Whisper. "
            f"Examples of supported codes: {supported_sample}..."
        )
    
    return normalized


def get_aws_supported_languages() -> Set[str]:
    """Return set of AWS Transcribe supported language codes."""
    return AWS_SUPPORTED_LANGUAGES.copy()


def get_gcp_supported_languages() -> Set[str]:
    """Return set of GCP Speech-to-Text supported language codes."""
    return GCP_SUPPORTED_LANGUAGES.copy()


def get_azure_supported_languages() -> Set[str]:
    """Return set of Azure AI Speech supported language codes."""
    return AZURE_SUPPORTED_LANGUAGES.copy()


def get_whisper_supported_languages() -> Set[str]:
    """Return set of Whisper supported language codes."""
    return WHISPER_SUPPORTED_LANGUAGES.copy()
