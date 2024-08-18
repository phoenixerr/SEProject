<template>
    <login-nav-bar/>
    <AdminNavBar/>
    <AdminLayout >
      <div class="dashboard">
        <h1>Dashboard</h1>
        <div class="p-grid" >
          <div class="p-col-12 p-md-4">
            <Card>
              <template #title>Total Instructors</template>
              <template #content>
                <div class="dashboard-card-content">
                  <i class="pi pi-users"></i>
                  <span class="dashboard-card-number">{{ totalInst }}</span>
                </div>
              </template>
            </Card>
          </div>
          <div class="p-col-12 p-md-4">
            <Card>
              <template #title>Total Students</template>
              <template #content>
                <div class="dashboard-card-content">
                  <i class="pi pi-user"></i>
                  <span class="dashboard-card-number">{{ totalStudents }}</span>
                </div>
              </template>
            </Card>
          </div>
          <div class="p-col-12 p-md-4">
            <Card>
              <template #title>Total Courses</template>
              <template #content>
                <div class="dashboard-card-content">
                  <i class="pi pi-book"></i>
                  <span class="dashboard-card-number">{{ totalCourses }}</span>
                </div>
              </template>
            </Card>
          </div>
        </div>
      </div>
    </AdminLayout>
  </template>
  
  <script setup>
const baseURL = inject('baseURL');
const adminStore = useAdminStore();
// const router = useRouter();
// const toast = inject('toast');

  import AdminNavBar from '../components/AdminNavBar.vue';
  
  const totalInst = ref(0);
  const totalStudents = ref(0);
  const totalCourses = ref(0);
  const totalUsers = ref(0);

  const courseDetails = await useFetch(`${baseURL}/courses`, 
  {
    headers: {Authorization: `Bearer ${adminStore.accessToken}`},
  });

  adminStore.courses = courseDetails.data.value

  const studentDetails = await useFetch(`${baseURL}/students`, 
  {
    headers: {Authorization: `Bearer ${adminStore.accessToken}`},
  });

  adminStore.students = studentDetails.data.value

  const instDetails = await useFetch(`${baseURL}/instructors`, 
  {
    headers: {Authorization: `Bearer ${adminStore.accessToken}`},
  });

  adminStore.instructors = instDetails.data.value

    totalInst.value = adminStore.instructors.length;
    totalStudents.value = adminStore.students.length;
    totalCourses.value = adminStore.courses.length;
  const items = ref([
    {
        label: 'Dashboard',
        icon: 'pi pi-home',
        route: 'home'
    },
    {
        label: 'Courses',
        icon: 'pi pi-book',
        route: 'courses_view'
    },
    {
        label: 'Users',
        icon: 'pi pi-user',
        route: 'user_view'
    },
]);
</script>  
  <style scoped>
  .dashboard {
    padding: 1rem;
  }
  
  .dashboard-card-content {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
  }
  
  .dashboard-card-content i {
    margin-right: 1rem;
    font-size: 3rem;
  }
  
  .dashboard-card-number {
    font-weight: bold;
  }
  </style>