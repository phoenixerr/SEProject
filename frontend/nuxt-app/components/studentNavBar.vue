<template>
  <div class="card">
    <MegaMenu class="py-1 bg-surface-1 shadow-3">
      <template #start>
        <div class="flex gap-2 align-items-center">
          <Button v-if="props.sideMenu??false" severity="secondary" icon="pi pi-bars"
                  @click="()=>{showMenu=!showMenu}"></Button>
          <img src="@/images/programming-svgrepo-com-2.svg" alt="logo" class="h-1 w-1"/>
          <span class="font-bold text-2xl " style="font-family: Futura, “Trebuchet MS”, Arial, sans-serif;">
            NeoSeek
          </span>
        </div>
      </template>
      <template #end>
        <div class="flex gap-4 align-items-center">

          <Avatar shape="circle" size="xlarge" :label="studentStore.userData?.name[0]"/>
          <span class="font-bold text-xl">Welcome {{ studentStore.userData?.name }}</span>
          <Button severity="danger" size="large"
                  @click="logOut"
                  rounded raised icon="pi pi-sign-out"
                  v-tooltip.top="'Logout'"/>

        </div>
      </template>

    </MegaMenu>
  </div>
</template>

<script setup>

const baseURL = inject('baseURL');
const router = useRouter();
const toast = inject('toast');

const showMenu = inject('showMenu');
const studentStore = useStudentStore();

const props = defineProps(['sideMenu']);


const logOut = async () => {
  const {data, error} = await useFetch(`${baseURL}/logout`);

  studentStore.$reset();

  router.push('/');
  toast.add({
    severity: 'success',
    summary: 'Logged out successfully',
    detail: 'You have been logged out successfully',
    life: 2500
  });

}


</script>
