<template>

  <studentNavBar/>

  <div class="px-4 py-4">
    <NuxtPage/>
  </div>


</template>


<script setup>

const baseURL = inject('baseURL');
const toast = inject('toast');

const showMenu = ref(false);
const router = useRouter();

const studentStore = useStudentStore();

const {data, error} = await useFetch(`${baseURL}/user`, {
  headers: {
    Authorization: `Bearer ${studentStore.accessToken}`
  }
});

if (error.value) {
  router.push('/');
  toast.add({
    severity: 'error',
    summary: 'Error',
    detail: 'Something went wrong.Please Try Logging in Again',
    life: 2500
  });
}

else{
  studentStore.userData = data
}

router.push('/student/home');


provide('showMenu', showMenu);

</script>


<style scoped>
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.8s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}

</style>