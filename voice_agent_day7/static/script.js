function generateAudio() {
    const text = document.getElementById("textInput").value;

    fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text }),
    })
    .then((response) => response.json())
    .then((data) => {
        const audioPlayer = document.getElementById("audioPlayer");
        audioPlayer.src = data.audio_url;
        audioPlayer.play();
    })
    .catch((err) => {
        console.error("Error generating audio:", err);
    });
}

let mediaRecorder;
let audioChunks = [];

const startButton = document.getElementById("startRecording");
const stopButton = document.getElementById("stopRecording");
const echoAudio = document.getElementById("echoAudio");
const statusMessage = document.getElementById("uploadStatus");

startButton.addEventListener("click", async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.addEventListener("dataavailable", (event) => {
            audioChunks.push(event.data);
        });

        mediaRecorder.addEventListener("stop", () => {
            const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
            const formData = new FormData();
            const filename = `recording_${Date.now()}.webm`;
            formData.append("file", audioBlob, filename);

            statusMessage.innerText = "Uploading...";
            fetch("/tts/echo", {
                method: "POST",
                body: formData,
            })
            .then((res) => res.json())
            .then((data) => {
                statusMessage.innerText = "✅ Playing back in Murf voice";
                echoAudio.src = data.audio_url;
                echoAudio.play();
            })
            .catch((err) => {
                statusMessage.innerText = "❌ Echo failed";
                console.error("Echo error:", err);
            });
        });

        mediaRecorder.start();
        startButton.disabled = true;
        stopButton.disabled = false;
    } catch (err) {
        console.error("Error starting recording:", err);
    }
});

stopButton.addEventListener("click", () => {
    mediaRecorder.stop();
    startButton.disabled = false;
    stopButton.disabled = true;
});
