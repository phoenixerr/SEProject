<template>
    <login-nav-bar/>
    <br><br>
  
    <div class="flex align-items-center justify-content-center">
      <Card class="shadow-7 w-6 h-6">
  
        <template #title>
          <div class="font-bold text-3xl">Assign an Instructor to teach a course</div>
        </template>
  
        <template #content>
          <div class="flex align-items-center justify-content-center">
            <form @submit.prevent="addins" class="w-6">
                <FloatLabel>
                <Select v-model="selectedInst" :options="adminStore.instructors" optionLabel="name" placeholder="Instructor" class="w-full md:w-56" />
                <label for="level" class="font-medium">Instructor</label>
              </FloatLabel>
              <br><br>
              <FloatLabel>
                <Select v-model="selectedCourse" :options="adminStore.course" optionLabel="name" placeholder="Course" class="w-full md:w-56" />
                <label for="level" class="font-medium">Course</label>
              </FloatLabel>
              <br><br>
              <br>
              <Button label="Add course"
                      type="submit" class="flex justify-content-center w-full"
                      icon="pi pi-plus"
                      raised
                      rounded
              /><br>
              <Button severity="danger" @click="cancel()"
              label="cancel" class="flex justify-content-center w-full"
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
  const selectedInst = ref();
  const selectedCourse = ref();
  const Inst = [];
  const Course = []
  
  const baseURL = inject('baseURL');
  const toast = inject('toast');
  const router = useRouter();
  const adminStore = useAdminStore();
  

  function cancel(){
        router.push('/admin/home')
  }

  function getfreecourse(){
    
  }
  const addins = async () => {
  
    const {data, error} = await useFetch(`${baseURL}/instructor/${selectedInst.value.id}/teach/${selectedCourse.value.id}`, {
      headers: {Authorization: `Bearer ${adminStore.accessToken}`},
      method:'POST'

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