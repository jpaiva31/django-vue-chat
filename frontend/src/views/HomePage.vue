<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

interface Conversation {
  id: string;
  state: "OPEN" | "CLOSED";
  created_at: string;
}

const conversations = ref<Conversation[]>([]);
const loading = ref(true);
const creating = ref(false);

const router = useRouter();

/* ==========================
   CARREGAR LISTA DE CONVERSAS
   ========================== */
async function loadConversations() {
  try {
    const res = await fetch("http://localhost:80/conversations/");
    if (!res.ok) {
      console.error("Erro carregando conversas");
      return;
    }

    const data = await res.json();

    // Filtra só as conversas abertas
    conversations.value = data.filter(
      (c: Conversation) => c.state === "OPEN"
    );

  } catch (err) {
    console.error("Erro:", err);
  } finally {
    loading.value = false;
  }
}

onMounted(loadConversations);

/* ==========================
   CRIAR NOVA CONVERSA
   ========================== */
async function createConversation() {
  if (creating.value) return;

  creating.value = true;
  const id = crypto.randomUUID();

  try {
    await fetch("http://localhost:80/webhook/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        type: "NEW_CONVERSATION",
        timestamp: new Date().toISOString(),
        data: { id },
      }),
    });

    router.push(`/conversation/${id}`);
  } catch (err) {
    console.error("Erro criando conversa:", err);
  } finally {
    creating.value = false;
  }
}
</script>

<template>
  <div class="min-h-screen flex flex-col items-center bg-background py-10">

    <div class="w-full max-w-lg bg-card shadow-xl rounded-xl p-8">
      <h1 class="text-2xl font-semibold mb-6 text-center">
        Conversas Abertas
      </h1>

      <div v-if="loading" class="text-muted-foreground text-center py-8">
        Carregando...
      </div>

      <!-- LISTA DE CONVERSAS -->
      <div v-else>
        <div v-if="conversations.length === 0" class="text-center text-muted-foreground py-6">
          Nenhuma conversa aberta ainda.
        </div>

        <div v-else class="space-y-3">
          <button
            v-for="c in conversations"
            :key="c.id"
            @click="router.push(`/conversation/${c.id}`)"
            class="w-full flex justify-between items-center px-4 py-3 bg-muted hover:bg-muted/80 rounded-lg shadow transition"
          >
            <span>Conversa {{ c.id }}</span>
          </button>
        </div>
      </div>

      <hr class="my-8 opacity-30" />

      <!-- BOTÃO CRIAR -->
      <button
        @click="createConversation"
        :disabled="creating"
        class="w-full px-6 py-3 rounded-lg bg-primary text-primary-foreground font-medium text-lg shadow hover:bg-primary/90 transition disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {{ creating ? "Criando..." : "Criar nova conversa" }}
      </button>
    </div>

  </div>
</template>
