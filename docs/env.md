# .env

Add only the variables for the providers you plan to use.

## AWS

```bash
AWS_ACCESS_KEY_ID={the_aws_access_key_created_for_the_transcribe_user}
AWS_SECRET_ACCESS_KEY={the_aws_secret_access_key_created_for_the_transcribe_user}
AWS_REGION={your_aws_region}
AWS_S3_BUCKET={your_s3_name}
```

## GCP

```bash
GCP_STORAGE_BUCKET={your_gcp_bucket_name}
```

Optional for GCP:

```bash
# Only set this if you explicitly want to use a Google credential config file
# GOOGLE_APPLICATION_CREDENTIALS=/path/to/google-credentials.json
```

For local development, the recommended GCP authentication flow is **Application Default Credentials** via Google login, not a long-lived JSON key.

See the dedicated runbook in **docs/gcp_config.md**.

---

## Important

Make sure your `.env` file is ignored by `.gitignore`.

---
