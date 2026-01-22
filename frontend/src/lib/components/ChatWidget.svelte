<script>
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';
  import { api } from '$lib/api.js';

  /** @type {boolean} */
  let isOpen = false;

  /** @type {string} */
  let question = '';

  /** @type {boolean} */
  let isLoading = false;

  /** @type {Array<{question: string, answer: string, timestamp: Date}>} */
  let chatHistory = [];

  /** @type {string} */
  let error = '';

  /** @type {HTMLElement | null} */
  let chatHistoryContainer = null;

  // Auto-scroll to bottom when chat history changes
  $: if (chatHistory.length > 0 && chatHistoryContainer) {
    setTimeout(() => {
      if (chatHistoryContainer) {
        chatHistoryContainer.scrollTop = chatHistoryContainer.scrollHeight;
      }
    }, 100);
  }

  // Load chat history from sessionStorage on mount
  onMount(() => {
    if (browser) {
      const savedHistory = sessionStorage.getItem('chatHistory');
      const savedIsOpen = sessionStorage.getItem('chatWidgetOpen');

      if (savedHistory) {
        try {
          const parsed = JSON.parse(savedHistory);
          chatHistory = parsed.map(
            /** @param {any} msg */
            (msg) => ({
              ...msg,
              timestamp: new Date(msg.timestamp)
            })
          );
        } catch (e) {
          console.error('Failed to load chat history:', e);
        }
      }

      if (savedIsOpen === 'true') {
        isOpen = true;
      }
    }
  });

  // Save chat history to sessionStorage whenever it changes
  $: if (browser && chatHistory.length >= 0) {
    sessionStorage.setItem('chatHistory', JSON.stringify(chatHistory));
  }

  // Save open state to sessionStorage
  $: if (browser) {
    sessionStorage.setItem('chatWidgetOpen', isOpen.toString());
  }

  function toggleChat() {
    isOpen = !isOpen;
  }

  async function sendQuestion() {
    if (!question.trim() || isLoading) return;

    const currentQuestion = question.trim();
    question = '';
    isLoading = true;
    error = '';

    try {
      const response = await api.chat(currentQuestion);

      chatHistory = [
        ...chatHistory,
        {
          question: currentQuestion,
          answer: response.answer,
          timestamp: new Date()
        }
      ];
    } catch (err) {
      error = err instanceof Error ? err.message : 'Failed to get response from AI assistant';
      console.error('Chat error:', err);
    } finally {
      isLoading = false;
    }
  }

  /**
   * @param {KeyboardEvent} event
   */
  function handleKeydown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      sendQuestion();
    }
  }

  // Sample questions to help users get started
  const sampleQuestions = [
    'Which ventures have the highest burn rate?',
    'How many ventures are in each stage?',
    'What are the most common venture statuses?',
    'Which pod has the most ventures?',
    'Show me ventures with runway less than 6 months'
  ];

  /**
   * @param {string} sampleQ
   */
  function useSampleQuestion(sampleQ) {
    question = sampleQ;
    // Auto-focus the textarea after setting question
    setTimeout(() => {
      const textarea = /** @type {HTMLTextAreaElement | null} */ (
        document.querySelector('#chat-textarea')
      );
      if (textarea) {
        textarea.focus();
      }
    }, 100);
  }
</script>

<!-- Chat Toggle Button -->
<button
  on:click={toggleChat}
  class="fixed right-6 bottom-6 z-50 flex h-14 w-14 items-center justify-center rounded-full bg-blue-600 text-white shadow-lg transition-all hover:bg-blue-700 hover:shadow-xl {isOpen
    ? 'scale-0 opacity-0'
    : 'scale-100 opacity-100'}"
  aria-label="Toggle chat"
>
  {#if chatHistory.length > 0}
    <span
      class="absolute -top-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-red-500 text-xs font-bold text-white"
    >
      {chatHistory.length}
    </span>
  {/if}
  <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path
      stroke-linecap="round"
      stroke-linejoin="round"
      stroke-width="2"
      d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
    ></path>
  </svg>
</button>

<!-- Chat Widget -->
<div
  class="fixed right-0 bottom-0 z-40 flex h-[600px] w-full max-w-md flex-col rounded-t-xl border border-gray-200 bg-white shadow-2xl transition-transform duration-300 ease-out {isOpen
    ? 'translate-y-0'
    : 'translate-y-full'}"
