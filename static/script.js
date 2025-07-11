const recordAudioButton = document.getElementById('record-audio');
const stopAudioButton = document.getElementById('stop-audio');
const audioPlayback = document.getElementById('audio-playback');
const consentCheckbox = document.getElementById('consent-checkbox');

// Function to generate a UUID
function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        let r = Math.random() * 16 | 0,
            v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

// Get or generate USER_ID
let USER_ID = localStorage.getItem('user_id');
if (!USER_ID) {
    USER_ID = generateUUID();
    localStorage.setItem('user_id', USER_ID);
}

// Generate a new SESSION_ID for each session
const SESSION_ID = generateUUID();

let mediaRecorder;
let audioChunks = [];

consentCheckbox.addEventListener('change', async () => {
    recordAudioButton.disabled = !consentCheckbox.checked;
    if (consentCheckbox.checked) {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };

        audioPlayback.src = '/uploads/welcome.mp3';
        audioPlayback.play();
    } else {
        if (audioPlayback) {
            audioPlayback.pause();
            audioPlayback.currentTime = 0;
        }
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
        }
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

        const response = await fetch(`/process?user_id=${USER_ID}&session_id=${SESSION_ID}`, {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        if (result.filename) {
            audioPlayback.src = `/uploads/${result.filename.split('/').pop()}`;
            audioPlayback.play();
        }

        audioChunks = [];
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
