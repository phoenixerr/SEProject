<template>
  <Drawer v-model:visible="showChat" class="w-4 md:w-80 lg:w-[15rem]" position="right" header="AI Chatbot" blockScroll>
    <studentChatBox/>
  </Drawer>
  <div class="flex grid">
    <div class="col-3">
      <student-side-bar :data="studentStore.weeks" dataKey="lectureDetails"
                        :command="(currLecture)=>{studentStore.selectedLecture=currLecture}"/>
    </div>
    <div class="col-9 py-5" v-if="studentStore.selectedLecture">
      <div class="text-xl font-semibold">{{ studentStore.selectedLecture?.title }}</div>
      <br><br>
      <div class="justify-content-center iframe-container">
        <iframe :src="`https://www.youtube.com/embed/${studentStore.selectedLecture?.url}`"
                title="YouTube video player" frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                referrerpolicy="strict-origin-when-cross-origin" allowfullscreen
                :key="studentStore.selectedLecture?.id"
        ></iframe>

      </div>
      <div class="flex justify-content-between my-2 gap-2">
        <Panel header="Lecture Summary" class="w-full shadow-5" toggleable>

          <ScrollPanel style="width: 100%; height: 200px" >
            <div v-html="md.render(studentStore.selectedLecture?.summary)">
            </div>
          </ScrollPanel>
        </Panel>

        <Button
            icon="pi pi-comment"
            class="p-5"
            severity="info"
            rounded raised size="large" @click="showChat=true"/>

      </div>
      <br>
    </div>

  </div>


</template>

<script setup>

import markdownit from "markdown-it";

const md = markdownit();

const baseURL = inject('baseURL');

const studentStore = useStudentStore();
const showChat = ref(false);



</script>


<style scoped>
.iframe-container {
  position: relative;
  width: 100%;
  padding-bottom: 56.25%; /* 16:9 Aspect Ratio */
  height: 0;
  overflow: hidden;
}

iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: 0;
}
</style>>