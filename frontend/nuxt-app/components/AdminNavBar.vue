<template>
    <Menubar :model="items">
      <template #item="{ item, props, hasSubmenu, root }">
          <router-link v-if="item.route" v-slot="{ href, navigate }" :to="item.route" custom>
                      <a v-ripple :href="href" v-bind="props.action" @click="navigate">
                          <span :class="item.icon" />
                          <span class="ml-2">{{ item.label }}</span>
                      </a>
                  </router-link>
                  <a v-else v-ripple :href="item.url" :target="item.target" v-bind="props.action">
                      <span :class="item.icon" />
                      <span class="ml-2">{{ item.label }}</span>
                      <span v-if="hasSubmenu" class="pi pi-fw pi-angle-down ml-2" />
                  </a>
      </template>
      <template #end>
        <div class="flex gap-4 align-items-center">

          <!-- <Avatar shape="circle" size="xlarge" :label="adminStore.userData?.name[0]"/>
          <span class="font-bold text-xl">Welcome {{ adminStore.userData?.name }}</span> -->
          <Button severity="danger" size="large"
                  @click="logOut"
                  rounded raised icon="pi pi-sign-out"
                  v-tooltip.top="'Logout'"/>
        </div>
      </template>
    </Menubar>
  </template>
  
  <script setup>
const baseURL = inject('baseURL');
const router = useRouter();
const toast = inject('toast');

const adminStore = useAdminStore();

  const items = ref([
    {
        label: 'Dashboard',
        icon: 'pi pi-home',
        route: 'home'
    },
    
    {
        label: 'Users',
        icon: 'pi pi-user',
        route: 'user_view'
    },

    {
        label: 'Courses',
        icon: 'pi pi-book',
        route: 'courses_view'
    },
    {
        label: 'Enroll instructors',
        icon: 'pi pi-plus',
        route: 'add_inst'
    }
]);

const logOut = async () => {
  const {data, error} = await useFetch(`${baseURL}/logout`);

  adminStore.$reset();

  router.push('/');
  toast.add({
    severity: 'success',
    summary: 'Logged out successfully',
    detail: 'You have been logged out successfully',
    life: 2500
  });

}
  </script>
  
  <style scoped>
  .admin-layout {
    display: flex;
    height: 100vh;
  }
  
  .admin-sidebar {
    width: 250px;
    height: 100%;
  }
  
  .admin-content {
    flex: 1;
    padding: 20px;
  }
  </style>