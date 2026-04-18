# GCP Configuration

## Target setup

This project is configured to use the following Google Cloud resources:

- Project ID: **transcribe-493712**
- Cloud Storage bucket: **umabot_audio_files**
- Service account: `umabottranscribe@transcribe-493712.iam.gserviceaccount.com`

The recommended local authentication method is **Application Default Credentials (ADC)** using **OAuth login** and, ideally, **service-account impersonation**.

> Do **not** create long-lived JSON service account keys unless you have no other option.

---

## Recommended authentication model

### Local development on macOS / VS Code

Use one of these two options:

1. **Preferred**: user login + service account impersonation
   - secure
   - short-lived tokens
   - no private key file to manage

2. **Fallback**: user login with ADC directly
   - works well for local testing
   - still avoids JSON keys

### GitHub identity federation

GitHub-based Workload Identity Federation is a good follow-up step for **GitHub Actions / CI**, but it is **not required** for local development.

---

## Prerequisites

Before testing GCP transcription, confirm the following:

- Billing is enabled for the project
- The project exists and is selected correctly
- The bucket exists and is writable by the runtime identity
- The service account exists
- You have permission to impersonate the service account if you want the most secure local flow

---

## 1) Install and initialize the Google Cloud CLI

If you do not already have the CLI installed, install it and sign in:

```bash
gcloud auth login
gcloud config set project transcribe-493712
```

---

## 2) Enable the required APIs

```bash
gcloud services enable \
  speech.googleapis.com \
  storage.googleapis.com \
  iamcredentials.googleapis.com \
  --project transcribe-493712
```

If you later set up GitHub OIDC / Workload Identity Federation for CI, also enable:

```bash
gcloud services enable sts.googleapis.com --project transcribe-493712
```

---

## 3) IAM guidance

Keep permissions minimal.

### Service account access

The service account used by the app should be able to:

- call Speech-to-Text
- upload audio objects to the bucket
- read the uploaded object if required
- delete temporary uploaded objects after processing

For bucket access, a bucket-scoped role such as **Storage Object User** or **Storage Object Admin** is typically appropriate.

### Your local user access

If you want to use service-account impersonation, your Google user should be granted:

- **Service Account Token Creator** on the service account

Avoid broad roles like **Owner** or **Editor** unless you are still in a temporary setup phase.

---

## 4) Configure local ADC without JSON keys

### Preferred: impersonate the service account

```bash
gcloud auth application-default login \
  --impersonate-service-account=umabottranscribe@transcribe-493712.iam.gserviceaccount.com
```

Then set the quota project:

```bash
gcloud auth application-default set-quota-project transcribe-493712
```

### Fallback: use your Google user credentials directly

```bash
gcloud auth application-default login
gcloud auth application-default set-quota-project transcribe-493712
```

### Verify that ADC is working

```bash
gcloud auth application-default print-access-token
```

If that returns a token, the local ADC setup is working.

---

## 5) Environment variables for this app

For the secure local flow, the only required variable is:

```bash
GCP_STORAGE_BUCKET=umabot_audio_files
```

Optional:

```bash
# Only set this if you intentionally want to use an explicit Google credential config
# GOOGLE_APPLICATION_CREDENTIALS=/path/to/google-credentials.json
```

> For local development, leave `GOOGLE_APPLICATION_CREDENTIALS` unset unless you have a specific reason to use it.

---

## 6) Install Python dependencies for GCP

```bash
pip install google-cloud-speech google-cloud-storage
```

Or install from the project requirements file:

```bash
pip install -r requirements.txt
```

---

## 7) Smoke test the transcription flow

Run a small test file first:

```bash
python3 ./scripts/mytranscript.py input/test.wav output/test-gcp.md --provider gcp --language en-US
```

Expected behavior:

- the app initializes the GCP provider
- the file is uploaded to the bucket
- Speech-to-Text processes the audio
- a markdown transcript is written to the output file

---

## Troubleshooting

### Error: missing default credentials

Run:

```bash
gcloud auth application-default login
```

Or, for the preferred secure setup:

```bash
gcloud auth application-default login \
  --impersonate-service-account=umabottranscribe@transcribe-493712.iam.gserviceaccount.com
```

### Error: quota project missing

Run:

```bash
gcloud auth application-default set-quota-project transcribe-493712
```

### Error: bucket access denied

Check that the runtime identity has access to **umabot_audio_files** and that the role is granted at the correct scope.

### Error: Speech API permission denied

Confirm that the Speech-to-Text API is enabled and the runtime identity can call the service in the selected project.

### Error: provider not available

Install the Google dependencies:

```bash
pip install google-cloud-speech google-cloud-storage
```

---

## Optional future enhancement: GitHub OIDC / Workload Identity Federation

If you later want to run GCP transcription from GitHub Actions without secrets:

- create a Workload Identity Pool
- add a GitHub OIDC provider
- restrict it with repository-level attribute conditions
- allow the federated identity to impersonate the service account

This is the right long-term approach for CI/CD, but it is separate from the local setup described above.
