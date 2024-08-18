<template>

  <Tabs value="0">
    <TabList>
      <Tab value="0">Table View</Tab>
      <Tab value="1">Calendar View</Tab>
    </TabList>
    <TabPanels>
      <TabPanel value="0">
        <DataTable :value="studentStore.events" class="shadow-7" showGridlines striped-rows>
          <Column>
            <template #header>
              <span class="font-bold text-xl">S.No</span>
            </template>
            <template #body="{index}">{{ index + 1 }}</template>
          </Column>
          <Column field="title" header="">
            <template #header>
              <span class="font-bold text-xl">Title</span>
            </template>

          </Column>
          <Column field="start" header="">
            <template #header>
              <span class="font-bold text-xl">Start Date</span>
            </template>
            <template #body="{data,field}">
              {{ formatDatetimeToStandard(data[field]) }}
            </template>
          </Column>
          <Column field="end" header="">
            <template #header>
              <span class="font-bold text-xl">End Date</span>
            </template>
            <template #body="{data,field}">
              {{ formatDatetimeToStandard(data[field]) }}
            </template>
          </Column>

        </DataTable>
      </TabPanel>
      <TabPanel value="1">
        <div class="flex justify-content-center w-full h-full">
          <DatePicker inline>
            <template #date="{date}">
              <div class="flex justify-content-center">
                <div
                    :class="{'underline':studentStore.events.find(event=>{
                      return new Date(event.start)===new Date(date.year, date.month - 1, date.day)
                    }
                    )}"

                >
                  {{ date.day }}
                </div>
              </div>

            </template>
          </DatePicker>
        </div>
      </TabPanel>

    </TabPanels>
  </Tabs>

</template>


<script setup>


const studentStore = useStudentStore();

function formatDatetimeToStandard(datetimeString) {
  const date = new Date(datetimeString);

  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
  const year = date.getFullYear();
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');

  return `${day}/${month}/${year} ${hours}:${minutes}`;
}

</script>

<style scoped>

</style>