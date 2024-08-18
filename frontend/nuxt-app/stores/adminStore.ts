export const useAdminStore = defineStore('adminStore', {
    state: () => ({
        accessToken:null,
        userData:null,
        role:null,
        courses:[],
        course:null,
        students:[],
        instructors:[],
    }),
    actions: {

    }
})