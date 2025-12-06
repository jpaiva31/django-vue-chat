<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted, nextTick } from "vue";
import ConversationMessage from "./ConversationMessage.vue";
import ConversationInput from "./ConversationInput.vue";
import EmptyState from "./EmptyState.vue";

interface Message {
  id: string;
  content: string;
  direction: "SENT" | "RECEIVED";
  timestamp: string;
}

interface ConversationResponse {
  id: string;
  state: "OPEN" | "CLOSED";
  messages: Message[];
}

const props = defineProps<{
  conversationId: string;
}>();

const chatState = ref<"OPEN" | "CLOSED" >("OPEN");
const messages = ref<Message[]>([]);
const loading = ref(true);

const bottomRef = ref<HTMLDivElement | null>(null);

function scrollToBottom() {
  nextTick(() => bottomRef.value?.scrollIntoView({ behavior: "smooth" }));
}

watch(messages, scrollToBottom);

async function loadConversation() {
  try {
    const res = await fetch(`http://localhost:80/conversations/${props.conversationId}/`);
    if (!res.ok) {
      console.error("Erro carregando conversa");
      return;
    }

    const data: ConversationResponse = await res.json();

    chatState.value = data.state

    messages.value = data.messages;
  } catch (err) {
    console.error("Erro:", err);
  } finally {
    loading.value = false;
  }
}

async function closeConversation() {
  try {
    await fetch("http://localhost:80/webhook/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        type: "CLOSE_CONVERSATION",
        timestamp: new Date().toISOString(),
        data: {
          id: props.conversationId
        }
      }),
    });

    chatState.value = "closed"; // Atualiza imediatamente
  } catch (err) {
    console.error("Erro encerrando conversa:", err);
  }
}


let interval: number | null = null;

onMounted(async () => {
  await loadConversation();

  interval = setInterval(loadConversation, 1500);
});

onUnmounted(() => {
  if (interval) clearInterval(interval);
});

async function handleSend(content: string) {
  if (chatState.value !== "OPEN") return;

  try {
    await fetch("http://localhost:80/webhook/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        type: "NEW_MESSAGE",
        timestamp: new Date().toISOString(),
        data: {
          id: crypto.randomUUID(),
          direction: "SENT",
          content,
          conversation_id: props.conversationId,
        },
      }),
    });

    await loadConversation();
  } catch (e) {
    console.error("Erro enviando:", e);
  }
}
</script>

<template>
  <div v-if="loading" class="p-8 text-center text-muted-foreground">
    Carregando conversa...
  </div>

  <div
    v-else
    class="flex flex-col h-screen max-w-2xl mx-auto bg-card shadow-2xl"
  >

    <header
      class="flex items-center justify-between px-6 py-4 bg-primary text-primary-foreground shadow-md"
    >
      <router-link to="/" class="flex items-center gap-2"><h1 class="font-semibold text-lg">Chat</h1></router-link>

      <div class="flex items-center gap-3">

        <span v-if="chatState === 'closed'" class="text-sm opacity-80">
          (Encerrado)
        </span>

        <!-- BOTÃO DE ENCERRAR -->
        <button
          v-if="chatState === 'OPEN'"
          @click="closeConversation"
          class="px-3 py-1 text-sm rounded-md bg-destructive text-destructive-foreground hover:bg-destructive/80 transition"
        >
          Encerrar
        </button>
      </div>
    </header>

    <!-- MENSAGENS -->
    <div class="flex-1 overflow-y-auto p-4 space-y-3 bg-background">
      <EmptyState v-if="messages.length === 0" />

      <template v-else>
        <ConversationMessage
          v-for="m in messages"
          :key="m.id"
          :content="m.content"
          :isSent="m.direction === 'Sent'"
          :timestamp="m.timestamp"
        />
        <div ref="bottomRef"></div>
      </template>
    </div>
    <!-- INPUT -->
    <ConversationInput
      v-if="chatState === 'OPEN'"
      @send="handleSend"
    />

    <div
      v-if="chatState === 'CLOSED'"
      class="p-4 text-center text-muted-foreground text-sm"
    >
      Esta conversa está encerrada.
    </div>
  </div>
</template>
