<template>
    <login-nav-bar/>
    <br><br>
  
    <div class="flex align-items-center justify-content-center">
      <Card class="shadow-7 w-6 h-6">
  
        <template #title>
          <div class="font-bold text-3xl">Add a course</div>
        </template>
  
        <template #content>
          <div class="flex align-items-center justify-content-center">
            <form @submit.prevent="addcourse" class="w-6">
              <FloatLabel>
                <InputText id="name" v-model.trim="courseName" required size="large" fluid/>
                <label for="coursename" class="font-medium">Name of the course</label>
              </FloatLabel>
              <br><br>
              <FloatLabel>
                <Select v-model="selectedLevel" :options="levels" optionLabel="name" placeholder="Level" class="w-full md:w-56" />
                <label for="level" class="font-medium">Level of the course</label>
              </FloatLabel>
              <br><br>
              <FloatLabel>
                <InputText id="summary" v-model.trim="courseSummary" autoResize size="large" fluid/>
                <label for="coursesummary" class="font-medium">Summary of the course</label>
              </FloatLabel>
              <br>
              <Button label="Add course"
                      type="submit" class="flex justify-content-center w-full"
                      icon="pi pi-plus"
                      raised
                      rounded
              />
              <br>
  
              <br>
            </form>
          </div>
  
        </template>
  
      </Card>
    </div>
  
  
  </template>
  
  
  <script setup>
  const selectedLevel = ref();
  const levels = [{ name: 'Foundational', code:1 },
    { name: 'Diploma', code: 2 },
    { name: 'Degree', code: 3 },];
  
  const baseURL = inject('baseURL');
  const toast = inject('toast');
  const router = useRouter();
  const adminStore = useAdminStore();
  
  
  const courseName = ref();
  const courseSummary = ref();
  
  const loginType = ref('Admin');
  
  const addcourse = async () => {
  
    const {data, error} = await useFetch(`${baseURL}/courses`, {
      method: 'POST',
      headers: {Authorization: `Bearer ${adminStore.accessToken}`},
      body:{"name": courseName.value, "level": selectedLevel.value.code, "summary": courseSummary.value},
    });
  
    if (error.value) {
      if (error.value.statusCode === 401) {
          toast.add({
            severity: 'error', summary: 'Invalid Credentials', detail: 'Please enter Correct Credentials',life:2500
          });
      }
      else{
        toast.add({
          severity: 'error', summary: 'Invalid Credentials', detail: 'Server Error',life:2500
        });
      }
    }
    else{
      toast.add({
        severity: 'success', summary: 'Success', detail: 'You Have Successfully added a course',life:2500
      });
      router.push('/admin/home');
      // router.push('/student/home');
  
  
    }
  }
  
  </script>
  
  
  <style scoped>
  
  </style>