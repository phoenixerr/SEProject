<template>
    <login-nav-bar/>
    <AdminNavBar/>
    <div class="p-grid">
      <div class="p-col-12">
        <h1>Users</h1>
      </div>
      <div class="p-col-12">
        <div class="p-col-12">
        <h2>Instructors</h2>
      </div>
            <div
            class="w-2 no-underline "
            v-for="inst in adminStore.instructors"
            :key="inst.id">
            <Card class="shadow-5  w-full min-h-full">
              <template #content>
                <div class="flex p-2 text-xl font-bold justify-content-center align-items-center ">
                  {{ inst.name }}
                </div>
                <Button severity="danger" size="large"
                  @click="delIsnt(inst.id)"
                  rounded raised icon="pi pi-trash"
                  v-tooltip.top="'Delete Instructor'"/>
              </template>
            </Card>
          </div>
          <div class="p-col-12">
        <h2>Students</h2>
      </div>
            <div
            class="w-2 no-underline "
            v-for="stu in adminStore.students"
            :key="stu.id">
            <Card class="shadow-5  w-full min-h-full">
              <template #content>
                <div class="flex p-2 text-xl font-bold justify-content-center align-items-center ">
                  {{ stu.name }}
                </div>
                <p class="flex justify-content-center align-items-center">Current CGPA: {{ stu.cgpa }}</p>

                <Button severity="danger" size="large"
                  @click="delStudent(stu.id)"
                  rounded raised icon="pi pi-trash"
                  v-tooltip.top="'Delete  Student'"/>
              </template>
            </Card>
          </div>
      </div>
    </div>
  </template>
  
  <script setup>
  const levels = ['Instructors', 'Students'];
  const displayCourseDetails = ref(false);
  const toast = inject('toast');
  const router = useRouter();

  const baseURL = inject('baseURL');
  const adminStore = useAdminStore();

  import AdminNavBar from '../components/AdminNavBar.vue';

for( let i = 0; i < adminStore.instructors.length; i++){
    const user_id = adminStore.instructors[i].id;
    const {data, error} = await useFetch(`${baseURL}/user/${user_id}`, 
    {
    headers: {Authorization: `Bearer ${adminStore.accessToken}`},
  })
  adminStore.instructors[i] = {'id':data.value.id,'name':data.value.name,'username':data.value.username}
  }

  for( let i = 0; i < adminStore.students.length; i++){
    const user_id = adminStore.students[i].id;
    const {data, error} = await useFetch(`${baseURL}/user/${user_id}`, 
    {
    headers: {Authorization: `Bearer ${adminStore.accessToken}`},
  })
  const student_details = await useFetch(`${baseURL}/student/${user_id}`,
    {
      headers: {Authorization: `Bearer ${adminStore.accessToken}`},
    }
  )
  adminStore.students[i] = {'id':data.value.id,'name':data.value.name,'username':data.value.username,'cgpa':student_details.data.value.cgpa}
  console.log({'cgpa':student_details.data.value.cgpa})
  }
  async function delIsnt(id) {
  const {data, error} = await useFetch(`${baseURL}/instructor/${id}`,{
    method:'DELETE',
    headers: {Authorization: `Bearer ${adminStore.accessToken}`},
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
  // router.push('/');
  toast.add({
    severity: 'success',
    summary: 'User has been deleted',
    detail: 'User has been deleted',
    life: 2500
  });
  router.push('/admin/home');
  }
}
async function delStudent(id) {
  const {data, error} = await useFetch(`${baseURL}/student/${id}`,{
    method:'DELETE',
    headers: {Authorization: `Bearer ${adminStore.accessToken}`},
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
  // router.push('/');
  toast.add({
    severity: 'success',
    summary: 'User has been deleted',
    detail: 'User has been deleted',
    life: 2500
  });
  router.push('/admin/home');
  }
}
  </script>