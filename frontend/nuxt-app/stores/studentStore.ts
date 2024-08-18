export const useStudentStore = defineStore('studentStore', {
    state: () => ({
        accessToken: null,
        userData: null,
        courses: [],
        course: null,
        weeks: [],
        lectures: [],
        selectedLecture: null,
        selectedAssignment: null,
        chats: [],
        questions: [],
        events:[]
    }),
    actions: {},
})