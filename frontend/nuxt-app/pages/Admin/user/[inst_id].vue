<template>
  <Breadcrumb :home="home" :model="[
  {label:adminStore.instructor?.name,
    route:`/admin/user/${route.params.id}`},
]">


    <template #item="{item}">
      <NuxtLink :to="item.route" class="no-underline">
        <i :class="`pi ${item.icon}`"/>
        <span>{{ item.label }}</span>
      </NuxtLink>
    </template>
  </Breadcrumb>

  


</template>


<script setup>

const baseURL = inject('baseURL');
const toast = inject('toast');
const route = useRoute();

const adminStore = useAdminStore();


// const courseDetails = await useFetch(`${baseURL}/course/${route.params?.course_id}`, {
//   headers: {Authorization: `Bearer ${studentStore.accessToken}`}
// });
// studentStore.course = courseDetails.data.value;

// const weekDetails = await useFetch(`${baseURL}/course/${route.params?.course_id}/weeks`, {
//   headers: {Authorization: `Bearer ${studentStore.accessToken}`}
// });
// studentStore.weeks = weekDetails.data.value;

// studentStore.weeks?.forEach(async obj => {
//   const lectureDetails = await useFetch(`${baseURL}/week/${obj.id}/lectures`, {
//     headers: {Authorization: `Bearer ${studentStore.accessToken}`}
//   });
//   obj.lectureDetails = lectureDetails.data.value;
// });

// const chatDetails = await useFetch(`${baseURL}/course/${route.params.course_id}/chats`,{
//   headers: {Authorization: `Bearer ${studentStore.accessToken}`}
// });

// studentStore.chats = chatDetails.data.value;


const home = ref({
  icon: 'pi pi-home',
  route: '/admin/home'
});
const items = ref();


</script>


<style scoped>

</style>