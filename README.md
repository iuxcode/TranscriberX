# TranscriberX

The TranscriberX API is a real-time transcription service that uses AI technology to transcribe live and pre-recorded audio content into text. This API can be integrated into your own applications or services, providing automated transcription capabilities to your users.

## Getting Started

To use the TranscriberX API, you'll need to have the following:

- Python 3.x installed on your system
- Django framework installed on your system
- API credentials (provided upon registration)

## Installation

- Clone the repository or download the source code from the Github page.
- Install the required packages listed in the requirements.txt file using pip install -r requirements.txt.
- Create a new Django project and add the TranscriberX app to your project.
- Configure the API credentials by adding them to the Django settings file.
- Start the Django server using python manage.py runserver.

## Usage

### Endpoints

The TranscriberX API provides the following endpoints:

- /transcribe/live - for real-time transcription of live audio streams
- /transcribe/upload - for transcription of pre-recorded audio files

### Parameters

For the /transcribe/live endpoint, you'll need to provide the following parameters:

- audio - the live audio stream to be transcribed

For the /transcribe/upload endpoint, you'll need to provide the following parameters:

- audio - the pre-recorded audio file to be transcribed

### Response

The API will respond with a JSON object containing the transcribed text and any relevant metadata.

### Support

If you have any issues or questions about the TranscriberX API, please contact our support team at support@transcriberx.com.

### License

This project is licensed under the MIT License - see the LICENSE.md file for details.
