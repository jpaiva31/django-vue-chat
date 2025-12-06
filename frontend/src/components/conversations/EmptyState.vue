<script setup lang="ts">
const emit = defineEmits(["start"]);
</script>

<template>
  <div class="flex flex-col items-center justify-center h-full text-center px-6">
    <div class="mb-6">
      <div class="flex items-center justify-center w-24 h-24 rounded-full bg-muted">
        📥
      </div>
    </div>

    <h2 class="text-xl font-semibold mb-2">Nenhuma conversa ainda</h2>
    <p class="text-muted-foreground mb-6 max-w-xs">
      Comece enviando sua primeira mensagem
    </p>

    <button
      @click="emit('start')"
      class="px-4 py-2 rounded-xl bg-primary text-primary-foreground shadow hover:opacity-90"
    >
      Começar Conversa
    </button>
  </div>
</template>
