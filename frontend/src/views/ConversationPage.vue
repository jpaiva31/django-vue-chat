<script setup lang="ts">
import { useRoute } from "vue-router";
import ConversationContainer from "../components/conversations/ConversationContainer.vue";

const route = useRoute();

// URL: /chat/<id>
const conversationId = route.params.id as string;
</script>

<template>
  <main class="min-h-screen bg-muted">
    <ConversationContainer :conversationId="conversationId" />
  </main>
</template>