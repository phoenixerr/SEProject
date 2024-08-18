<template>
  <br>
  <div class="font-semibold text-2xl">
    Courses
    <Divider/>
  </div>

  <br>

  <div class="flex gap-5">
    <NuxtLink
        class="w-2 no-underline "
        v-for="course in studentStore.courses"
        :key="course.id"
        :to="`/student/courses/${course.id}`">
      <Card class="shadow-5  w-full min-h-full">
        <template #content>
          <div class="flex p-2 text-xl font-bold justify-content-center align-items-center ">
            {{ course.name }}
          </div>
        </template>

      </Card>

    </NuxtLink>
  </div>


</template>

<script setup>

const baseURL = inject('baseURL');
const studentStore = useStudentStore();
const router = useRouter();
const toast = inject('toast');

const {data,error} = useFetch(`${baseURL}/courses`,{
  headers:{
    Authorization:`Bearer ${studentStore.accessToken}`,
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

studentStore.courses = data;

</script>

<style scoped>

</style>