<template>

  <div class="flex grid">
    <div class="col-3">
      <student-side-bar :data="studentStore.weeks" dataKey="assignmentDetails"
                        :command="(currentAssignment)=>{studentStore.selectedAssignment = currentAssignment}"/>
    </div>
    <div class="col-9" v-if="studentStore.selectedAssignment">
      <div class="text-xl font-semibold">{{ studentStore.selectedAssignment?.title }}</div>
      <span class="text-xs font-bold" style="color: #d10b0b">Due Date: {{
          formatDatetimeToStandard(studentStore.selectedAssignment?.due_date)
        }}</span>
      <ScrollPanel>
        <div v-for="(question,index) in studentStore.selectedAssignment.questions">
          <div class="flex mx-1 gap-2 my-2 align-items-center">
            <span>{{ index + 1 }}.</span>
            <div v-html="md.render(question.text)"/>
            <br>
          </div>
          <div v-for="(option,index) in question.options" class="flex gap-2 mx-1 my-3 align-items-center">
            <CheckBox :input-id="option.id" :value="option.id" v-model="question.markedOption" v-if="question.is_msq"/>
            <RadioButton :input-id="option.id" :value="option.id" v-model="question.markedOption" variant="filled"
                         v-else/>
            <label :for="option.id"
                   class="correct_answer"
                   v-if="submitted&option.is_correct"
            >{{ option.text }}</label>
            <label :for="option.id"
                   class="wrong_answer"
                   v-else-if="submitted&!option.is_correct"
            >{{ option.text }}</label>
            <label :for="option.id" v-else>{{ option.text }}</label>

          </div>

          <divider/>

        </div>
      </ScrollPanel>

      <Button label="Submit" severity="success" icon="pi pi-check" @click="submitAndEvaluate"/>


    </div>
  </div>

</template>


<script setup>

const toast = inject('toast')

import markdownit from 'markdown-it'

const md = markdownit();

const submitted = ref(false);

const studentStore = useStudentStore();

function formatDatetimeToStandard(datetimeString) {
  const date = new Date(datetimeString);

  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
  const year = date.getFullYear();
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');

  return `${day}/${month}/${year} ${hours}:${minutes}`;
}

const submitAndEvaluate = () => {

  submitted.value = true;
  toast.add({severity: 'success', summary: 'Successfully evaluated...',description:'Assignment Successfully Submitted'});

}

</script>


<style scoped>

.correct_answer {
  color: green;
}

.wrong_answer {
  color: red;
}

</style>