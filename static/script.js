const recordAudioButton = document.getElementById('record-audio');
const stopAudioButton = document.getElementById('stop-audio');
const audioPlayback = document.getElementById('audio-playback');
const consentCheckbox = document.getElementById('consent-checkbox');
const welcomeMessage = document.getElementById('welcome-message');

// Function to generate a UUID
function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        let r = Math.random() * 16 | 0,
            v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

// Get or generate USER_ID and set welcome message
let USER_ID = localStorage.getItem('user_id');
if (!USER_ID) {
    USER_ID = generateUUID();
    localStorage.setItem('user_id', USER_ID);
    welcomeMessage.textContent = 'Welcome';
} else {
    welcomeMessage.textContent = `Welcome back ${USER_ID}`;
}

// Generate a new SESSION_ID for each session
const SESSION_ID = generateUUID();

// Get session recording consent from localStorage
let sessionRecordingConsent = localStorage.getItem('sessionRecordingConsent') === 'true';
consentCheckbox.checked = sessionRecordingConsent;

let mediaRecorder;
let audioChunks = [];

consentCheckbox.addEventListener('change', () => {
    sessionRecordingConsent = consentCheckbox.checked;
    localStorage.setItem('sessionRecordingConsent', sessionRecordingConsent);
    if (sessionRecordingConsent) {
        audioPlayback.src = '/static/welcome.mp3';
        audioPlayback.play();
    }
});

// Record audio
recordAudioButton.addEventListener('click', async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const audioUrl = URL.createObjectURL(audioBlob);
        audioPlayback.src = audioUrl;

        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.wav');

        let url = `/process?user_id=${USER_ID}`;
        if (sessionRecordingConsent) {
            url += `&session_id=${SESSION_ID}`;
            url += `&consent=allow`;
        }

        try {
            const response = await fetch(url, {
                method: 'POST',
                body: formData
            });

            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('audio/')) {
                const responseAudioBlob = await response.blob();
                const responseAudioUrl = URL.createObjectURL(responseAudioBlob);

                audioPlayback.src = responseAudioUrl;
                audioPlayback.play()
                    .then(() => {
                        console.log('Backend audio played successfully!');
                    })
                    .catch(error => {
                        console.error('Error playing backend audio:', error);
                        audioPlayback.src = '/static/try_again.mp3';
                        audioPlayback.play();
                    });

                audioChunks = [];
            } else {
                const errorResult = await response.json();
                const errorMessage = errorResult.error || `HTTP error! Status: ${response.status} - ${JSON.stringify(errorResult)}`;
                throw new Error(errorMessage);
            }
        } catch (error) {
            console.error('Error during audio processing or playback:', error);
            audioPlayback.src = '/static/try_again.mp3';
            audioPlayback.play();
        } finally {
            audioChunks = [];
        }
    };

    mediaRecorder.start();
    recordAudioButton.disabled = true;
    stopAudioButton.disabled = false;
});

// Stop recording
stopAudioButton.addEventListener('click', () => {
    mediaRecorder.stop();
    recordAudioButton.disabled = false;
    stopAudioButton.disabled = true;
});