>
  <!-- Header -->
  <div class="flex items-center justify-between border-b border-gray-200 px-4 py-3">
    <div>
      <h2 class="text-lg font-bold text-gray-900">Venture AI Assistant</h2>
      <p class="text-xs text-gray-600">Ask questions about your ventures</p>
    </div>
    <button
      on:click={toggleChat}
      class="rounded-lg p-2 text-gray-400 transition-colors hover:bg-gray-100 hover:text-gray-600"
      aria-label="Close chat"
    >
      <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M6 18L18 6M6 6l12 12"
        ></path>
      </svg>
    </button>
  </div>

  <!-- Chat History -->
  <div bind:this={chatHistoryContainer} class="flex-1 space-y-4 overflow-y-auto p-4">
    {#if chatHistory.length === 0}
      <!-- Welcome message -->
      <div class="py-8 text-center">
        <div
          class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-blue-100"
        >
          <svg class="h-6 w-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
            ></path>
          </svg>
        </div>
        <h3 class="mb-2 text-base font-medium text-gray-900">Start a conversation</h3>
        <p class="mb-4 text-sm text-gray-500">Ask me anything about your ventures!</p>

        <!-- Sample questions -->
        <div class="space-y-2">
          {#each sampleQuestions as sampleQ}
            <button
              on:click={() => useSampleQuestion(sampleQ)}
              class="w-full rounded-lg border border-gray-200 bg-gray-50 p-2 text-left text-sm text-gray-700 transition-colors hover:bg-gray-100"
            >
              {sampleQ}
            </button>
          {/each}
        </div>
      </div>
    {:else}
      {#each chatHistory as message}
        <!-- User message -->
        <div class="flex justify-end">
          <div class="max-w-[80%] rounded-lg bg-blue-600 px-3 py-2 text-white">
            <p class="text-sm">{message.question}</p>
          </div>
        </div>

        <!-- AI response -->
        <div class="flex justify-start">
          <div class="max-w-[80%] rounded-lg bg-gray-100 px-3 py-2 text-gray-900">
            <div class="text-sm whitespace-pre-wrap">{message.answer}</div>
            <div class="mt-1 text-xs text-gray-500">
              {message.timestamp.toLocaleTimeString()}
            </div>
          </div>
        </div>
      {/each}
    {/if}

    {#if isLoading}
      <div class="flex justify-start">
        <div class="rounded-lg bg-gray-100 px-3 py-2 text-gray-900">
          <div class="flex items-center space-x-2">
            <div class="flex space-x-1">
              <div class="h-2 w-2 animate-bounce rounded-full bg-gray-400"></div>
              <div
                class="h-2 w-2 animate-bounce rounded-full bg-gray-400"
                style="animation-delay: 0.1s"
              ></div>
              <div
                class="h-2 w-2 animate-bounce rounded-full bg-gray-400"
                style="animation-delay: 0.2s"
              ></div>
            </div>
            <span class="text-sm text-gray-500">AI is thinking...</span>
          </div>
        </div>
      </div>
    {/if}

    {#if error}
      <div class="flex justify-center">
        <div
          class="max-w-[80%] rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700"
        >
          {error}
        </div>
      </div>
    {/if}
  </div>

  <!-- Input area -->
  <div class="border-t border-gray-200 p-4">
    <div class="flex space-x-2">
      <div class="flex-1">
        <textarea
          id="chat-textarea"
          bind:value={question}
          on:keydown={handleKeydown}
          placeholder="Ask a question about your ventures..."
          class="w-full resize-none rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500 focus:outline-none"
          rows="2"
          disabled={isLoading}
        ></textarea>
      </div>
      <button
        on:click={sendQuestion}
        disabled={!question.trim() || isLoading}
        class="flex items-center justify-center rounded-lg bg-blue-600 px-4 py-2 text-white transition-colors hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-gray-400"
        aria-label="Send message"
      >
        {#if isLoading}
          <div
            class="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"
          ></div>
        {:else}
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
            ></path>
          </svg>
        {/if}
      </button>
    </div>
    <p class="mt-1 text-xs text-gray-500">Press Enter to send, Shift+Enter for new line</p>
  </div>
</div>

<style>
  /* Smooth scroll to bottom when new messages arrive */
  :global(.chat-history) {
    scroll-behavior: smooth;
  }
</style>
