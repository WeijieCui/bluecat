<template>
  <div id="container">
    <button @click="startRecording" style="margin-right: 20px;">
      <font-awesome-icon :icon="['fas', 'microphone']" :class="{ 'recording': isRecording, 'fa-4x': true }"/>
    </button>
    <button @click="stopRecording">
      <font-awesome-icon :icon="['fas', 'stop']" :class="{'fa-4x': true }"/>
    </button>
  </div>
</template>

<script lang="js">
import {library} from '@fortawesome/fontawesome-svg-core';
import {faMicrophone, faStop} from '@fortawesome/free-solid-svg-icons';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

library.add(faMicrophone, faStop);

export default {
  name: "TalkContainer",
  props: {
    msg: String,
  },
  components: {
    FontAwesomeIcon
  },
  data() {
    return {
      mediaRecorder: null,
      audioChunks: [],
      isRecording: false,
    };
  },
  methods: {
    startRecording() {
      this.isRecording = true;
      if (this.mediaRecorder) {
        this.mediaRecorder.stop();
      }
      navigator.mediaDevices.getUserMedia({audio: true})
          .then(stream => {
            const options = {mimeType: 'audio/webm'};
            this.mediaRecorder = new MediaRecorder(stream, options);
            this.mediaRecorder.start();

            this.mediaRecorder.addEventListener("dataavailable", event => {
              this.audioChunks.push(event.data);
            });
          });
    },
    stopRecording() {
      this.isRecording = false;
      this.mediaRecorder.stop();
      const audioBlob = new Blob(this.audioChunks);
      this.audioChunks = [];
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      console.log(audio);
      // You can now send `audioBlob` to your backend
      this.sendAudioToBackend(audioBlob);
    },
    async sendAudioToBackend(audioBlob) {
      const formData = new FormData();
      formData.append("audio", audioBlob);

      const response = await fetch("http://localhost:5000/bluecat_bk/chat", {
        method: "POST",
        body: formData
      });
      console.log(response)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      // Get the response data as a Blob
      const blob = await response.blob();

      // Create an Object URL from the Blob
      const audioUrl = URL.createObjectURL(blob);

      // Create an Audio object from the Object URL
      const audio = new Audio(audioUrl);

      // Play the audio
      await audio.play();
    }
  }
};
</script>

<style scoped>
#container {
  text-align: center;
  position: absolute;
  left: 0;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
}

#container strong {
  font-size: 20px;
  line-height: 26px;
}

#container p {
  font-size: 16px;
  line-height: 22px;
  color: #8c8c8c;
  margin: 0;
}

#container a {
  text-decoration: none;
}

.recording {
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}
</style>
