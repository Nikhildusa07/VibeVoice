// ----------- File Upload Functionality -----------
document.getElementById("uploadBtn").addEventListener("click", function () {
    console.log("File upload predict button clicked");

    var fileInput = document.getElementById("audioFile");
    if (fileInput.files.length === 0) {
        alert("Please select an audio file.");
        return;
    }

    var file = fileInput.files[0];
    console.log("Selected file:", file);

    var formData = new FormData();
    formData.append("audio", file);

    console.log("Sending file upload request to /predict");
    fetch("/predict", {
        method: "POST",
        body: formData,
    })
        .then((response) => {
            console.log("Received response:", response);
            return response.json();
        })
        .then((data) => {
            console.log("Received data:", data);
            if (data.error) {
                alert("Error: " + data.error);
                return;
            }

            // Display the result
            showResult(data.emotion, data.suggestions);
        })
        .catch((error) => {
            console.error("Error during file upload fetch:", error);
            alert("An error occurred while predicting emotion from file.");
        });
});

// ----------- Recording Functionality -----------
let mediaRecorder;
let recordedChunks = [];

const recordBtn = document.getElementById("recordBtn");
const stopBtn = document.getElementById("stopBtn");
const predictRecordedBtn = document.getElementById("predictRecordedBtn");
const recordedAudio = document.getElementById("recordedAudio");
const recordingStatus = document.getElementById("recordingStatus");
const recordIcon = document.getElementById("recordIcon");

recordBtn.addEventListener("click", async function () {
    console.log("Start recording button clicked");
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        recordedChunks = [];

        mediaRecorder.ondataavailable = function (event) {
            if (event.data && event.data.size > 0) {
                recordedChunks.push(event.data);
            }
        };

        mediaRecorder.onstart = function () {
            recordingStatus.innerText = "Recording...";
            recordIcon.classList.add("recording-active");
        };

        mediaRecorder.onstop = function () {
            recordingStatus.innerText = "Recording stopped.";
            recordIcon.classList.remove("recording-active");

            // Combine recorded chunks into a blob.
            const audioBlob = new Blob(recordedChunks, { type: "audio/webm" });
            const audioUrl = URL.createObjectURL(audioBlob);
            recordedAudio.src = audioUrl;
            recordedAudio.style.display = "block";
            predictRecordedBtn.style.display = "inline-block";
        };

        mediaRecorder.start();
        console.log("Recording started");
        recordBtn.disabled = true;
        stopBtn.disabled = false;
    } catch (err) {
        console.error("Error accessing microphone:", err);
        alert("Could not access your microphone.");
    }
});

stopBtn.addEventListener("click", function () {
    console.log("Stop recording button clicked");
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
        mediaRecorder.stop();
        console.log("Recording stopped");
        recordBtn.disabled = false;
        stopBtn.disabled = true;
    }
});

predictRecordedBtn.addEventListener("click", function () {
    console.log("Predict from recording button clicked");
    if (recordedChunks.length === 0) {
        alert("No recording available. Please record audio first.");
        return;
    }

    // Create a Blob from the recorded chunks
    const audioBlob = new Blob(recordedChunks, { type: "audio/webm" });
    const formData = new FormData();
    formData.append("audio", audioBlob, "recorded_audio.webm");

    console.log("Sending recorded audio to /predict");
    fetch("/predict", {
        method: "POST",
        body: formData,
    })
        .then((response) => {
            console.log("Received response for recorded audio:", response);
            return response.json();
        })
        .then((data) => {
            console.log("Received data:", data);
            if (data.error) {
                alert("Error: " + data.error);
                return;
            }

            // Display the result
            showResult(data.emotion, data.suggestions);
        })
        .catch((error) => {
            console.error("Error during recorded audio fetch:", error);
            alert("An error occurred while predicting emotion from your recording.");
        });
});

// ----------- Function to Show Result with Blur Effect -----------
function showResult(emotion, suggestions) {
    const resultDiv = document.getElementById("result");
    const emotionText = document.getElementById("emotion");
    const suggestionsList = document.getElementById("suggestions");
    const overlay = document.getElementById("overlay");

    // Update emotion text
    emotionText.innerText = " ---You Are Too " + emotion +"---";
    emotionText.style.fontSize = "33px"; // Adjust size as needed
emotionText.style.fontWeight = "bold"; // Make it bold
emotionText.style.color = "#e3c117"; // Keep the color
    console.log("I Have Some Suggestions For You To Improve Your Mood");

    // Clear previous suggestions and add new ones
    suggestionsList.innerHTML = "";
    suggestions.forEach(function (suggestion) {
        const li = document.createElement("li");
        li.innerText = suggestion;
        suggestionsList.appendChild(li);
    });

    // Show result and blur only the background
    overlay.style.display = "block";
    resultDiv.style.display = "block";

    setTimeout(() => {
        resultDiv.classList.add("active");
    }, 50);
}

// ----------- Function to Hide Result and Remove Blur -----------
document.getElementById("overlay").addEventListener("click", function () {
    const resultDiv = document.getElementById("result");
    const overlay = document.getElementById("overlay");

    resultDiv.classList.remove("active");

    setTimeout(() => {
        resultDiv.style.display = "none";
        overlay.style.display = "none";
    }, 500);
});


// // ----------- Function to Close the Result -----------
// document.getElementById("closeResult").addEventListener("click", function () {
//     const resultDiv = document.getElementById("result");
//     const overlay = document.getElementById("overlay");

//     resultDiv.classList.remove("active");

//     setTimeout(() => {
//         resultDiv.style.display = "none";
//         overlay.style.display = "none";
//     }, 500);
// });