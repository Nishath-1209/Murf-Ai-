async function generateAudio() {
    const text = document.getElementById("textInput").value;
    const response = await fetch("/generate-audio", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text })
    });
    if (!response.ok) {
        const errorText = await response.text();
        alert("Error: " + errorText);
        return;
    }
    const data = await response.json();
    if (data.audio_url) {
        const audioPlayer = document.getElementById("audioPlayer");
        audioPlayer.src = data.audio_url;
        audioPlayer.play();
    } else {
        alert("Failed to get audio. Try again.");
    }
}

let mediaRecorder;
let audioChunks = [];

const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const audioPlayback = document.getElementById('audioPlayback');
const statusText = document.getElementById('statusText'); // ← NEW

startBtn.onclick = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.start();
    audioChunks = [];
    statusText.innerText = "Recording..."; // ← NEW

    mediaRecorder.ondataavailable = event => {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
        const audioUrl = URL.createObjectURL(audioBlob);
        audioPlayback.src = audioUrl;

        // UPLOAD to server
        const formData = new FormData();
        formData.append("file", audioBlob, "recording.webm");

        statusText.innerText = "Uploading..."; // ← NEW

        try {
            const response = await fetch("/upload-audio", {
                method: "POST",
                body: formData
            });

            if (!response.ok) {
                throw new Error(await response.text());
            }

            const result = await response.json();
            statusText.innerText = `✅ Uploaded: ${result.filename} (${result.size_in_bytes} bytes)`;
        } catch (err) {
            console.error(err);
            statusText.innerText = "❌ Upload failed!";
        }
    };

    startBtn.disabled = true;
    stopBtn.disabled = false;
};

stopBtn.onclick = () => {
    mediaRecorder.stop();
    startBtn.disabled = false;
    stopBtn.disabled = true;
};
