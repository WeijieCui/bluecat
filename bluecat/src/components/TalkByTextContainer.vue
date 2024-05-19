<template>
  <div id="container">
    <div>
      <button @click="startListening" style="margin-right: 80px;">
        <font-awesome-icon :icon="['fas', 'microphone']" :class="{ 'recording': isRecording, 'fa-8x': true }"/>
      </button>
      <button @click="stopListening" style="margin-right: 80px;">
        <font-awesome-icon :icon="['fas', 'stop']" :class="{'fa-8x': true }"/>
      </button>
      <button @click="clear">
        <font-awesome-icon :icon="['fas', 'burn']" :class="{'fa-8x': true }"/>
      </button>
      <div v-for="(message, index) in messages" :key="index" style="margin-left:10%;width: 80%;">
        <div v-if="message.role === 'system'" style="width: 80%;text-align: left;">
          <strong style="margin-right: 10px">Robot</strong>
          {{ message.content }}
        </div>
        <div v-if="message.role === 'user'" style="margin-left: 20%; width: 80%;text-align: right;">
          {{ message.content }}<strong style="margin-left: 10px">You</strong>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="js">
import {library} from '@fortawesome/fontawesome-svg-core';
import {faMicrophone, faStop, faBurn} from '@fortawesome/free-solid-svg-icons';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

library.add(faMicrophone, faStop, faBurn);

export default {
  name: "TalkByTextContainer",
  props: {
    msg: String,
    language: String,
    utteranceLang: String,
  },
  components: {
    FontAwesomeIcon
  },
  data() {
    return {
      recognition: null,
      messages: [],
      isRecording: false,
    }
  },
  created() {
    // Check if SpeechRecognition is available
    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
      // Use SpeechRecognition if available, otherwise use webkitSpeechRecognition
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      this.recognition = new SpeechRecognition();

      // Set the language (optional)
      this.recognition.lang = this.language;

      // Set continuous mode to true to keep the microphone on
      this.recognition.continuous = true;

      // Set interim results to true to get results that are not yet final
      this.recognition.interimResults = true;

      // Define the onresult event handler
      this.recognition.onresult = (event) => {
        for (let i = event.resultIndex; i < event.results.length; i++) {
          if (event.results[i].isFinal) {
            const transcript = event.results[i][0].transcript;
            if (transcript === 'stop') {
              this.stopListening();
              return;
            }else if (transcript === '' || transcript === null || transcript === undefined) {
              return;
            }
            this.stopListening();
            if (this.messages.length > 2){
              this.messages.shift();
              this.messages.shift();
            }
            this.messages.push({role: 'user', content: transcript});
            fetch("http://localhost:5000/bluecat_bk/chat_by_text", {
              method: "POST",
              body: JSON.stringify({messages: this.messages}),
              headers: {
                "Content-Type": "application/json",
              },
            }).then(response => response.json()).then(data => {
              console.log(data);
              this.reply = data.reply;
              this.messages.push({role: 'system', content: data.reply});
              this.textToSpeech(data.reply);
            }).catch(error => {
              console.error('Error:', error);
            });
          }
        }
      };
    } else {
      console.log('SpeechRecognition is not available in this browser.');
    }
  },
  methods: {
    textToSpeech(reply) {
      this.stopListening();
      // Create a new SpeechSynthesisUtterance instance
      const utterance = new SpeechSynthesisUtterance(reply);
      // Set the language (optional)
      utterance.lang = this.utteranceLang;
      utterance.onend = () => {
        this.startListening();
      };

      // Set the volume (optional)
      utterance.volume = 1;

      // Set the rate (optional)
      utterance.rate = 1;

      // Set the pitch (optional)
      utterance.pitch = 1;

      // Use the SpeechSynthesis interface to speak the utterance
      window.speechSynthesis.speak(utterance);
    },
    startListening() {
      if (window.speechSynthesis.speaking) {
        window.speechSynthesis.cancel();
      }
      this.isRecording = true;
      if (this.recognition) {
        this.recognition.start();
      }
    },
    stopListening() {
      if (window.speechSynthesis.speaking) {
        window.speechSynthesis.cancel();
      }
      this.isRecording = false;
      if (this.recognition) {
        this.recognition.stop();
      }
    },
    clear() {
      if (window.speechSynthesis.speaking) {
        window.speechSynthesis.cancel();
      }
      this.messages = [];
    },
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
