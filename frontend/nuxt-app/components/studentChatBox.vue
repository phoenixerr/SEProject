<template>

  <ScrollPanel style="height: 90%">
    <TransitionGroup name="list" ref="scrollPanel">
      <div v-for="chat in studentStore.chats" :key="chat.id">

        <div class="text-right my-5">
          <label :for="`Prompt ${chat.id}`" class="text-xs text-black-alpha-40 my-2">You
            {{ formatDatetimeToStandard(chat.datetime) }}</label>
          <Message severity="secondary" class="my-1" :id="`Prompt ${chat.id}`">
            <span class="text-right flex ">{{ chat.prompt }}</span>
          </Message>
        </div>

        <div class="my-5">
          <label :for="`Response ${chat.id}`" class="text-xs text-black-alpha-40 my-2">AI
            {{ formatDatetimeToStandard(chat.datetime) }}</label>
          <Message severity="contrast" class="my-1 text-sm" :id="`Response ${chat.id}`"  v-if="chat.id!=='temp'">
            <div v-html="md.render(chat.response)"></div>
          </Message>
          <div class="my-1" :id="`Prompt ${chat.id}`" v-else>
            <Skeleton width="100%" class="mb-2"></Skeleton>
            <Skeleton width="75%"></Skeleton>
          </div>
        </div>
      </div>
      <div ref="lastEle" key="last"/>
    </TransitionGroup>
  </ScrollPanel>

  <div class="flex grid align-items-end" v-focustrap>
    <div class="col-10">
      <InputText class="w-full" placeholder="Type your Prompt Here" v-model.trim="chatInput"/>
    </div>
    <div class="col-2">
      <Button icon="pi pi-send" severity="contrast" @click="sendChat" rounded :disabled="sendingChat"/>
    </div>
  </div>

</template>

<script setup>
import markdownit from "markdown-it";

const md = markdownit();

const baseURL = inject('baseURL');
const route = useRoute();


const sendingChat = ref(false);
const chatInput = ref('');
const lastEle = ref(null)


function formatDatetimeToStandard(datetimeString) {
  const date = new Date(datetimeString);

  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
  const year = date.getFullYear();
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');

  return `${day}/${month}/${year} ${hours}:${minutes}`;
}
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

const studentStore = useStudentStore();

const sendChat = async () => {



  sendingChat.value = true;

  studentStore.chats.push({id: 'temp', prompt: chatInput.value, datetime: new Date()});
  await nextTick();
  lastEle.value.scrollIntoView({behavior: 'smooth'});

  const payload = {prompt: chatInput.value};
  chatInput.value='';



  const {data, error} = await useFetch(`${baseURL}/course/${route.params.course_id}/chats`, {
    headers: {Authorization: `Bearer ${studentStore.accessToken}`},
    method: "POST",
    body: JSON.stringify(payload)
  });

  chatInput.value = '';

  studentStore.chats[studentStore.chats.length - 1] = data.value;

  lastEle.value.scrollIntoView({behavior: 'smooth'})

  sendingChat.value = false;

  await nextTick();

  scrollToBottom();

}

onMounted(() => {
  lastEle.value.scrollIntoView({behavior: 'smooth'});
})


</script>
<style scoped>
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

</style>