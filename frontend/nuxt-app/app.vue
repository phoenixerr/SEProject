<template>
  <div>
    <Toast/>
    <NuxtLoadingIndicator />
    <NuxtPage/>
  </div>
</template>

<script setup>

import "primeflex/primeflex.css"
import 'primeicons/primeicons.css'

const baseURL = 'http://127.0.0.1:5000';
const toast = useToast()

provide('baseURL', baseURL);
provide('toast',toast);

</script>
