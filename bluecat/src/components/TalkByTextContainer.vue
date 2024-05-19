<template>
  <div id="container">
    <div>
      <button @click="startListening" style="margin-right: 20px;">Start Listening</button>
      <button @click="stopListening">Stop Listening</button>
      <button @click="clear">Clear</button>
      <div v-for="(message, index) in messages" :key="index">
        <p v-if="message.role === 'system'" style="float: left">
          <strong style="margin-right: 10px">Robot</strong>
          {{ message.content }}
        </p>
        <p v-if="message.role === 'user'" style="float: right">
          {{ message.content }}<strong style="margin-left: 10px">You</strong>
        </p>
      </div>
    </div>
  </div>
</template>

<script lang="js">
export default {
  name: "TalkContainer",
  props: {
    msg: String,
  },
  data() {
    return {
      recognition: null,
      messages: [],
    }
  },
  created() {
    // Check if SpeechRecognition is available
    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
      // Use SpeechRecognition if available, otherwise use webkitSpeechRecognition
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      this.recognition = new SpeechRecognition();

      // Set the language (optional)
      // this.recognition.lang = 'en-US';

      // Set continuous mode to true to keep the microphone on
      this.recognition.continuous = true;

      // Set interim results to true to get results that are not yet final
      this.recognition.interimResults = true;

      // Define the onresult event handler
      this.recognition.onresult = (event) => {
        for (let i = event.resultIndex; i < event.results.length; i++) {
          if (event.results[i].isFinal) {
            this.stopListening();
            this.messages.push({role: 'user', content: event.results[i][0].transcript});
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
      utterance.onend = () => {
        this.startListening();
      };
      // Set the language (optional)
      utterance.lang = 'en-US';

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
      if (this.recognition) {
        this.recognition.start();
      }
    },
    stopListening() {
      if (this.recognition) {
        this.recognition.stop();
      }
    },
    clear() {
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
</style>
