<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Chinese</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large">Chinese</ion-title>
        </ion-toolbar>
      </ion-header>

      <TalkByTextContainer language="zh-CN" utteranceLang="zh" name="Tab 2 page" />
    </ion-content>
  </ion-page>
</template>

<script setup lang="js">
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent } from '@ionic/vue';
import TalkByTextContainer from '@/components/TalkByTextContainer.vue';
</script>
