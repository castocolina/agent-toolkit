<script setup lang="ts">
defineProps<{ name: string; email: string }>();
const emit = defineEmits<{ edit: [] }>();
</script>

<template>
  <section class="rounded-lg bg-white p-[18px] text-gray-900 dark:bg-[#1f2937] dark:text-white">
    <h2 class="text-lg font-semibold">{{ name }}</h2>
    <p class="text-sm text-gray-600 dark:text-gray-300">{{ email }}</p>
    <button
      type="button"
      class="mt-4 rounded-md bg-[#1d4ed8] px-4 py-2 text-white hover:bg-[#1e40af] active:bg-[#1e3a8a] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#1d4ed8] dark:bg-[#93c5fd] dark:text-gray-900"
      @click="emit('edit')"
    >
      Edit profile
    </button>
  </section>
</template>
