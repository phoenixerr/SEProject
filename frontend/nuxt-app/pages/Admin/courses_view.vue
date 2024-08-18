<template>
    <login-nav-bar/>
    <AdminNavBar/>
    <div class="p-grid">
      <div class="p-col-12">
        <h1>Courses</h1>
      </div>
      <div class="p-col-12">
        <div>
          <Button severity="success" size="large"
                  @click="addcourse()"
                  rounded raised icon="pi pi-plus"
                  v-tooltip.top="'Add Course'"/>
        </div>
          
        <TabView>
          <TabPanel v-for="level in levels" :key="level" :header="level">
            <DataTable :value="getCoursesByLevel(level)" :paginator="true" :rows="10">
              <Column field="name" header="Course Name">
              </Column>
              <Column field="actions" header="Actions">
                <template #body="slotProps">
                  <Button severity="danger" size="large"
                  @click="delcourse(slotProps.data)"
                  rounded raised icon="pi pi-trash"
                  v-tooltip.top="'Delete'"/>  
              </template>
            </Column>
            </DataTable>
          </TabPanel>
        </TabView>
      </div>
    </div>
  </template>
  
  <script setup>
  import AdminNavBar from '../components/AdminNavBar.vue';
  const baseURL = inject('baseURL');
  const adminStore = useAdminStore();
  const toast = inject('toast');
  const router = useRouter();


  const levels = ['Foundational', 'Diploma', 'Degree'];
  
  const getCoursesByLevel = (level) => {
    let courses_by_level = []
    if (level === 'Foundational'){
      let j = 0
      for (let i = 0; i < adminStore.courses.length;i++){
        if(adminStore.courses[i].level === 1){
          courses_by_level[j] = {'id':adminStore.courses[i].id,'name':adminStore.courses[i].name}
          j++

        }
      }
    }
    if (level === 'Diploma'){
      let j = 0
      for (let i = 0; i < adminStore.courses.length;i++){
        if(adminStore.courses[i].level === 2){
          courses_by_level[j] = {'id':adminStore.courses[i].id,'name':adminStore.courses[i].name}
          j++
        }
      }
    }
    if (level === 'Degree'){
      let j = 0
      for (let i = 0; i < adminStore.courses.length;i++){
        if(adminStore.courses[i].level === 3){
          courses_by_level[j] = {'id':adminStore.courses[i].id,'name':adminStore.courses[i].name}
          j++
        }
      }
    }
    return courses_by_level
  };
  
  async function delcourse(course_data) {
    const {data, error} = await useFetch(`${baseURL}/course/${course_data.id}`,{
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
    toast.add({
    severity: 'success',
    summary: 'Course has been deleted',
    detail: 'Course has been deleted',
    life: 2500
  });
  router.push('/admin/home');

  };
}

function addcourse(){
  router.push('/admin/add_course');
}
  </script>