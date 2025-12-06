<script setup lang="ts">
import { ref } from "vue";

const emit = defineEmits(["send"]);
const message = ref("");

const submit = () => {
  if (!message.value.trim()) return;
  emit("send", message.value.trim());
  message.value = "";
};
</script>

<template>
  <form
    @submit.prevent="submit"
    class="flex items-center gap-3 p-4 bg-card border-t border-border"
  >
    <input
      v-model="message"
      @keydown.enter.prevent="submit"
      type="text"
      placeholder="Digite sua mensagem..."
      class="flex-1 px-4 py-3 rounded-full bg-chat-input-bg border border-border focus:ring-2 focus:ring-primary/30 text-sm"
    />

    <button
      type="submit"
      class="h-12 w-12 rounded-full bg-primary text-primary-foreground shadow-lg hover:scale-105 active:scale-95"
      :disabled="!message.trim()"
    >
      ➤
    </button>
  </form>
</template>
