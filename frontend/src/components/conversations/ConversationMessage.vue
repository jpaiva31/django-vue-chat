<template>
  <div
    class="flex flex-col"
    :class="isSent ? 'items-end' : 'items-start'"
  >
    <div
      class="max-w-xs px-4 py-2 rounded-lg shadow text-sm"
      :class="isSent
        ? 'bg-primary text-primary-foreground'
        : 'bg-muted text-foreground'"
    >
      {{ content }}
    </div>
    <span class="text-xs text-muted-foreground mt-1">
      {{ formattedTimestamp }}
    </span>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
  content: string;
  isSent: boolean;
  timestamp: string;
}>();

const formattedTimestamp = computed(() => {
  const date = new Date(props.timestamp);
  const hours = date.getHours().toString().padStart(2, "0");
  const minutes = date.getMinutes().toString().padStart(2, "0");
  return `${hours}:${minutes}`;
});
</script>
