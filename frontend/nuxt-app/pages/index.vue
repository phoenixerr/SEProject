<template>
  <login-nav-bar/>
  <br><br>

  <div class="flex align-items-center justify-content-center">
    <Card class="shadow-7 w-6 h-6">

      <template #title>
        <div class="font-bold text-3xl">Login</div>
      </template>

      <template #content>
        <div class="flex align-items-center justify-content-center">
          <form @submit.prevent="login" class="w-6">
            <FloatLabel>
              <InputText id="username" v-model.trim="userName" required size="large"
                         autocomplete="username" fluid/>
              <label for="username" class="font-medium">Username</label>
            </FloatLabel>
            <br><br>
            <FloatLabel>
              <InputText id="password" v-model="password" type="password" size="large"
                         autocomplete="current-password" fluid/>

              <label for="password" class="font-medium">Password</label>
            </FloatLabel>
            <br>
            <Button label="Log In"
                    type="submit" class="flex justify-content-center w-full"
                    icon="pi pi-sign-in"
                    raised
                    rounded
            />
            <br>

            <br>
            <div v-if="loginType!=='Admin'">
              <divider class="flex justify-content-center w-full"/>
              <span class="flex justify-content-center w-full">Don't Have an Account?</span>
              <br>
              <Button :label="`Register`"
                      severity="info"
                      icon="pi pi-user-plus"
                      class="flex justify-content-center w-full"

                      raised
                      rounded
              />
            </div>
          </form>
        </div>

      </template>

    </Card>
  </div>


</template>


<script setup>

const baseURL = inject('baseURL');
const toast = inject('toast');
const router = useRouter();

const adminStore = useAdminStore();
const studentStore = useStudentStore();


const userName = ref();
const password = ref();

const loginType = ref('Admin');
// const loginType = ref('Student');

const login = async () => {

  const {data, error} = await useFetch(`${baseURL}/login`, {
    method: 'POST',
    body: JSON.stringify({username: userName.value, password: password.value}),
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

    if(data.value.student){
      studentStore.accessToken = data.value.access_token;
      router.push('/student/home');
    }
    else if(data.value.instructor){

    }
    else{
      adminStore.accessToken = data.value.access_token;
      router.push('/admin/home');
    }
    toast.add({
      severity: 'success', summary: 'Success', detail: 'You Have Successfully Logged in',life:2500
    });


  }

}

</script>


<style scoped>

</style>