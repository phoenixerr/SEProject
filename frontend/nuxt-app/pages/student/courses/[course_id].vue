<template>


  <div class="flex justify-content-between align-items-center">
    <Breadcrumb :home="home"
                :model="[{label:studentStore.course?.name,route:`/student/courses/${route.params.course_id}`}]">
      <template #item="{item}">
        <NuxtLink :to="item.route" class="no-underline">
          <i :class="`pi ${item.icon}`"/>
          <span>{{ item.label }}</span>
        </NuxtLink>
      </template>
    </Breadcrumb>
    <Button label="Refresh Content" severity="info" icon="pi pi-refresh" :loading="loading"
            @click="init">

    </Button>
  </div>

  <Tabs value="0">
    <TabList>
      <tab value="0">Lecture Content</tab>
      <tab value="1">Assignment</tab>
      <tab value="2">Events</tab>
    </TabList>
    <TabPanels>
      <TabPanel value="0">
        <studentLecture/>
      </TabPanel>
      <TabPanel value="1">
        <studentAssignments/>
      </TabPanel>
      <TabPanel value="2">
        <studentEvents/>
      </TabPanel>
    </TabPanels>

  </Tabs>


</template>


<script setup>

const baseURL = inject('baseURL');
const toast = inject('toast');
const route = useRoute();
const loading = ref(false);

const studentStore = useStudentStore();


async function init() {
  loading.value = true;
  const courseDetails = await useFetch(`${baseURL}/course/${route.params?.course_id}`, {
    headers: {Authorization: `Bearer ${studentStore.accessToken}`}
  });
  studentStore.course = courseDetails.data.value;

  const weekDetails = await useFetch(`${baseURL}/course/${route.params?.course_id}/weeks`, {
    headers: {Authorization: `Bearer ${studentStore.accessToken}`}
  });
  studentStore.weeks = weekDetails.data.value;

  for (const obj of studentStore.weeks) {
    const lectureDetails = await useFetch(`${baseURL}/week/${obj.id}/lectures`, {
      headers: {Authorization: `Bearer ${studentStore.accessToken}`}
    });
    const assignmentDetails = await useFetch(`${baseURL}/week/${obj.id}/richassignments`, {
      headers: {Authorization: `Bearer ${studentStore.accessToken}`}
    });

    obj.assignmentDetails = assignmentDetails.data.value;
    for (const assignment of obj.assignmentDetails??[]) {
      for (const question of assignment?.questions??[]) {
        const markedOptions = await useFetch(`${baseURL}/question/${question.id}/marked`, {
          headers: {Authorization: `Bearer ${studentStore.accessToken}`}
        });
        question.markedOptions = markedOptions.data.value;
        question.markedOption = ref(markedOptions);
      }
    }
    obj.lectureDetails = lectureDetails.data.value;
  }

  const chatDetails = await useFetch(`${baseURL}/course/${route.params.course_id}/chats`, {
    headers: {Authorization: `Bearer ${studentStore.accessToken}`}
  });
  studentStore.chats = chatDetails.data.value;

  const eventDetails = await useFetch(`${baseURL}/course/${route.params.course_id}/events`,{
    headers: {Authorization: `Bearer ${studentStore.accessToken}`}
  });
  studentStore.events = eventDetails.data;

  loading.value = false;

  studentStore.selectedAssignment = null;
  studentStore.selectedLectures = null;

}

await init();


const home = ref({
  icon: 'pi pi-home',
  route: '/student/home'
});
const items = ref();


</script>


<style scoped>

</style>